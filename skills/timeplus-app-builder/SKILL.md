---
name: timeplus-app-builder
description: Build real-time Timeplus data processing and analysis applications. Creates pure frontend HTML/JavaScript apps that connect directly to Timeplus Proton via @timeplus/proton-javascript-driver (UMD), visualize live streaming data with @timeplus/vistral (UMD), and follow the Timeplus UI style guide. No npm build or bundler required — output is a single self-contained HTML file.
license: Apache-2.0
compatibility: pulsebot>=0.1.0
allowed-tools: shell, workspace, file_ops
---

# Timeplus App Builder

Use this skill whenever the user asks to build a data processing application, pipeline visualizer, real-time dashboard, streaming analytics app, or any frontend tool that queries or visualizes data from Timeplus Proton.

## Overview

You will produce a **single self-contained HTML file** that:
1. Queries Timeplus Proton directly via `@timeplus/proton-javascript-driver` loaded from unpkg CDN
2. Visualizes streaming data using `@timeplus/vistral` loaded from unpkg CDN
3. Follows the **Timeplus App Style Guide** (dark theme, brand colors, clean layout)
4. Requires **no npm install, no build step** — open the HTML file directly in a browser

> **Key architecture:** Both `@timeplus/proton-javascript-driver` and `@timeplus/vistral` ship UMD builds. Import them via `<script src="https://unpkg.com/...">` tags. The Proton driver connects directly to the agent proxy running at `localhost:8001`.

---

## Step-by-Step Workflow

### Step 1 — Clarify Requirements

Before writing any code, confirm:
- What stream(s) or table(s) to query (name, schema if known)
- What kind of visualization: time series, bar/column, table, single value, or multi-panel
- Whether the query is **streaming** (`SELECT ... FROM stream_name`) or **historical** (`SELECT ... FROM table(stream_name)`)
- Any filters, aggregations, or window functions needed

If the user doesn't know the schema, suggest running `DESCRIBE stream_name` or `SHOW STREAMS` first.

---

### Step 2 — Use the HTML Template

All Timeplus apps follow this single-file HTML template. Read `references/STYLE_GUIDE.md` for style rules and `references/VISTRAL_API.md` for chart configuration options.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>My Timeplus App</title>

  <!-- 1. React (required by Vistral) -->
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>

  <!-- 2. Vistral peer dependencies — load BEFORE vistral -->
  <script src="https://unpkg.com/lodash@4/lodash.min.js"></script>
  <script src="https://unpkg.com/ramda@0.29/dist/ramda.min.js"></script>
  <script src="https://unpkg.com/@antv/g2@5/dist/g2.min.js"></script>
  <script src="https://unpkg.com/@antv/s2@2/dist/s2.min.js"></script>

  <script>
    // Prevent jsx-runtime from crashing on process.env access
    window.process = window.process || {
      env: { NODE_ENV: "production" }
    };

    // Some builds also expect global
    window.global = window.global || window;
  </script>

  <!-- 3. Vistral UMD — exposes window.Vistral -->
  <script src="https://unpkg.com/@timeplus/vistral/dist/index.umd.min.js"></script>

  <!-- 4. Proton JavaScript Driver UMD — exposes window.ProtonDriver -->
  <script src="https://unpkg.com/@timeplus/proton-javascript-driver/dist/index.umd.js"></script>

  <style>
    /* Timeplus design tokens */
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
    .tp-header { display: flex; align-items: center; gap: 12px; padding: 0 24px; height: 56px; background: var(--tp-bg-secondary); border-bottom: 1px solid var(--tp-border); flex-shrink: 0; }
    .tp-header-title { font-size: 16px; font-weight: 600; }
    .tp-header-badge { font-size: 11px; padding: 2px 8px; background: var(--tp-accent-primary); color: white; border-radius: 99px; font-weight: 500; }
    .tp-status { display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--tp-text-muted); margin-left: auto; }
    .tp-status-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--tp-text-muted); }
    .tp-status-dot.connected { background: var(--tp-accent-success); }
    .tp-status-dot.error { background: var(--tp-accent-danger); }
    .tp-main { flex: 1; overflow: auto; padding: 20px 24px; display: grid; gap: 16px; }
    .tp-card { background: var(--tp-bg-card); border: 1px solid var(--tp-border); border-radius: var(--tp-radius-lg); padding: 16px; box-shadow: var(--tp-shadow); }
    .tp-card-title { font-size: 13px; font-weight: 600; color: var(--tp-text-secondary); text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 12px; }
    .tp-error { background: rgba(247,111,111,0.1); border: 1px solid var(--tp-accent-danger); border-radius: 8px; padding: 12px 16px; color: var(--tp-accent-danger); font-size: 13px; display: none; }
    .chart-container { min-height: 300px; }
  </style>
</head>
<body>
  <div class="tp-app">
    <header class="tp-header">
      <span class="tp-header-title">My Stream App</span>
      <span class="tp-header-badge">LIVE</span>
      <span class="tp-status">
        <span class="tp-status-dot" id="status-dot"></span>
        <span id="status-text">Connecting…</span>
      </span>
    </header>
    <main class="tp-main">
      <div class="tp-error" id="error-panel"></div>
      <div class="tp-card">
        <div class="tp-card-title">Live Stream</div>
        <div class="chart-container" id="chart"></div>
      </div>
    </main>
  </div>

  <script>
    // ---- Library globals ----
    // proton-javascript-driver UMD exposes window.ProtonDriver
    const { ProtonClient } = window.ProtonDriver;
    // vistral UMD exposes window.Vistral; React/ReactDOM are also on window
    const { Vistral, React, ReactDOM } = window;
    const { StreamChart } = Vistral;

    // ---- Configuration ----
    const SQL = 'SELECT * FROM my_stream';  // TODO: replace with your SQL

    // Connect to the Proton proxy running on the agent at localhost:8001
    const client = new ProtonClient({ host: 'localhost', port: 8001 });

    // ---- State ----
    let columns = [];
    let rows = [];
    let chartRoot = null;

    // ---- Helpers ----
    function setStatus(state, message) {
      document.getElementById('status-dot').className = 'tp-status-dot ' + (state || '');
      document.getElementById('status-text').textContent = message;
    }

    function showError(msg) {
      const panel = document.getElementById('error-panel');
      panel.style.display = msg ? 'block' : 'none';
      panel.textContent = msg || '';
      if (msg) setStatus('error', 'Error');
    }

    function inferColumns(row) {
      return Object.entries(row).map(([name, value]) => ({
        name,
        type: typeof value === 'number' ? 'float64'
            : String(value).match(/^\d{4}-\d{2}-\d{2}/) ? 'datetime64'
            : 'string',
      }));
    }

    // ---- Render chart ----
    function renderChart() {
      if (columns.length === 0) return;
      if (!chartRoot) chartRoot = ReactDOM.createRoot(document.getElementById('chart'));

      // TODO: adjust config for your data — see references/VISTRAL_API.md
      const config = {
        chartType: 'line',
        xAxis: columns[0].name,
        yAxis: columns[1]?.name ?? columns[0].name,
        temporal: { mode: 'axis', field: columns[0].name, range: 60 },
      };

      chartRoot.render(
        React.createElement(StreamChart, {
          config,
          data: { columns, data: rows, isStreaming: true },
          theme: 'dark',
        })
      );
    }

    // ---- Main query loop ----
    async function runQuery() {
      try {
        setStatus('', 'Connecting…');
        const { rows: stream, abort } = await client.query(SQL);
        setStatus('connected', 'Connected');

        // Expose abort so it can be called externally if needed
        window.stopQuery = abort;

        for await (const row of stream) {
          if (columns.length === 0) columns = inferColumns(row);
          rows = [...rows.slice(-999), row];  // keep last 1000 rows
          renderChart();
        }

        setStatus('', 'Stream ended');
      } catch (err) {
        showError(err.message);
      }
    }

    runQuery();
  </script>
</body>
</html>
```

---

### Step 3 — Proton Connection

Read `references/PROTON_DRIVER.md` for the full driver API.

The driver connects directly to the Proton proxy at `localhost:8001`. UMD global: `window.ProtonDriver`.

```javascript
const { ProtonClient } = window.ProtonDriver;

const client = new ProtonClient({ host: 'localhost', port: 8001 });

const { rows, abort } = await client.query('SELECT * FROM my_stream');

for await (const row of rows) {
  // row is a plain JavaScript object: { col1: val1, col2: val2, ... }
  console.log(row);
}

// To cancel a running streaming query:
abort();
```

---

### Step 4 — Visualization with Vistral

Read `references/VISTRAL_API.md` for the complete component reference.

Vistral UMD global: `window.Vistral`. Key components: `StreamChart`, `SingleValueChart`, `DataTable`.

All charts are rendered via React (`React.createElement`). Always pass `theme="dark"`.

**Quick chart config reference:**

| Chart type | `chartType` | Best for | temporal `mode` |
|-----------|-------------|----------|-----------------|
| Time series | `'line'` or `'area'` | Scrolling metrics over time | `'axis'` |
| Horizontal bars | `'bar'` | Ranked categories, latest snapshot | `'frame'` |
| Vertical bars | `'column'` | Categorical comparison | `'frame'` |
| KPI tile | `'singleValue'` | One big number | `'frame'` |
| Live table | `'table'` | Raw rows / mutable state | `'key'` |
| Geo points | `'geo'` | Location data | `'key'` |

---

### Step 5 — Apply Timeplus Style Guide

Read `references/STYLE_GUIDE.md` for full rules. Core rules always applied:
- Dark background `#0f1117` for page, `#1e2235` for cards
- Purple `#7c6af7` for primary accents
- Inter font for UI, monospace for data values
- Cards with `border-radius: 12px` and border `#2e3450`
- Header 56px with LIVE badge and connection status indicator

---

### Step 6 — Deliver the App

1. Write the complete single-file HTML, filling in the correct SQL and chart config
2. use workspace_create_app to create the app
3. Present the file — it opens directly in a browser with no server or build step needed

For PulseBot deployment:
```python
workspace_create_app(
  session_id=session_id,
  task_name="My Stream App",
  html=open("my-app.html").read()
)
```

---

## SQL Patterns

Load the `timeplus-sql-guide` skill for all SQL questions:
- Streaming vs historical queries
- Window functions (tumble, hop, session)
- Aggregations, joins, filters
- Schema introspection (`DESCRIBE`, `SHOW STREAMS`)

---

## Checklist Before Delivering

- [ ] Single HTML file — no separate JS/CSS files, no package.json, no build step
- [ ] Script load order: React → ReactDOM → lodash → ramda → @antv/g2 → @antv/s2 → vistral → proton-javascript-driver
- [ ] `window.ProtonDriver` destructured for `ProtonClient`
- [ ] `window.Vistral` destructured for `StreamChart` (and other components as needed)
- [ ] `ProtonClient` configured with `{ host: 'localhost', port: 8001 }`
- [ ] SQL uses correct Proton streaming syntax
- [ ] `columns` inferred from first received row using `inferColumns()`
- [ ] Chart `config.temporal` uses correct `mode` for the query type
- [ ] Status indicator updates on connect, stream end, and error
- [ ] `abort()` stored on `window.stopQuery` or similar
- [ ] CSS uses Timeplus design tokens (CSS variables) from the style template
