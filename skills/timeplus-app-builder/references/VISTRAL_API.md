# Vistral API Reference

## Package & Installation

```bash
npm install @timeplus/vistral
```

GitHub: https://github.com/timeplus-io/vistral  
Examples: https://timeplus-io.github.io/vistral/

Vistral is a React component library for **streaming data visualization**, built on top of AntV G2 (Grammar of Graphics).

---

## Core Concepts

### Temporal Binding

Vistral has three modes for handling how streaming data maps to the visual space:

| Mode | Description | Use case |
|------|-------------|----------|
| `axis-bound` | X-axis scrolls with time — oldest data drops off left edge | Live time series (CPU, metrics, events over time) |
| `frame-bound` | Chart always shows the latest snapshot — data is replaced each update | Top-N lists, leaderboards, latest state |
| `key-bound` | Each key has a fixed slot — values update in-place | Mutable counters, per-device gauges |

### StreamDataSource

All chart components accept a `data` prop of type `StreamDataSource`:

```typescript
interface StreamDataSource {
  columns: ColumnDefinition[];
  data: DataRow[];          // array of objects
  isStreaming?: boolean;    // set true for live data
}

interface ColumnDefinition {
  name: string;
  type: string;   // 'string' | 'number' | 'datetime64' | 'float64' | 'int64' | etc.
}

type DataRow = Record<string, unknown>;
```

---

## StreamChart (High-Level API)

Recommended for most use cases. Accepts a `config` object and handles temporal binding automatically.

```typescript
import { StreamChart } from '@timeplus/vistral';

<StreamChart
  config={config}           // StreamChartConfig
  data={streamDataSource}   // StreamDataSource
  theme="dark"              // "dark" | "light" (use "dark" for Timeplus apps)
  height={300}              // optional, default fills container
  width="100%"              // optional
/>
```

### TimeSeriesConfig

```typescript
<StreamChart
  config={{
    chartType: 'line',           // or 'area'
    xAxis: 'event_time',         // datetime column name
    yAxis: 'value',              // numeric column name (or array for multi-series)
    yAxisLabel: 'Events/s',      // optional axis label
    temporalBinding: 'axis-bound',
    timeWindow: 60,              // keep last N seconds visible
    maxDataPoints: 500,
    colors: ['#7c6af7', '#4fc3f7'],  // optional custom colors
    smooth: true,                // smooth line
    showArea: false,             // fill under line
  }}
  data={{ columns, data: rows, isStreaming: true }}
  theme="dark"
/>
```

### BarColumnConfig

```typescript
<StreamChart
  config={{
    chartType: 'bar',            // 'bar' = horizontal, 'column' = vertical
    xAxis: 'category',
    yAxis: 'count',
    temporalBinding: 'frame-bound',
    maxDataPoints: 20,
    sortBy: 'value',             // sort bars by value
    sortOrder: 'desc',
  }}
  data={{ columns, data: rows, isStreaming: true }}
  theme="dark"
/>
```

### ScatterConfig

```typescript
<StreamChart
  config={{
    chartType: 'scatter',
    xAxis: 'latency_ms',
    yAxis: 'throughput',
    colorBy: 'service',          // color points by this column
    temporalBinding: 'axis-bound',
    maxDataPoints: 1000,
  }}
  data={{ columns, data: rows, isStreaming: true }}
  theme="dark"
/>
```

---

## SingleValueChart

Displays a single KPI metric.

```typescript
import { SingleValueChart } from '@timeplus/vistral';

<SingleValueChart
  config={{
    label: 'Events per second',
    unit: 'eps',
    precision: 1,
    trend: true,          // show up/down trend indicator
    sparkline: true,      // show mini sparkline below
  }}
  data={currentValue}     // number or string
  history={historyArray}  // optional: array of numbers for sparkline
  theme="dark"
/>
```

---

## DataTable

Renders streaming rows in a scrollable table.

```typescript
import { DataTable } from '@timeplus/vistral';

<DataTable
  config={{
    maxRows: 100,           // keep last N rows visible
    showTimestamp: true,    // prepend _tp_time column if present
    columns: ['col1', 'col2'],  // optional: show only these columns
    highlightNew: true,     // flash new rows
    sortBy: '_tp_time',
    sortOrder: 'desc',
  }}
  data={{ columns, data: rows }}
  theme="dark"
/>
```

---

## VistralChart (Low-Level Grammar API)

For complex custom visualizations that `StreamChart` doesn't cover.

```typescript
import { VistralChart } from '@timeplus/vistral';
import type { VistralSpec } from '@timeplus/vistral';

const spec: VistralSpec = {
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
    mode: 'axis-bound',
    timeField: 'ts',
    windowSeconds: 120,
  },
};

<VistralChart
  spec={spec}
  source={{ columns, data: rows, isStreaming: true }}
  theme="dark"
/>
```

---

## useStreamingData Hook

Manages a bounded streaming buffer in React state.

```typescript
import { useStreamingData } from '@timeplus/vistral';

const { data, append, clear, replace } = useStreamingData(
  initialData,   // DataRow[]
  maxItems       // max buffer size, default 1000
);

// append new rows
append(newRows);

// replace entire dataset (for frame-bound)
replace(latestSnapshot);

// clear all data
clear();
```

---

## Color Palettes

```typescript
import { multiColorPalettes, singleColorPalettes, findPaletteByLabel } from '@timeplus/vistral';

// Multi-color: 'Dawn', 'Morning', 'Midnight', 'Ocean', 'Sunset'
const palette = findPaletteByLabel('Midnight');
// palette.values = ['#7c6af7', '#4fc3f7', ...]

// Single-color ramps: 'purple', 'blue', 'cyan', 'green', etc.
```

Recommended palette for Timeplus apps: **Midnight** (matches the dark purple brand).

---

## Themes

Always use `theme="dark"` for Timeplus-branded applications. The dark theme uses:
- Background: `#1e2235`
- Axis/grid: muted purple-gray
- Default palette: Midnight

---

## Peer Dependencies

```json
{
  "react": ">=18.0.0",
  "react-dom": ">=18.0.0"
}
```

AntV G2 is bundled with Vistral — do not install it separately.
