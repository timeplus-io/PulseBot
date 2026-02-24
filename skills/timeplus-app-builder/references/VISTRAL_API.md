# Vistral API Reference

## Package & CDN

npm: `@timeplus/vistral`  
GitHub: https://github.com/timeplus-io/vistral  
Playground: https://timeplus-io.github.io/vistral/

**UMD import (use this in HTML apps — no npm required):**

Load dependencies first, then Vistral:
```html
<!-- React (required peer dependency) -->
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>

<!-- Vistral peer dependencies — must load BEFORE vistral -->
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

<!-- Vistral UMD — exposes window.Vistral -->
<script src="https://unpkg.com/@timeplus/vistral/dist/index.umd.min.js"></script>
```

Access globals:
```javascript
const { Vistral, React, ReactDOM } = window;
const { StreamChart, SingleValueChart, DataTable, VistralChart } = Vistral;
```

---

## Core Concepts

### Temporal Binding

Vistral has three modes controlling how streaming data maps to the visible frame:

| Mode | Description | Use case |
|------|-------------|----------|
| `'axis'` | X-axis scrolls with time, oldest drops off left | Live time-series trends |
| `'frame'` | Only rows at the latest timestamp are shown | Real-time snapshots, leaderboards |
| `'key'` | Latest value per unique key, updated in place | Mutable counters, live dashboards |

Configure via the `temporal` object in `config`:
```javascript
temporal: {
  mode: 'axis',       // 'axis' | 'frame' | 'key'
  field: 'timestamp', // column name for time or key
  range: 60,          // (axis mode only) window size in seconds/minutes — depends on data
}
```

### Data Format

All chart components accept a `data` prop:
```javascript
{
  columns: [
    { name: 'timestamp', type: 'datetime64' },
    { name: 'value', type: 'float64' },
    { name: 'category', type: 'string' },
  ],
  data: [
    // Array-of-objects format (preferred for Proton driver output):
    { timestamp: '2024-01-01T10:00:00Z', value: 42.5, category: 'A' },
    // OR array-of-arrays format:
    // ['2024-01-01T10:00:00Z', 42.5, 'A'],
  ],
  isStreaming: true,  // set true for live data
}
```

---

## StreamChart (Unified API — use for most cases)

```javascript
React.createElement(StreamChart, {
  config,      // StreamChartConfig — see chart types below
  data,        // StreamDataSource
  theme: 'dark',  // 'dark' | 'light' — always use 'dark' for Timeplus apps
  height: 300,    // optional
  width: '100%',  // optional
})
```

### Line Chart

```javascript
config = {
  chartType: 'line',          // or 'area' for filled
  xAxis: 'timestamp',         // datetime column
  yAxis: 'value',             // numeric column (or array for multi-series)
  color: 'category',          // optional: split into series by this column
  lineStyle: 'curve',         // 'curve' | 'straight'
  points: true,               // show data points
  legend: true,
  gridlines: true,
  temporal: {
    mode: 'axis',
    field: 'timestamp',
    range: 5,                 // show last 5 minutes
  },
  fractionDigits: 2,          // decimal places for Y axis
  colors: ['#7c6af7', '#4fc3f7'],  // optional custom palette
}
```

### Area Chart

```javascript
config = {
  chartType: 'area',
  xAxis: 'timestamp',
  yAxis: 'value',
  color: 'category',          // creates stacked areas if multi-series
  temporal: { mode: 'axis', field: 'timestamp', range: 5 },
}
```

### Bar Chart (Horizontal)

```javascript
config = {
  chartType: 'bar',           // horizontal bars
  xAxis: 'category',          // categorical column
  yAxis: 'count',             // numeric column
  groupType: 'stack',         // 'stack' | 'dodge'
  dataLabel: true,            // show value labels on bars
  temporal: { mode: 'frame', field: '_tp_time' },
}
```

### Column Chart (Vertical)

```javascript
config = {
  chartType: 'column',        // vertical bars
  xAxis: 'month',
  yAxis: 'sales',
  color: 'region',
  groupType: 'dodge',
  gridlines: true,
  temporal: { mode: 'frame', field: '_tp_time' },
}
```

### Single Value (KPI)

```javascript
config = {
  chartType: 'singleValue',
  yAxis: 'activeUsers',       // column whose latest value to display
  fontSize: 72,               // font size for the number
  color: 'green',             // text color
  fractionDigits: 0,
  sparkline: true,            // show mini sparkline
  delta: true,                // show up/down change indicator
  unit: { position: 'left', value: '$' },  // optional prefix/suffix
  temporal: { mode: 'frame', field: '_tp_time' },
}
```

### Data Table

```javascript
config = {
  chartType: 'table',
  tableStyles: {
    // Optional per-column display config:
    timestamp: { name: 'Time', width: 200 },
    value: {
      name: 'Value',
      miniChart: 'sparkline',
      color: {
        type: 'condition',
        conditions: [
          { operator: 'gt', value: 100, color: '#22C55E' },
          { operator: 'lt', value: 50, color: '#EF4444' },
        ],
      },
    },
  },
  temporal: { mode: 'key', field: 'id' },  // deduplicate rows by 'id'
}
```

### Geo Chart

```javascript
config = {
  chartType: 'geo',
  latitude: 'lat',
  longitude: 'lng',
  color: 'category',          // color points by category
  size: { key: 'value', min: 4, max: 20 },  // size points by value column
  zoom: 3,
  center: [40.7128, -74.006], // [lat, lng]
  showZoomControl: true,
  pointOpacity: 0.8,
  temporal: { mode: 'key', field: ['region', 'vehicle_id'] },  // composite key
}
```

---

## Individual Components

### SingleValueChart

```javascript
React.createElement(SingleValueChart, {
  config: {
    label: 'Events per second',
    unit: 'eps',
    precision: 1,
    trend: true,
    sparkline: true,
  },
  data: currentValue,      // number or string
  history: historyArray,   // optional: array of numbers for sparkline
  theme: 'dark',
})
```

### DataTable

```javascript
React.createElement(DataTable, {
  config: {
    maxRows: 100,
    showTimestamp: true,
    columns: ['col1', 'col2'],  // optional: show only these columns
    highlightNew: true,
  },
  data: { columns, data: rows },
  theme: 'dark',
})
```

---

## VistralChart (Low-Level Grammar API)

For complex visualizations beyond what `StreamChart` covers:

```javascript
const spec = {
  type: 'layer',
  marks: [
    {
      type: 'line',
      encode: {
        x: { field: 'ts', type: 'temporal' },
        y: { field: 'value', type: 'quantitative' },
        color: { field: 'service', type: 'nominal' },
      },
    },
  ],
  streaming: {
    mode: 'axis',
    timeField: 'ts',
    windowSeconds: 120,
  },
};

React.createElement(VistralChart, {
  spec,
  source: { columns, data: rows, isStreaming: true },
  theme: 'dark',
})
```

---

## useStreamingData Hook

Manages a bounded streaming buffer in state. **Note:** In HTML UMD apps, this hook requires React functional component context. For plain script usage, manage state manually (e.g. `rows = [...rows.slice(-999), newRow]`).

```javascript
// In a React functional component only:
const { data, append, clear, replace } = Vistral.useStreamingData([], 1000);

append(newRows);    // add new rows
replace(snapshot);  // replace entire dataset (for frame-bound)
clear();            // clear all data
```

---

## Color Palettes

```javascript
const { multiColorPalettes, singleColorPalettes, findPaletteByLabel } = Vistral;

// Multi-color: 'Dawn', 'Morning', 'Midnight', 'Ocean', 'Sunset'
const palette = findPaletteByLabel('Midnight');  // recommended for Timeplus apps
// palette.values = ['#7c6af7', '#4fc3f7', ...]

// Apply to chart:
config.colors = palette.values;
```

Recommended palette for Timeplus apps: **Midnight** (matches the dark purple brand).

---

## Rendering Pattern (UMD)

In a plain HTML app, always render via `React.createElement` — no JSX:

```javascript
const root = ReactDOM.createRoot(document.getElementById('chart'));

function render() {
  root.render(
    React.createElement(StreamChart, {
      config: { chartType: 'line', xAxis: 'ts', yAxis: 'val',
                temporal: { mode: 'axis', field: 'ts', range: 60 } },
      data: { columns, data: rows, isStreaming: true },
      theme: 'dark',
    })
  );
}
```

Call `render()` each time `rows` changes to push updates to the chart.

---

## Temporal Binding Cheatsheet

| Mode | `config.temporal` | Best Proton SQL pattern |
|------|-------------------|------------------------|
| `'axis'` | `{ mode: 'axis', field: 'ts', range: 60 }` | `SELECT ts, val FROM stream` |
| `'frame'` | `{ mode: 'frame', field: '_tp_time' }` | `LATEST_BY` or window aggregation |
| `'key'` | `{ mode: 'key', field: 'device_id' }` | `SELECT device_id, latest(val) GROUP BY device_id` |

---

## Themes

Always use `theme="dark"` for Timeplus-branded applications. The dark theme uses:
- Background: `#1e2235`
- Axis/grid: muted purple-gray
- Default palette: Midnight
