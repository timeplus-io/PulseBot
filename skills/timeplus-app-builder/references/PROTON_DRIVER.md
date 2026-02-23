# Proton Query Proxy Reference

## Overview

PulseBot's agent server exposes a proxy endpoint that forwards SQL queries to Timeplus Proton and streams results back. Using this proxy is **required** for browser-based apps — it avoids CORS issues and centralises auth.

```
POST http://localhost:8001/query
Content-Type: application/json

SELECT * FROM my_stream
```

Results stream back as **newline-delimited JSON** (`JSONEachRow` format): one JSON object per row, flushed as data arrives.

---

## Request Format

```typescript
const response = await fetch('http://localhost:8001/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: 'SELECT * FROM my_stream',
});
```

---

## Reading the Streaming Response

The response body is a readable stream. Read it incrementally:

```typescript
const reader = response.body!.getReader();
const decoder = new TextDecoder();
let buffer = '';

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  buffer += decoder.decode(value, { stream: true });
  const lines = buffer.split('\n');
  buffer = lines.pop() ?? '';   // last partial line stays in buffer

  for (const line of lines) {
    if (!line.trim()) continue;
    const row = JSON.parse(line);
    // handle row...
  }
}
```

---

## Cancellation

Use an `AbortController` to stop a streaming query when the React component unmounts:

```typescript
const ctrl = new AbortController();
const res = await fetch('http://localhost:8001/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: sql,
  signal: ctrl.signal,
});

// Cancel:
ctrl.abort();
```

---

## Error Handling

Non-200 responses carry Proton's error message in the body:

```typescript
if (!response.ok) {
  const msg = await response.text();
  throw new Error(`Query failed (${response.status}): ${msg}`);
}
```

Common errors:
| HTTP status | Meaning |
|-------------|---------|
| 400 | Bad SQL — syntax error or unknown stream |
| 404 | Proxy endpoint not found — check agent server is running |
| 500 | Proton internal error — check Proton logs |

---

## Row Format

Each line is a JSON object matching the query's SELECT columns:

```json
{"event_time":"2024-01-15T10:23:45.123Z","device_id":"sensor-42","value":98.7}
{"event_time":"2024-01-15T10:23:45.456Z","device_id":"sensor-07","value":12.1}
```

Column types in JSON:
| Proton type | JSON representation |
|-------------|---------------------|
| `int*`, `uint*`, `float*` | `number` |
| `string`, `fixed_string` | `string` |
| `datetime`, `datetime64` | `string` (ISO 8601) |
| `array(T)` | `array` |
| `nullable(T)` | value or `null` |

---

## Inferring Column Definitions for Vistral

Vistral's `StreamChart` needs a `columns` array with `name` and `type`. Infer these from the first received row:

```typescript
function inferColumns(row: Record<string, unknown>) {
  return Object.entries(row).map(([name, value]) => ({
    name,
    type: typeof value === 'number' ? 'float64'
        : String(value).match(/^\d{4}-\d{2}-\d{2}/) ? 'datetime64'
        : 'string',
  }));
}
```
