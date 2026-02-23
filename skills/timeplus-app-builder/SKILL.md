---
name: timeplus-app-builder
description: Build real-time Timeplus data processing and analysis applications. Creates pure frontend TypeScript/React apps that connect to Timeplus Proton via proton-javascript-driver, apply the Timeplus UI style guide, and visualize live streaming data with the @timeplus/vistral library.
license: Apache-2.0
compatibility: pulsebot>=0.1.0
allowed-tools: shell, workspace, file_ops
---

# Timeplus App Builder

Use this skill whenever the user asks to build a data processing application, pipeline visualizer, real-time dashboard, streaming analytics app, or any frontend tool that queries or visualizes data from Timeplus Proton.

## Overview

You will produce a **pure frontend TypeScript + React** application that:
1. Queries Timeplus Proton via the **PulseBot agent proxy** at `http://localhost:8001/query` — no CORS issues, no direct Proton access needed
2. Visualizes streaming data using `@timeplus/vistral`
3. Follows the **Timeplus App Style Guide** (dark theme, brand colors, clean layout)
4. Is built with Vite and can be deployed via `npm run build`

---

## Step-by-Step Workflow

### Step 1 — Clarify Requirements

Before writing any code, confirm:
- What stream(s) or table(s) to query (name, schema if known)
- What kind of visualization: time series, bar, table, single KPI value, or multi-panel
- Whether the query is **streaming** (`SELECT ... FROM stream_name`) or **historical** (`SELECT ... FROM table(stream_name)`)
- Any filters, aggregations, or window functions needed
- For SQL, consult the `timeplus-sql-guide` skill for correct streaming SQL syntax before writing queries

If the user doesn't know the schema, use `DESCRIBE stream_name` first (run via shell tool or ask the user).

---

### Step 2 — Scaffold the Project

Use the `shell` or `workspace` tool to create the project:

```bash
# Create Vite + React + TypeScript project
npm create vite@latest <app-name> -- --template react-ts
cd <app-name>

# Install required dependencies
npm install @timeplus/vistral

# Install dev dependencies
npm install -D typescript @types/react @types/react-dom
```

Project structure to follow:
```
<app-name>/
├── src/
│   ├── main.tsx           # Entry point
│   ├── App.tsx            # Root component + layout
│   ├── components/        # Reusable chart/panel components
│   ├── hooks/             # Custom hooks (useTimeplusQuery, etc.)
│   ├── styles/            # Global CSS (follows style guide)
│   │   └── global.css
│   └── config.ts          # Proton connection config
├── index.html
├── vite.config.ts
└── package.json
```

---

### Step 3 — Proton Connection via Agent Proxy

The PulseBot agent exposes a proxy endpoint at `http://localhost:8001/query` that forwards requests to Proton and handles CORS. **Always use this proxy in generated apps** — never connect to Proton's raw HTTP port directly from the browser.

Read `references/PROTON_DRIVER.md` for full proxy API details.

```typescript
// src/config.ts
export const PROXY_URL = 'http://localhost:8001/query';
```

```typescript
// src/hooks/useTimeplusQuery.ts
import { useState, useEffect, useRef } from 'react';
import { PROXY_URL } from '../config';

interface StreamRow {
  [key: string]: unknown;
}

export function useTimeplusQuery(sql: string, maxRows = 1000) {
  const [rows, setRows] = useState<StreamRow[]>([]);
  const [columns, setColumns] = useState<{ name: string; type: string }[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    if (!sql) return;
    abortRef.current?.abort();
    abortRef.current = new AbortController();
    const ctrl = abortRef.current;

    setRows([]);
    setError(null);
    setIsConnected(false);

    (async () => {
      try {
        const res = await fetch(PROXY_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: sql,
          signal: ctrl.signal,
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
        setIsConnected(true);

        const reader = res.body!.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let colsSet = false;

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop() ?? '';
          for (const line of lines) {
            if (!line.trim()) continue;
            try {
              const row = JSON.parse(line) as StreamRow;
              if (!colsSet) {
                setColumns(
                  Object.keys(row).map(k => ({
                    name: k,
                    type: typeof row[k] === 'number' ? 'float64' : 'string',
                  }))
                );
                colsSet = true;
              }
              setRows(prev => [...prev.slice(-(maxRows - 1)), row]);
            } catch {
              // skip malformed line
            }
          }
        }
      } catch (err: unknown) {
        if ((err as Error).name !== 'AbortError') {
          setError((err as Error).message);
        }
      }
    })();

    return () => ctrl.abort();
  }, [sql, maxRows]);

  return { rows, columns, error, isConnected };
}
```

> **Streaming vs Historical queries** — use the `timeplus-sql-guide` skill to construct correct SQL. The proxy streams `JSONEachRow` format back to the browser regardless of query type.

---

### Step 4 — Visualization with Vistral

Read `references/VISTRAL_API.md` for the full component reference.

**Quick reference:**

```typescript
import { StreamChart, useStreamingData } from '@timeplus/vistral';

// Time series
<StreamChart
  config={{
    chartType: 'line',
    xAxis: 'event_time',   // must be a datetime column
    yAxis: 'value',        // numeric column
    temporalBinding: 'axis-bound',  // scroll with time
    maxDataPoints: 500,
  }}
  data={{
    columns: [
      { name: 'event_time', type: 'datetime64' },
      { name: 'value', type: 'float64' },
    ],
    data: rows,
    isStreaming: true,
  }}
  theme="dark"
/>

// Bar / column chart
<StreamChart
  config={{
    chartType: 'bar',
    xAxis: 'category',
    yAxis: 'count',
    temporalBinding: 'frame-bound',   // latest snapshot
    maxDataPoints: 20,
  }}
  data={{ columns, data: rows, isStreaming: true }}
  theme="dark"
/>

// Single KPI value
import { SingleValueChart } from '@timeplus/vistral';
<SingleValueChart
  config={{ label: 'Total Events', unit: 'events/s' }}
  data={rows[rows.length - 1]?.value ?? 0}
  theme="dark"
/>

// Data table
import { DataTable } from '@timeplus/vistral';
<DataTable
  config={{ maxRows: 50, showTimestamp: true }}
  data={{ columns, data: rows }}
  theme="dark"
/>
```

**Temporal binding cheatsheet:**
| Mode | Best for | Proton SQL pattern |
|------|----------|--------------------|
| `axis-bound` | Scrolling time series | streaming SELECT with `event_time` |
| `frame-bound` | Live leaderboards, snapshots | `LATEST_BY` or window aggregations |
| `key-bound` | Mutable metrics (counts, sums) | changelog stream or materialized view |

---

### Step 5 — Apply Timeplus Style Guide

Read `references/STYLE_GUIDE.md` for the full style rules.

**Core rules (always apply):**

```css
/* src/styles/global.css */
:root {
  /* Brand colors */
  --tp-bg-primary: #0f1117;
  --tp-bg-secondary: #1a1d27;
  --tp-bg-card: #1e2235;
  --tp-bg-hover: #252a3a;

  --tp-accent-primary: #7c6af7;   /* Timeplus purple */
  --tp-accent-secondary: #4fc3f7; /* Cyan for data */
  --tp-accent-success: #4caf82;
  --tp-accent-warning: #f7a84f;
  --tp-accent-danger: #f76f6f;

  --tp-text-primary: #e8eaf6;
  --tp-text-secondary: #9ea3b8;
  --tp-text-muted: #5c6380;

  --tp-border: #2e3450;
  --tp-border-hover: #4a5280;

  --tp-font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  --tp-font-sans: 'Inter', system-ui, sans-serif;

  --tp-radius-sm: 4px;
  --tp-radius-md: 8px;
  --tp-radius-lg: 12px;

  --tp-shadow: 0 2px 12px rgba(0, 0, 0, 0.4);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--tp-bg-primary);
  color: var(--tp-text-primary);
  font-family: var(--tp-font-sans);
  font-size: 14px;
  line-height: 1.5;
}

/* App shell */
.tp-app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.tp-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 24px;
  height: 56px;
  background: var(--tp-bg-secondary);
  border-bottom: 1px solid var(--tp-border);
  flex-shrink: 0;
}

.tp-header-logo {
  width: 28px;
  height: 28px;
}

.tp-header-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--tp-text-primary);
}

.tp-header-badge {
  font-size: 11px;
  padding: 2px 8px;
  background: var(--tp-accent-primary);
  color: white;
  border-radius: 99px;
  font-weight: 500;
}

.tp-main {
  flex: 1;
  overflow: auto;
  padding: 20px 24px;
  display: grid;
  gap: 16px;
}

/* Card */
.tp-card {
  background: var(--tp-bg-card);
  border: 1px solid var(--tp-border);
  border-radius: var(--tp-radius-lg);
  padding: 16px;
  box-shadow: var(--tp-shadow);
}

.tp-card-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--tp-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 12px;
}

/* Status indicator */
.tp-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--tp-text-muted);
}

.tp-status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--tp-text-muted);
}

.tp-status-dot.connected { background: var(--tp-accent-success); }
.tp-status-dot.error { background: var(--tp-accent-danger); }

/* Monospace for SQL / values */
.tp-mono { font-family: var(--tp-font-mono); }

/* Error panel */
.tp-error {
  background: rgba(247, 111, 111, 0.1);
  border: 1px solid var(--tp-accent-danger);
  border-radius: var(--tp-radius-md);
  padding: 12px 16px;
  color: var(--tp-accent-danger);
  font-size: 13px;
}
```

**App shell template:**

```tsx
// src/App.tsx
import './styles/global.css';

function App() {
  return (
    <div className="tp-app">
      <header className="tp-header">
        <span className="tp-header-title">My Stream App</span>
        <span className="tp-header-badge">LIVE</span>
      </header>
      <main className="tp-main">
        {/* panels go here */}
      </main>
    </div>
  );
}

export default App;
```

---

### Step 6 — Assemble & Build

1. Write all source files using the patterns above
2. Run `npm run build` to produce a `dist/` bundle
3. If using the PulseBot workspace tool, serve via `workspace_create_fullstack_app` or just `workspace_create_app` for the built HTML

**Common build issues:**
- Type errors: ensure `@types/react`, `@types/react-dom` are installed
- Vistral peer deps: must have `react >= 18` (vistral bundles AntV G2 automatically)
- Proxy not running: if `localhost:8001/query` is unreachable, confirm the PulseBot agent server is running

---

### Step 7 — Integrate with PulseBot Workspace (optional)

If running inside PulseBot, deploy the app after building:

```python
workspace_create_app(
  session_id=session_id,
  task_name="My Stream App",
  html=open("dist/index.html").read()
)
```

The app connects to `localhost:8001/query` which the PulseBot agent server already handles — no additional backend proxy is needed.

---

## SQL Patterns

Load the `timeplus-sql-guide` skill for all SQL questions:
- How to write streaming vs historical queries
- Window functions (tumble, hop, session)
- Aggregations, joins, filters
- Schema introspection (`DESCRIBE`, `SHOW STREAMS`)

Call `load_skill("timeplus-sql-guide")` before writing any SQL for the app.

---

## Checklist Before Delivering

- [ ] Project scaffolded with `npm create vite@latest -- --template react-ts`
- [ ] `@timeplus/vistral` installed (no direct Proton driver needed — using proxy)
- [ ] Connection points to `http://localhost:8001/query` via POST with `{ query: sql }`
- [ ] `useTimeplusQuery` hook handles streaming, cleanup (AbortController), and error state
- [ ] SQL written using guidance from `timeplus-sql-guide` skill
- [ ] Vistral `StreamChart` used for charts — correct `temporalBinding` for the query type
- [ ] Global CSS follows Timeplus style guide (dark theme, correct CSS variables)
- [ ] Status indicator shows connection state (connected / error)
- [ ] `npm run build` passes without errors
- [ ] App shared with user via workspace URL or as downloadable files
