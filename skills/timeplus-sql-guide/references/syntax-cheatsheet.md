# Timeplus SQL Syntax Cheatsheet

## Stream Operations
| Operation | Syntax |
|-----------|--------|
| Create stream | `CREATE STREAM name (col type, ...) SETTINGS ...` |
| Drop stream | `DROP STREAM IF EXISTS name` |
| Insert | `INSERT INTO name (cols) VALUES (vals)` |

## Time Windows
| Window | Syntax | Description |
|--------|--------|-------------|
| Tumble | `tumble(stream, interval)` | Fixed non-overlapping |
| Hop | `hop(stream, step, size)` | Fixed overlapping |
| Session | `session(stream, timeout)` | Gap-based |

## Query Modes
| Mode | Syntax | Description |
|------|--------|-------------|
| Streaming | `SELECT FROM stream` | Continuous results |
| Historical | `SELECT FROM table(stream)` | Batch query |

## Common Settings
- `SETTINGS seek_to='latest'` - Start from latest data
- `SETTINGS seek_to='earliest'` - Start from beginning
