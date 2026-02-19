# Random Streams — Simulated Data in Timeplus

Random streams generate synthetic data continuously without any external source.
They are ideal for development, testing, demos, and load testing.

---

## Basic Syntax

```sql
CREATE RANDOM STREAM [IF NOT EXISTS] stream_name (
    column_name type DEFAULT expression,
    ...
)
SETTINGS
    eps           = N,      -- events per second (default: 1)
    interval_time = N;      -- emit interval in milliseconds (default: 100)
```

Every column **must** have a `DEFAULT` expression that generates random data.
The `_tp_time` column is automatically set to ingestion time.

---

## Random Generation Functions

| Function | Returns | Example |
|----------|---------|---------|
| `rand()` | uint32 (0..4294967295) | `rand() % 100` → 0..99 |
| `rand64()` | uint64 | `rand64()` |
| `rand_normal(mean, std)` | float64 | `rand_normal(20.0, 5.0)` |
| `random_printable_ascii(N)` | string (N printable chars) | `random_printable_ascii(8)` |
| `random_string(N)` | binary string of N bytes | `random_string(16)` |
| `random_fixed_string(N)` | fixed_string(N) | `random_fixed_string(4)` |
| `now64(3, 'UTC')` | current datetime64 | For timestamp columns |
| `uuid()` | random UUID string | Unique IDs |

---

## Practical Examples

### IoT Sensor Data

```sql
CREATE RANDOM STREAM IF NOT EXISTS iot_sensors (
    device_id   string   DEFAULT 'sensor-' || to_string(rand() % 50),
    location    string   DEFAULT ['warehouse-a','warehouse-b','rooftop','basement'][rand() % 4 + 1],
    temperature float32  DEFAULT round(rand_normal(22.0, 8.0)::float32, 1),
    humidity    float32  DEFAULT round(20 + (rand() % 60)::float32, 1),
    pressure    float32  DEFAULT round(1000 + (rand() % 50)::float32, 1),
    battery     uint8    DEFAULT (rand() % 101)::uint8,
    status      string   DEFAULT ['ok','warn','error','offline'][rand() % 4 + 1]
)
SETTINGS eps = 20;           -- 20 events per second
```

### E-Commerce Events

```sql
CREATE RANDOM STREAM IF NOT EXISTS ecommerce_events (
    event_id    string   DEFAULT random_printable_ascii(12),
    user_id     string   DEFAULT 'user-' || to_string(rand() % 10000),
    session_id  string   DEFAULT 'sess-' || to_string(rand() % 100000),
    event_type  string   DEFAULT ['page_view','add_to_cart','checkout','purchase','refund'][rand() % 5 + 1],
    product_id  string   DEFAULT 'prod-' || to_string(rand() % 500),
    category    string   DEFAULT ['electronics','clothing','food','books','sports'][rand() % 5 + 1],
    amount      float32  DEFAULT round((5 + (rand() % 495))::float32, 2),
    country     string   DEFAULT ['US','GB','DE','JP','BR','CA','FR'][rand() % 7 + 1]
)
SETTINGS eps = 50;
```

### Web Access Logs

```sql
CREATE RANDOM STREAM IF NOT EXISTS web_logs (
    ip          string   DEFAULT to_string(rand() % 256) || '.' || to_string(rand() % 256) || '.0.1',
    method      string   DEFAULT ['GET','POST','PUT','DELETE'][rand() % 4 + 1],
    path        string   DEFAULT ['/api/users','/api/orders','/api/products','/health','/login'][rand() % 5 + 1],
    status_code uint16   DEFAULT [200, 200, 200, 201, 400, 401, 403, 404, 500][rand() % 9 + 1],
    latency_ms  uint32   DEFAULT 10 + (rand() % 990),
    user_agent  string   DEFAULT ['Chrome/120','Firefox/121','Safari/17','curl/8.0'][rand() % 4 + 1]
)
SETTINGS eps = 100;
```

### Financial Trades

```sql
CREATE RANDOM STREAM IF NOT EXISTS trades (
    trade_id    string   DEFAULT uuid(),
    symbol      string   DEFAULT ['AAPL','GOOGL','MSFT','TSLA','AMZN','META','NVDA'][rand() % 7 + 1],
    side        string   DEFAULT ['buy','sell'][rand() % 2 + 1],
    quantity    uint32   DEFAULT (1 + rand() % 1000)::uint32,
    price       float64  DEFAULT round(50 + (rand() % 4950)::float64 + rand()::float64, 2),
    trader_id   string   DEFAULT 'trader-' || to_string(rand() % 100)
)
SETTINGS eps = 200;
```

### Clickstream with Nested JSON

```sql
CREATE RANDOM STREAM IF NOT EXISTS clickstream (
    raw string DEFAULT concat(
        '{"user_id":"u-', to_string(rand() % 10000),
        '","event":"', ['click','scroll','hover','submit'][rand() % 4 + 1],
        '","x":', to_string(rand() % 1920),
        ',"y":', to_string(rand() % 1080),
        ',"ts":', to_string(to_unix_timestamp(now())), '}'
    )
)
SETTINGS eps = 30;
```

---

## Rate Control

```sql
-- Very high throughput (stress test)
CREATE RANDOM STREAM load_test (id uint64 DEFAULT rand64())
SETTINGS eps = 100000;                 -- 100K events/sec

-- Slow trickle (one event every 10 seconds)
CREATE RANDOM STREAM slow_stream (id uint64 DEFAULT rand64())
SETTINGS eps = 0.1;

-- Batched: emit 1000 events every 500ms
CREATE RANDOM STREAM batch_stream (id uint64 DEFAULT rand64())
SETTINGS eps = 2000, interval_time = 500;
```

---

## One-Shot Batch with table()

Use `table()` to get a single static batch (≈65,409 rows) instead of a continuous stream:

```sql
-- Get a single batch of ~65K random rows
SELECT device_id, avg(temperature) AS avg_temp
FROM table(iot_sensors)
GROUP BY device_id;
```

---

## Querying Random Streams

```bash
# Continuously stream 10 seconds of data (Ctrl+C to stop)
echo "SELECT device_id, temperature, status FROM iot_sensors LIMIT 20" | \
  curl "http://${TIMEPLUS_HOST}:8123/" \
    -H "X-ClickHouse-User: ${TIMEPLUS_USER}" \
    -H "X-ClickHouse-Key: ${TIMEPLUS_PASSWORD}" \
    --data-binary @-

# Get a static batch of rows
echo "SELECT * FROM table(iot_sensors) LIMIT 100 FORMAT JSONEachRow" | \
  curl "http://${TIMEPLUS_HOST}:8123/" \
    -H "X-ClickHouse-User: ${TIMEPLUS_USER}" \
    -H "X-ClickHouse-Key: ${TIMEPLUS_PASSWORD}" \
    --data-binary @-
```

---

## Using Random Streams as Pipeline Input

Random streams work just like native streams — pipe them through materialized views:

```sql
-- 1. Create random input
CREATE RANDOM STREAM IF NOT EXISTS raw_trades (
    symbol  string  DEFAULT ['AAPL','MSFT','GOOGL'][rand() % 3 + 1],
    price   float64 DEFAULT 100 + (rand() % 400)::float64,
    qty     uint32  DEFAULT (1 + rand() % 100)::uint32,
    side    string  DEFAULT ['buy','sell'][rand() % 2 + 1]
) SETTINGS eps = 10;

-- 2. Create output stream
CREATE STREAM IF NOT EXISTS trade_summary (
    window_start datetime64(3),
    symbol       string,
    trade_count  uint64,
    total_volume float64,
    vwap         float64
);

-- 3. Materialize aggregations from random stream
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_trade_summary
INTO trade_summary AS
SELECT
    window_start,
    symbol,
    count()          AS trade_count,
    sum(price * qty) AS total_volume,
    sum(price * qty) / sum(qty) AS vwap
FROM tumble(raw_trades, 1m)
GROUP BY window_start, symbol;
```

---

## Drop a Random Stream

```bash
echo "DROP STREAM IF EXISTS iot_sensors" | \
  curl "http://${TIMEPLUS_HOST}:8123/" \
    -H "X-ClickHouse-User: ${TIMEPLUS_USER}" \
    -H "X-ClickHouse-Key: ${TIMEPLUS_PASSWORD}" \
    --data-binary @-
```
