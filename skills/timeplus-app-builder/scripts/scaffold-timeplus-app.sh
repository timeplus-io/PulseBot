#!/usr/bin/env bash
# scaffold-timeplus-app.sh
# Usage: bash scaffold-timeplus-app.sh <app-name> [proton-host] [proton-port]
# Creates a minimal Timeplus React/TypeScript app scaffold.

set -euo pipefail

APP_NAME="${1:-my-timeplus-app}"
PROTON_HOST="${2:-localhost}"
PROTON_PORT="${3:-8001}"

echo "🚀 Scaffolding Timeplus app: $APP_NAME"
echo "   Proton: http://$PROTON_HOST:$PROTON_PORT"

# Create Vite project
npm create vite@latest "$APP_NAME" -- --template react-ts
cd "$APP_NAME"

# Install dependencies
npm install @timeplus/vistral
npm install -D typescript @types/react @types/react-dom

# Create directories
mkdir -p src/hooks src/components src/styles

# Write config
cat > src/config.ts << 'CONFIG'
// PulseBot agent proxy — handles Proton auth and CORS
export const PROXY_URL = 'http://localhost:8001/query';
CONFIG

# Write global CSS
cat > src/styles/global.css << 'CSS'
:root {
  --tp-bg-primary: #0f1117;
  --tp-bg-secondary: #1a1d27;
  --tp-bg-card: #1e2235;
  --tp-bg-hover: #252a3a;
  --tp-accent-primary: #7c6af7;
  --tp-accent-secondary: #4fc3f7;
  --tp-accent-success: #4caf82;
  --tp-accent-warning: #f7a84f;
  --tp-accent-danger: #f76f6f;
  --tp-text-primary: #e8eaf6;
  --tp-text-secondary: #9ea3b8;
  --tp-text-muted: #5c6380;
  --tp-border: #2e3450;
  --tp-font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  --tp-font-sans: 'Inter', system-ui, sans-serif;
  --tp-radius-lg: 12px;
  --tp-shadow: 0 2px 12px rgba(0,0,0,0.4);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--tp-bg-primary); color: var(--tp-text-primary); font-family: var(--tp-font-sans); font-size: 14px; line-height: 1.5; }
.tp-app { display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
.tp-header { display: flex; align-items: center; gap: 12px; padding: 0 24px; height: 56px; background: var(--tp-bg-secondary); border-bottom: 1px solid var(--tp-border); }
.tp-header-title { font-size: 16px; font-weight: 600; }
.tp-header-badge { font-size: 11px; padding: 2px 8px; background: var(--tp-accent-primary); color: white; border-radius: 99px; font-weight: 500; }
.tp-main { flex: 1; overflow: auto; padding: 20px 24px; display: grid; gap: 16px; }
.tp-card { background: var(--tp-bg-card); border: 1px solid var(--tp-border); border-radius: var(--tp-radius-lg); padding: 16px; box-shadow: var(--tp-shadow); }
.tp-card-title { font-size: 13px; font-weight: 600; color: var(--tp-text-secondary); text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 12px; }
.tp-status { display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--tp-text-muted); }
.tp-status-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--tp-text-muted); }
.tp-status-dot.connected { background: var(--tp-accent-success); }
.tp-status-dot.error { background: var(--tp-accent-danger); }
.tp-error { background: rgba(247,111,111,0.1); border: 1px solid var(--tp-accent-danger); border-radius: 8px; padding: 12px 16px; color: var(--tp-accent-danger); font-size: 13px; }
CSS

# Write useTimeplusQuery hook (uses PulseBot agent proxy)
cat > src/hooks/useTimeplusQuery.ts << 'HOOK'
import { useState, useEffect, useRef } from 'react';
import { PROXY_URL } from '../config';

export interface StreamRow { [key: string]: unknown; }
export interface ColumnDef { name: string; type: string; }

export function useTimeplusQuery(sql: string, maxRows = 1000) {
  const [rows, setRows] = useState<StreamRow[]>([]);
  const [columns, setColumns] = useState<ColumnDef[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    if (!sql) return;
    abortRef.current?.abort();
    abortRef.current = new AbortController();
    const ctrl = abortRef.current;
    setRows([]); setError(null); setIsConnected(false);

    (async () => {
      try {
        const res = await fetch(PROXY_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: sql }),
          signal: ctrl.signal,
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
        setIsConnected(true);
        const reader = res.body!.getReader();
        const dec = new TextDecoder();
        let buf = '';
        let colsSet = false;
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buf += dec.decode(value, { stream: true });
          const lines = buf.split('\n');
          buf = lines.pop() ?? '';
          for (const line of lines) {
            if (!line.trim()) continue;
            try {
              const row = JSON.parse(line) as StreamRow;
              if (!colsSet) {
                setColumns(Object.keys(row).map(k => ({ name: k, type: typeof row[k] === 'number' ? 'float64' : 'string' })));
                colsSet = true;
              }
              setRows(prev => [...prev.slice(-(maxRows - 1)), row]);
            } catch { /* skip */ }
          }
        }
      } catch (err: unknown) {
        if ((err as Error).name !== 'AbortError') setError((err as Error).message);
      }
    })();

    return () => ctrl.abort();
  }, [sql, maxRows]);

  return { rows, columns, error, isConnected };
}
HOOK

# Write skeleton App.tsx
cat > src/App.tsx << 'APP'
import './styles/global.css';
import { useTimeplusQuery } from './hooks/useTimeplusQuery';
import { StreamChart } from '@timeplus/vistral';

// TODO: Replace with your actual stream name and SQL
const SQL = 'SELECT * FROM my_stream';

function App() {
  const { rows, columns, error, isConnected } = useTimeplusQuery(SQL);

  return (
    <div className="tp-app">
      <header className="tp-header">
        <span className="tp-header-title">Timeplus App</span>
        <span className="tp-header-badge">LIVE</span>
        <span className="tp-status" style={{ marginLeft: 'auto' }}>
          <span className={`tp-status-dot ${isConnected ? 'connected' : 'error'}`} />
          {isConnected ? 'Connected' : 'Connecting…'}
        </span>
      </header>
      <main className="tp-main">
        {error && <div className="tp-error">{error}</div>}
        <div className="tp-card">
          <div className="tp-card-title">Live Stream</div>
          {columns.length > 0 && (
            <StreamChart
              config={{
                chartType: 'line',
                xAxis: columns[0].name,
                yAxis: columns[1]?.name ?? columns[0].name,
                temporalBinding: 'axis-bound',
                maxDataPoints: 500,
              }}
              data={{ columns, data: rows, isStreaming: true }}
              theme="dark"
            />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
APP

echo ""
echo "✅ Scaffold complete!"
echo ""
echo "Next steps:"
echo "  cd $APP_NAME"
echo "  # Edit src/App.tsx — replace 'my_stream' with your stream name"
echo "  npm run dev       # development server"
echo "  npm run build     # production build → dist/"
