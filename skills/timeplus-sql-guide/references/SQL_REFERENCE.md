# Timeplus SQL Reference

## Data Types

### Numeric

| Type | Range | Notes |
|------|-------|-------|
| `int8` / `uint8` | -128..127 / 0..255 | 1 byte |
| `int16` / `uint16` | -32768..32767 / 0..65535 | 2 bytes |
| `int32` / `uint32` | ±2B / 0..4B | 4 bytes |
| `int64` / `uint64` | ±9.2×10¹⁸ / 0..1.8×10¹⁹ | 8 bytes |
| `int128` / `uint128` | | 16 bytes |
| `int256` / `uint256` | | 32 bytes |
| `float32` | ~7 decimal digits | 4 bytes |
| `float64` | ~15 decimal digits | 8 bytes |
| `decimal(P, S)` | Precision P, Scale S | Fixed-point |
| `decimal32(S)` | P≤9 | 4 bytes |
| `decimal64(S)` | P≤18 | 8 bytes |
| `decimal128(S)` | P≤38 | 16 bytes |

### String

| Type | Notes |
|------|-------|
| `string` | UTF-8, variable length |
| `fixed_string(N)` | Exactly N bytes |

### DateTime

| Type | Notes |
|------|-------|
| `date` | YYYY-MM-DD, 2-byte |
| `date32` | Extended range date |
| `datetime` | Unix timestamp, second precision |
| `datetime64(scale)` | Subsecond. Scale: 0=s,3=ms,6=µs,9=ns |
| `datetime64(scale, 'tz')` | With timezone, e.g. `datetime64(3, 'UTC')` |

Default event-time column `_tp_time` is `datetime64(3, 'UTC')`.

### Compound / Complex

| Type | Example | Notes |
|------|---------|-------|
| `array(T)` | `array(string)` | Dynamic array |
| `map(K, V)` | `map(string, float32)` | Key-value map |
| `tuple(T1, T2, ...)` | `tuple(string, int32)` | Fixed structure |
| `nullable(T)` | `nullable(string)` | Allows NULL |
| `json` | `json` | Semi-structured (Enterprise 2.9+) |

### Other

| Type | Notes |
|------|-------|
| `bool` | true/false |
| `uuid` | UUID string |
| `ipv4` | 4-byte IPv4 |
| `ipv6` | 16-byte IPv6 |
| `enum('a','b','c')` | Enumerated string |
| `enum8(...)` / `enum16(...)` | With explicit values |
| `low_cardinality(T)` | Optimized for repeated values |

---

## Type Conversion

```sql
-- Explicit cast
SELECT cast(temperature, 'int32')   AS temp_int;
SELECT cast('2025-01-01', 'date')   AS d;

-- :: shorthand
SELECT temperature::int32           AS temp_int;
SELECT '2025-01-01'::date           AS d;

-- to_* functions
SELECT to_int32(temperature)        AS temp_int;
SELECT to_float32('23.5')           AS temp;
SELECT to_string(temperature)       AS temp_str;
SELECT to_date('2025-01-01')        AS d;
SELECT to_datetime('2025-01-01 00:00:00') AS dt;
SELECT to_datetime64('2025-01-01T00:00:00.000', 3, 'UTC') AS dt64;
SELECT to_decimal64('123.45', 2)    AS dec;
```

---

## All DDL Statements

### Streams

```sql
-- Create
CREATE STREAM [IF NOT EXISTS] name (col type [DEFAULT expr], ...)
    [PRIMARY KEY (col, ...)]
    [TTL expr]
    [SETTINGS key=value, ...];

CREATE MUTABLE STREAM [IF NOT EXISTS] name (col type, ...)
    [PRIMARY KEY (col, ...)]
    [INDEX name (col) UNIQUE]
    SETTINGS ttl_seconds = N;

CREATE EXTERNAL STREAM [IF NOT EXISTS] name (col type, ...)
    SETTINGS type='kafka'|'pulsar'|'timeplus', ...;

CREATE RANDOM STREAM [IF NOT EXISTS] name (col type DEFAULT expr, ...)
    SETTINGS eps=N, interval_time=N;

-- Modify
ALTER STREAM name ADD COLUMN col type;
ALTER STREAM name DROP COLUMN col;
ALTER STREAM name MODIFY COLUMN col type;
ALTER STREAM name RENAME COLUMN old TO new;
ALTER STREAM name MODIFY TTL expr;

-- Delete
DROP STREAM [IF EXISTS] name;

-- Inspect
SHOW STREAMS;
DESCRIBE name;
```

### Views

```sql
CREATE VIEW [IF NOT EXISTS] name AS SELECT ...;
CREATE MATERIALIZED VIEW [IF NOT EXISTS] name [INTO target_stream] AS SELECT ...;

DROP VIEW [IF EXISTS] name;
DROP VIEW [IF EXISTS] name ON CLUSTER cluster;

SHOW VIEWS;
SHOW CREATE VIEW name;

-- Pause / resume materialized view
SYSTEM SUSPEND view_name;
SYSTEM RESUME view_name;
```

### Functions

```sql
-- SQL lambda UDF
CREATE [OR REPLACE] FUNCTION name AS (param1, param2, ...) -> expression;

-- JavaScript UDF
CREATE [OR REPLACE] FUNCTION name(param type, ...)
RETURNS return_type
LANGUAGE JAVASCRIPT AS $$ ... $$;

-- JavaScript UDAF
CREATE AGGREGATE FUNCTION name(param type)
RETURNS return_type
LANGUAGE JAVASCRIPT AS $$ { initialize, process, finalize, serialize, deserialize, merge } $$;

-- Python UDF (Enterprise)
CREATE [OR REPLACE] FUNCTION name(param type, ...)
RETURNS return_type
LANGUAGE PYTHON AS $$ ... $$;

-- Remote UDF
CREATE REMOTE FUNCTION name(param type, ...)
RETURNS return_type
URL 'https://...'
[AUTH_METHOD 'auth_header']
[AUTH_HEADER 'Authorization']
[AUTH_KEY 'Bearer ...']
[EXECUTION_TIMEOUT ms];

DROP FUNCTION [IF EXISTS] name;
SHOW FUNCTIONS;
```

### Other DDL

```sql
-- External table
CREATE EXTERNAL TABLE [IF NOT EXISTS] name SETTINGS type='clickhouse'|..., ...;
DROP TABLE [IF EXISTS] name;

-- Named collection (reusable credentials)
CREATE NAMED COLLECTION my_kafka AS
    brokers='kafka:9092', data_format='JSONEachRow';

-- Format schema (Protobuf/Avro)
CREATE FORMAT SCHEMA my_schema TYPE Protobuf AS '...';
```

---

## DML Statements

```sql
-- Insert
INSERT INTO stream [(col1, col2, ...)] VALUES (v1, v2), ...;
INSERT INTO stream SELECT ... FROM ...;

-- Delete (mutable streams only)
DELETE FROM stream WHERE condition;

-- Update (mutable streams only — use INSERT for KV modes)
-- Versioned KV: just INSERT, it replaces the old row for that key
INSERT INTO versioned_stream VALUES ('key', 'new_value', now64(3));
```

---

## SELECT Syntax

```sql
SELECT [DISTINCT]
    expr [AS alias], ...
FROM stream_or_table
    [JOIN ... ON ...]
    [ASOF JOIN ... ON ...]
[WHERE condition]
[GROUP BY expr, ...]
[HAVING condition]
[ORDER BY expr [ASC|DESC], ...]  -- only for historical queries
[LIMIT n]
[OFFSET n]
[SETTINGS key=value, ...]
[EMIT ...]
```

**EXPLAIN:**
```sql
EXPLAIN SELECT ...;
EXPLAIN AST SELECT ...;
EXPLAIN SYNTAX SELECT ...;
EXPLAIN PLAN SELECT ...;
EXPLAIN PIPELINE SELECT ...;
```

---

## Streaming-Specific Functions

| Function | Description |
|----------|-------------|
| `table(stream)` | Query stream as historical table |
| `tumble(stream, interval)` | Fixed-size window |
| `hop(stream, slide, size)` | Sliding window |
| `session(stream, gap) PARTITION BY col` | Session window |
| `dedup(stream, col, window)` | Deduplicate by column |
| `changelog(subquery)` | Produce changelog from aggregation |
| `lag(col)` / `lag(col, N)` | Previous row value |
| `latest(col)` | Most recent value |
| `earliest(col)` | Earliest value |
| `emit_version()` | Monotonic window version |
| `date_diff_within(interval, t1, t2)` | Time proximity check for JOINs |
| `earliest_timestamp()` | Minimum possible _tp_time |
| `now64(3, 'UTC')` | Current time as datetime64(3) |
| `now()` | Current time as datetime |
| `today()` | Current date |

---

## Aggregation Functions (Full List)

**Basic:** `count()`, `count_distinct(col)`, `sum(col)`, `avg(col)`, `min(col)`, `max(col)`

**Statistical:** `median(col)`, `var_pop(col)`, `var_samp(col)`, `std_pop(col)`, `std_samp(col)`, `covar_pop(x,y)`, `corr(x,y)`

**Percentile:** `quantile(col, level)`, `quantiles(col, l1, l2, ...)`, `p90(col)`, `p95(col)`, `p99(col)`

**Time-weighted:** `avg_time_weighted(val, time)`, `sum_time_weighted(val, time)`

**Top-K / Bottom-K:** `top_k(col, K)`, `min_k(col, K)`, `max_k(col, K)`, `arg_min(val, by)`, `arg_max(val, by)`

**Array:** `group_array(col)`, `group_concat(col, sep)`, `group_array_sorted_arr(col, sort_col, limit)`

**Cardinality:** `unique(col)` (HLL, approx), `unique_exact(col)` (exact)

**First/Last:** `first_value(col)`, `last_value(col)`, `any(col)`, `any_last(col)`

**Histogram:** `histogram(N)(col)` → array of (lower, upper, height) tuples

**ML:** `stochastic_linear_regression_state(...)`, `stochastic_logistic_regression_state(...)`

---

## Math Functions

`abs(x)`, `sign(x)`, `floor(x)`, `ceil(x)`, `round(x, N)`, `round_to_exp2(x)`, `sqrt(x)`, `cbrt(x)`, `exp(x)`, `exp2(x)`, `log(x)`, `log2(x)`, `log10(x)`, `pow(x, y)`, `sin(x)`, `cos(x)`, `tan(x)`, `asin(x)`, `acos(x)`, `atan(x)`, `atan2(y, x)`, `hypot(x, y)`, `gcd(a, b)`, `lcm(a, b)`, `pi()`, `e()`, `inf()`, `nan()`

---

## String Functions

`length(s)`, `char_length(s)`, `lower(s)`, `upper(s)`, `reverse(s)`, `trim(s)`, `ltrim(s)`, `rtrim(s)`, `concat(s1, s2, ...)`, `s1 || s2`, `substring(s, offset, length)`, `left(s, N)`, `right(s, N)`, `starts_with(s, prefix)`, `ends_with(s, suffix)`, `contains(haystack, needle)`, `position(haystack, needle)`, `replace(s, from, to)`, `replace_all(s, from, to)`, `replace_regex(s, pattern, replacement)`, `match(s, regex)`, `extract(s, regex)`, `split_by_string(sep, s)`, `split_by_char(sep, s)`, `array_string_concat(arr, sep)`, `hex(s)`, `unhex(s)`, `md5(s)`, `sha256(s)`, `base64_encode(s)`, `base64_decode(s)`, `to_string(x)`, `format(fmt, args...)`, `char(N)`, `encode(s, 'UTF-8')`, `grok(s, pattern)` → map

---

## DateTime Functions

```sql
now()                          -- current datetime
now64(3, 'UTC')                -- current datetime64(3)
today()                        -- current date
yesterday()                    -- yesterday's date
to_date('2025-01-15')          -- parse date
to_datetime('2025-01-15 12:00:00')
parse_datetime_best_effort(s)  -- flexible parse

date_trunc('hour', dt)         -- truncate to hour/day/month/etc
date_diff('second', t1, t2)    -- difference in units
date_add(dt, INTERVAL 1 DAY)
date_sub(dt, INTERVAL 2 HOUR)
to_timezone(dt, 'America/New_York')

to_year(dt), to_month(dt), to_day(dt)
to_hour(dt), to_minute(dt), to_second(dt)
to_day_of_week(dt)             -- 1=Monday
to_unix_timestamp(dt)
from_unix_timestamp(N)
to_start_of_minute(dt)
to_start_of_hour(dt)
to_start_of_day(dt)
to_start_of_week(dt)
to_start_of_month(dt)
to_start_of_quarter(dt)
to_start_of_year(dt)
format_datetime(dt, '%Y-%m-%d %H:%M:%S')
```

---

## JSON Functions

```sql
-- Shorthand path extraction (preferred)
SELECT raw:user_id,             -- extract field as string
       raw:amount::float32,     -- extract and cast
       raw:address.city         -- nested path
FROM kafka_events;

-- Explicit functions
json_extract_string(json_col, 'path')   -- → string
json_extract_int(json_col, 'path')      -- → int64
json_extract_float(json_col, 'path')    -- → float64
json_extract_bool(json_col, 'path')     -- → bool
json_extract_array(json_col, 'path')    -- → array(string)
json_extract_keys(json_col)             -- → array(string)
json_extract_raw(json_col, 'path')      -- → raw JSON string
is_valid_json(s)                        -- → bool
to_json(map_or_tuple)                   -- → string
```

---

## Conditional Functions

```sql
if(cond, then, else)
multi_if(c1, r1, c2, r2, ..., else)   -- CASE shorthand
CASE WHEN c1 THEN r1 WHEN c2 THEN r2 ELSE r3 END
coalesce(a, b, c, ...)                 -- first non-NULL
null_if(a, b)                          -- NULL if a == b
if_null(a, b)                          -- b if a is NULL
is_null(a)                             -- bool
is_not_null(a)
in(x, (v1, v2, ...))
not_in(x, (v1, v2, ...))
```

---

## Array Functions

`array(v1, v2)`, `[v1, v2]`, `length(arr)`, `has(arr, el)`, `has_any(arr, arr2)`, `has_all(arr, arr2)`, `index_of(arr, el)`, `array_element(arr, N)`, `arr[N]`, `reverse(arr)`, `sort(arr)`, `flatten(arr)`, `array_union(a, b)`, `array_intersect(a, b)`, `array_difference(arr)`, `array_distinct(arr)`, `array_map(func, arr)`, `array_filter(func, arr)`, `array_reduce(func, arr)`, `array_count(arr)`, `array_sum(arr)`, `array_avg(arr)`, `range(start, stop, step)`, `empty(arr)`, `not_empty(arr)`, `array_compact(arr)`

---

## IP & Geo Functions

`to_ipv4(s)`, `to_ipv6(s)`, `ipv4_to_string(ip)`, `ipv6_to_string(ip)`, `ipv4_num_to_string(N)`, `ipv4_string_to_num(s)`, `ipv4_cidr_to_range(ip, cidr)`, `is_ipv4_string(s)`, `is_ipv6_string(s)`, `geo_distance(lat1, lon1, lat2, lon2)`, `great_circle_distance(lat1, lon1, lat2, lon2)`

---

## Hash & Encoding Functions

`md5(s)` → string, `sha1(s)`, `sha256(s)`, `sha512(s)`, `hex(s)`, `unhex(s)`, `base64_encode(s)`, `base64_decode(s)`, `city_hash64(s)`, `sipHash64(s)`, `murmurhash64(s)`, `xxHash64(s)`, `farmHash64(s)`, `uuid()` → random UUID, `generate_uuid_v4()`

---

## Query Settings Reference

```sql
SELECT ... SETTINGS
    -- Seek position for streaming queries
    seek_to = 'latest'                       -- default
    seek_to = 'earliest'                     -- from beginning
    seek_to = '2025-01-01T00:00:00.000'      -- specific time
    seek_to = '-2h'                          -- relative

    -- Mode
    query_mode = 'streaming'                 -- or 'table'

    -- Backfill historical data then continue streaming
    enable_backfill_from_historical_store = 1

    -- Replay historical data at controlled speed
    replay_speed = 1                         -- 1=real-time, 0=max speed

    -- Memory management
    default_hash_table = 'memory'            -- or 'hybrid' (spill to disk)
    max_bytes_before_external_group_by = 1073741824

    -- JOIN
    join_algorithm = 'default'               -- 'hash', 'direct', 'auto'

    -- Kafka-specific
    shards = '0,2'                           -- specific partitions

    -- Fault tolerance
    recovery_policy = 'strict'               -- or 'best_effort'
```
