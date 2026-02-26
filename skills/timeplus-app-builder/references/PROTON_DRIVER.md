# Proton JavaScript Driver Reference

## Package & CDN

npm: `@timeplus/proton-javascript-driver`  
GitHub: https://github.com/timeplus-io/proton-javascript-driver

**UMD import (use this in HTML apps — no npm required):**
```html
<script src="https://unpkg.com/@timeplus/proton-javascript-driver/dist/index.umd.js"></script>
```

This exposes `window.ProtonDriver`. Destructure it:
```javascript
const { ProtonClient } = window.ProtonDriver;
```

---

## Overview

`@timeplus/proton-javascript-driver` is a streaming REST client for Timeplus Proton. It connects to Proton's HTTP port and returns rows as an async iterable — one JavaScript object per row, streamed as data arrives.

In the agent context, a proxy to Proton is already running at `localhost:8001`. Always use this host and port — do not connect to Proton's raw port directly.

---

## Creating a Client

```javascript
const client = new ProtonClient({
  host: 'localhost',  // agent proxy host
  port: 8001,         // agent proxy port
  // username: 'default',  // optional
  // password: '',         // optional
  // timeout: 30000,       // optional connection timeout ms
});
```

### Configuration options

```
ProtonConfig {
  host?:     string   // default: 'localhost'
  port?:     number   // default: 3218  — always override to 8001 for agent use
  username?: string
  password?: string
  timeout?:  number   // connection timeout in milliseconds
}
```

---

## Running a Query

```javascript
const { rows, abort } = await client.query('SELECT * FROM my_stream');
```

Returns:
- `rows` — `AsyncIterableIterator<T>` — yields one object per result row
- `abort()` — function to cancel the query immediately

### Consuming rows

```javascript
for await (const row of rows) {
  // row is a plain object: { col1: val1, col2: val2, ... }
  console.log(row);
}
```

### With an AbortSignal

```javascript
const { rows, abort } = await client.query(sql, { signal: myAbortSignal });
```

### Cancellation

```javascript
const { rows, abort } = await client.query('SELECT * FROM my_stream');

// Cancel after 10 seconds
setTimeout(abort, 10000);

for await (const row of rows) {
  // loop exits cleanly when abort() is called
}
```

---

## Streaming vs Historical Queries

Both query types use the same `client.query()` API:

| Query type | SQL pattern | Behaviour |
|-----------|-------------|-----------|
| **Streaming** | `SELECT ... FROM stream_name` | Runs forever, emits rows as they arrive |
| **Historical** | `SELECT ... FROM table(stream_name)` | Returns past data then terminates |
| **Hybrid** | `SELECT ... FROM stream_name WHERE _tp_time > now() - 5m` | Backfills then continues streaming |

---

## Row Format

Each row is a plain JavaScript object keyed by column name:

```javascript
// Example row from sensor_stream
{ event_time: '2024-01-15T10:23:45.123Z', device_id: 'sensor-42', value: 98.7 }
```

Column type mapping from Proton:

| Proton type | JavaScript representation |
|-------------|--------------------------|
| `int*`, `uint*`, `float*` | `number` |
| `string`, `fixed_string` | `string` |
| `datetime`, `datetime64` | `string` (ISO 8601) |
| `array(T)` | `Array` |
| `nullable(T)` | value or `null` |

---

## Inferring Column Definitions for Vistral

Vistral's `StreamChart` needs a `columns` array with `name` and `type`. Infer these from the first received row:

```javascript
function inferColumns(row) {
  return Object.entries(row).map(([name, value]) => ({
    name,
    type: typeof value === 'number' ? 'float64'
        : String(value).match(/^\d{4}-\d{2}-\d{2}/) ? 'datetime64'
        : 'string',
  }));
}

let columns = [];
for await (const row of rows) {
  if (columns.length === 0) columns = inferColumns(row);
  // ... process row
}
```

---

## Low-Level: `ndjsonStreamParser`

For custom streaming needs, the driver also exports a low-level NDJSON parser:

```javascript
const { ndjsonStreamParser } = window.ProtonDriver;

const response = await fetch('http://localhost:8001/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: sql }),
});

const reader = response.body.getReader();
for await (const row of ndjsonStreamParser(reader)) {
  console.log(row);
}
```

---

## Error Handling

```javascript
try {
  const { rows, abort } = await client.query(sql);
  for await (const row of rows) {
    // process row
  }
} catch (err) {
  // Connection errors, SQL syntax errors, etc.
  console.error('Query failed:', err.message);
}
```

Common errors:

| Error | Likely cause |
|-------|-------------|
| `Failed to connect` | Proton proxy not running at localhost:8001 |
| `Bad SQL` / `Unknown stream` | SQL syntax error or stream doesn't exist |
| `AbortError` | Query was cancelled via `abort()` |

---

## Full Example (in HTML)

```html
<script src="https://unpkg.com/@timeplus/proton-javascript-driver/dist/index.umd.js"></script>
<script>
  const { ProtonClient } = window.ProtonDriver;

  const client = new ProtonClient({ host: 'localhost', port: 8001 });

  async function streamData() {
    try {
      const { rows, abort } = await client.query(
        'SELECT device_id, value, _tp_time FROM sensor_stream'
      );

      // Store abort so we can cancel later
      window.stopQuery = abort;

      for await (const row of rows) {
        console.log(row.device_id, row.value, row._tp_time);
      }
    } catch (err) {
      console.error(err.message);
    }
  }

  streamData();
</script>
```
