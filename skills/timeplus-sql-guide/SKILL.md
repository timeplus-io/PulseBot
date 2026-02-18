---
name: timeplus-sql-guide
description: Guide for writing Timeplus streaming SQL queries including tumble windows, hop windows, table functions, and materialized views. Use this skill when the user asks about Timeplus SQL syntax or needs help writing streaming queries.
license: Apache-2.0
metadata:
  author: timeplus-io
  version: "1.0"
---

# Timeplus Streaming SQL Guide

## When to use this skill
Use this skill when the user wants to:
- Write streaming SQL queries for Timeplus/Proton
- Understand window functions (tumble, hop, session)
- Create materialized views
- Query historical data vs streaming data

## Streaming vs Historical Queries

- **Streaming query**: `SELECT ... FROM stream_name` - continuously returns new results
- **Historical query**: `SELECT ... FROM table(stream_name)` - queries existing data like a regular table

## Window Functions

### Tumble Window
Fixed-size, non-overlapping time windows:
```sql
SELECT window_start, window_end, count(*) as cnt
FROM tumble(stream_name, 5s)
GROUP BY window_start, window_end
```

### Hop Window
Fixed-size, overlapping windows:
```sql
SELECT window_start, window_end, avg(value) as avg_val
FROM hop(stream_name, 1s, 5s)
GROUP BY window_start, window_end
```

## Materialized Views

Create a materialized view for continuous aggregation:
```sql
CREATE MATERIALIZED VIEW mv_hourly_stats AS
SELECT window_start, count(*) as events
FROM tumble(events, 1h)
GROUP BY window_start
```

## Available References
- See references/syntax-cheatsheet.md for a quick syntax reference
