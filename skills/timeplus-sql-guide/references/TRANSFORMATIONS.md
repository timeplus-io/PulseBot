# Data Transformations in Timeplus

## Streaming vs Historical Mode

```sql
-- STREAMING (continuous, default): query never ends, emits results as events arrive
SELECT device_id, avg(temperature) FROM sensor_data GROUP BY device_id;

-- HISTORICAL (bounded): wraps stream in table(), returns immediately
SELECT device_id, avg(temperature) FROM table(sensor_data) GROUP BY device_id;

-- ALL DATA (past + future): use earliest_timestamp()
SELECT * FROM sensor_data WHERE _tp_time >= earliest_timestamp();
```

---

## Window Functions

Windows are the primary mechanism for time-based aggregation over streams.

### Tumble (fixed, non-overlapping)

```sql
-- Count events per 5-minute window per device
SELECT
    window_start,
    window_end,
    device_id,
    count()     AS event_count,
    avg(temperature) AS avg_temp,
    max(temperature) AS max_temp
FROM tumble(sensor_data, 5m)
GROUP BY window_start, window_end, device_id;
```

Time shorthand: `5s`, `2m`, `3h`, `1d`.
Full syntax: `tumble(stream, INTERVAL 5 MINUTE)`.

### Hop (sliding, overlapping windows)

```sql
-- 30-second window sliding every 5 seconds
SELECT
    window_start,
    count() AS event_count
FROM hop(sensor_data, 5s, 30s)
GROUP BY window_start;
```

Syntax: `hop(stream, slide_interval, window_size)`.

### Session (dynamic, activity-gap based)

```sql
-- Session ends after 1 minute of inactivity per device
SELECT
    device_id,
    window_start,
    window_end,
    count()         AS events_in_session,
    max(temperature) AS peak_temp
FROM session(sensor_data, 1m) PARTITION BY device_id
GROUP BY device_id, window_start, window_end;
```

**Session with start/end conditions:**
```sql
-- Session starts when speed > 50, ends when speed < 10
SELECT trip_id, window_start, window_end, count()
FROM session(car_events, 5m, [speed > 50, speed < 10]) PARTITION BY trip_id
GROUP BY trip_id, window_start, window_end;
```

### EMIT Policies

Control when window results are emitted:

```sql
-- Emit after watermark passes window_end (default for tumble/hop)
SELECT window_start, count() FROM tumble(orders, 1m)
GROUP BY window_start
EMIT AFTER WATERMARK;

-- Wait 5s after watermark for late events
SELECT window_start, sum(amount) FROM tumble(orders, 1m)
GROUP BY window_start
EMIT AFTER WATERMARK AND DELAY 5s;

-- Emit incrementally on every update (for real-time dashboards)
SELECT device_id, avg(temperature) FROM sensor_data
GROUP BY device_id
EMIT ON UPDATE;

-- Start from 2 hours ago (backfill)
SELECT window_start, count() FROM tumble(events, 5m)
GROUP BY window_start
EMIT LAST 2h;
```

---

## Aggregations (Streaming and Historical)

### Basic Aggregations
```sql
SELECT
    region,
    count()              AS total_orders,
    count_distinct(user_id) AS unique_users,
    sum(amount)          AS revenue,
    avg(amount)          AS avg_order_value,
    min(amount)          AS min_order,
    max(amount)          AS max_order,
    median(amount)       AS median_order
FROM table(orders)
GROUP BY region;
```

### Percentile & Top-K
```sql
SELECT
    p90(response_time)    AS p90,
    p95(response_time)    AS p95,
    p99(response_time)    AS p99,
    quantile(response_time, 0.999) AS p999,
    top_k(error_code, 5)  AS top_errors,
    min_k(response_time, 3) AS fastest_3
FROM table(api_logs)
GROUP BY endpoint;
```

### Distinct & Array Aggregations
```sql
SELECT
    user_id,
    unique(product_id)         AS distinct_products_exact,
    group_array(product_id)    AS all_products,
    group_concat(tag, ', ')    AS tags_list
FROM table(user_events)
GROUP BY user_id;
```

### First/Last Values
```sql
SELECT
    device_id,
    first_value(temperature) AS first_reading,
    last_value(temperature)  AS latest_reading,
    arg_min(temperature, ts) AS coldest_at,
    arg_max(temperature, ts) AS hottest_at
FROM table(sensor_data)
GROUP BY device_id;
```

---

## JOINs

### Stream-to-Dimension Lookup (Append + Versioned KV)

```sql
-- Enrich streaming orders with current product dimensions
SELECT
    o._tp_time,
    o.order_id,
    o.product_id,
    p.name     AS product_name,
    p.category AS category,
    p.price * o.quantity AS revenue
FROM orders AS o
JOIN products AS p ON o.product_id = p.product_id;
-- 'products' must be versioned_kv or mutable stream
```

### ASOF JOIN (Time-versioned Lookup)

Match each event with the most recent prior row in the right table:

```sql
SELECT
    o.order_id,
    o.amount,
    p.price AS price_at_time_of_order
FROM orders AS o
ASOF JOIN price_history AS p
  ON o.product_id = p.product_id
  AND o._tp_time >= p._tp_time;
```

### Range / Bidirectional Stream-to-Stream JOIN

Join two streams within a time window:

```sql
SELECT
    clicks.user_id,
    clicks.url,
    purchases.amount
FROM clicks
INNER JOIN purchases
  ON clicks.user_id = purchases.user_id
  AND date_diff_within(10m, clicks._tp_time, purchases._tp_time);
```

### CROSS JOIN with table()

```sql
-- Cross join a stream with a static lookup table
SELECT e.device_id, e.temperature, t.threshold
FROM sensor_data AS e
CROSS JOIN table(device_thresholds) AS t
WHERE e.device_id = t.device_id;
```

### LEFT JOIN / RIGHT JOIN / FULL JOIN

Standard SQL semantics apply when joining streams with `table()` references.

---

## CTEs (Common Table Expressions)

```sql
-- Filter then aggregate
WITH high_temp_events AS (
    SELECT device_id, temperature, location
    FROM sensor_data
    WHERE temperature > 35
),
alert_summary AS (
    SELECT location, count() AS alert_count, max(temperature) AS peak
    FROM high_temp_events
    GROUP BY location
)
SELECT * FROM alert_summary
ORDER BY alert_count DESC;
```

---

## Subqueries

```sql
-- Find devices above their average
SELECT device_id, temperature
FROM sensor_data
WHERE temperature > (
    SELECT avg(temperature)
    FROM table(sensor_data)
);
```

---

## Deduplication

```sql
-- Deduplicate by event_id within a 10-second window
SELECT * FROM dedup(sensor_data, event_id, 10s);

-- Deduplicate historical data
SELECT DISTINCT device_id, temperature FROM table(sensor_data);
```

---

## Changelog Streaming

Convert append stream to changelog for diff-based processing:

```sql
-- Produces (+1/-1 delta rows) as the aggregate updates
SELECT * FROM changelog(
    SELECT device_id, count() AS cnt FROM sensor_data GROUP BY device_id
);
```

---

## Materialized Views (Continuous Pipelines)

Materialized views are the backbone of stream processing pipelines.
They run continuously, checkpoint state, and write to a target stream.

### Basic Pipeline

```sql
-- Step 1: Create target stream
CREATE STREAM IF NOT EXISTS revenue_5m (
    window_start datetime64(3),
    region       string,
    total_revenue float64
);

-- Step 2: Create materialized view
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_revenue_5m
INTO revenue_5m AS
SELECT
    window_start,
    region,
    sum(amount) AS total_revenue
FROM tumble(orders, 5m)
GROUP BY window_start, region;
```

### Enrichment Pipeline (with JOIN)

```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_enriched_orders
INTO enriched_orders AS
SELECT
    o._tp_time,
    o.order_id,
    o.amount,
    p.name      AS product_name,
    p.category  AS category,
    u.email     AS user_email
FROM orders AS o
JOIN products AS p ON o.product_id = p.product_id
JOIN users AS u    ON o.user_id    = u.user_id;
```

### Kafka-to-Kafka Pipeline (ETL)

```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_kafka_etl
INTO kafka_output_stream AS  -- kafka external stream as target
SELECT
    raw:user_id           AS user_id,
    raw:event_type        AS event_type,
    now64(3)              AS processed_at,
    lower(hex(md5(raw:ip))) AS masked_ip
FROM kafka_input_stream;
```

### Manage Materialized Views

```sql
-- List views
SHOW VIEWS;

-- Drop a view
DROP VIEW IF EXISTS mv_revenue_5m;

-- Pause / resume
SYSTEM SUSPEND mv_revenue_5m;
SYSTEM RESUME  mv_revenue_5m;
```

---

## Views (Non-materialized)

Views are saved queries — re-evaluated each time they are queried.

```sql
CREATE VIEW IF NOT EXISTS high_temp_sensors AS
SELECT device_id, temperature, location
FROM sensor_data
WHERE temperature > 30;

-- Query the view
SELECT * FROM table(high_temp_sensors) LIMIT 100;
```

---

## Streaming Enrichment Functions

```sql
-- Lag: access previous row value
SELECT device_id, temperature,
       lag(temperature)  AS prev_temp,
       temperature - lag(temperature) AS delta
FROM sensor_data;

-- Latest: get most recent value from a versioned stream
SELECT device_id, latest(price) FROM price_stream;

-- Emit version: monotonically increasing version per window
SELECT window_start, emit_version(), count()
FROM tumble(events, 1m) GROUP BY window_start;
```

---

## Query Settings

Add `SETTINGS key=value` at the end of any query:

```sql
SELECT * FROM events
SETTINGS
    seek_to                           = 'earliest',   -- or timestamp, or '-2h'
    enable_backfill_from_historical_store = 1,
    replay_speed                      = 0,            -- 0=max, 1=real-time
    default_hash_table                = 'hybrid';     -- spill to disk
```
