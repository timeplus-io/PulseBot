# Random Streams — Skill Guide for Timeplus SQL Agent

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

## Supported Data Types

| Category | Types |
|----------|-------|
| Numeric | `int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`, `float32`, `float64` |
| Text | `string` |
| Temporal | `date`, `datetime`, `datetime64(3)` |
| Boolean | `bool` |
| Structured | `array(type)`, `json` |
| Identifiers | `uuid` |
| Enums | `enum8('value'=1, 'value2'=2)`, `enum16(...)` |

---

## Random Generation Functions

### Numeric Distributions

> **CRITICAL**: All parameters must be **constants**, not variables or column references.

| Function | Description | Example |
|----------|-------------|---------|
| `rand()` | Random uint32 (0..4294967295) | `rand() % 100` → 0..99 |
| `rand64()` | Random uint64 | `rand64()` |
| `rand_uniform(min, max)` | Uniform distribution (float) | `rand_uniform(0.0, 100.0)` |
| `rand_normal(mean, stddev)` | Normal / Gaussian distribution | `rand_normal(22.0, 5.0)` |
| `rand_log_normal(mean, stddev)` | Log-normal distribution | `rand_log_normal(3.5, 1.2)` |
| `rand_exponential(lambda)` | Exponential distribution | `rand_exponential(0.5)` |
| `rand_poisson(lambda)` | Poisson distribution | `rand_poisson(150)` |
| `rand_bernoulli(p)` | Bernoulli distribution | `rand_bernoulli(0.3)` |
| `rand_student_t(degrees)` | Student's t-distribution | `rand_student_t(10)` |
| `rand_chi_squared(degrees)` | Chi-squared distribution | `rand_chi_squared(5)` |

### Rand Seed Rules

> **CRITICAL**: To produce properly independent random values across columns, **use a different integer seed for each `rand()` call** in a stream. Without seeds, multiple `rand()` calls may return correlated values.

```sql
-- ✅ Each column gets its own seed → independent values
device_id  string  DEFAULT concat('sensor-', to_string(rand(0) % 50)),
location   string  DEFAULT array_element([...], (rand(1) % 4) + 1),
battery    uint8   DEFAULT (rand(2) % 101)::uint8
```

> **Exception — `multi_if` weighted distributions**: within a single `multi_if` expression, all `rand()` calls that form the same logical branch comparison **must share the same seed**, so the conditions evaluate against a consistent random value for that row.

```sql
-- ✅ Same seed (1) throughout so all conditions compare the same number
customer_type string DEFAULT multi_if(
    (rand(1) % 100) < 60, 'regular',   -- 60%
    (rand(1) % 100) < 80, 'premium',   -- 20%
    'vip'                               -- 20%
)
```

---

### String Generation

| Function | Returns | Example |
|----------|---------|---------|
| `random_printable_ascii(N)` | N printable ASCII chars | `random_printable_ascii(8)` |
| `random_string_utf8(N)` | N UTF-8 characters | `random_string_utf8(10)` |
| `random_string(N)` | Binary string (may be non-printable) | `random_string(16)` |
| `random_fixed_string(N)` | Fixed binary string | `random_fixed_string(4)` |
| `uuid()` | Random UUID string | Unique IDs |
| `random_in_type('ipv4')` | Random IPv4 address | `random_in_type('ipv4')` |
| `random_in_type('ipv6')` | Random IPv6 address | `random_in_type('ipv6')` |

### Timestamp

```sql
now64(3, 'UTC')   -- current datetime64(3) at ingestion time
now()             -- current datetime
```

---

## Generating Realistic Data with `generate()`

For common real-world data types, use `generate('type_name', rand(seed))`.

to use such function, we need to install the `Faker` and `generate` UDF  first.

```sql

SYSTEM INSTALL PYTHON PACKAGE 'faker';

CREATE OR REPLACE FUNCTION generate(data string, seed uint32) RETURNS string LANGUAGE PYTHON AS 
$$
from faker import Faker
fake = Faker()

def generate(data, seed):
  result = []
  for d , s in zip(data, seed):
    try:
      r = fake.format(d)
      result.append(r)
    except:
      result.append('')
  return result
$$;
```

**Each `generate()` call must use a different seed** so each column produces independent values:

```sql
CREATE RANDOM STREAM test_generate (
    full_name    string DEFAULT generate('name',               rand(0)),
    first_name   string DEFAULT generate('first_name',         rand(1)),
    last_name    string DEFAULT generate('last_name',          rand(2)),
    email        string DEFAULT generate('email',              rand(3)),
    phone        string DEFAULT generate('phone_number',       rand(4)),
    address      string DEFAULT generate('address',            rand(5)),
    city         string DEFAULT generate('city',               rand(6)),
    state        string DEFAULT generate('state',              rand(7)),
    country      string DEFAULT generate('country',            rand(8)),
    postcode     string DEFAULT generate('postcode',           rand(9)),
    company      string DEFAULT generate('company',            rand(10)),
    job_title    string DEFAULT generate('job',                rand(11)),
    url          string DEFAULT generate('url',                rand(12)),
    mac_address  string DEFAULT generate('mac_address',        rand(13)),
    credit_card  string DEFAULT generate('credit_card_number', rand(14)),
    currency     string DEFAULT generate('currency_code',      rand(15)),
    color        string DEFAULT generate('color_name',         rand(16))
)
SETTINGS eps = 10;
```

**Available `generate()` categories:**

| Category | Type Names |
|----------|-----------|
| Person | `name`, `first_name`, `last_name`, `email`, `phone_number` |
| Address | `address`, `street_address`, `city`, `state`, `country`, `postcode` |
| Company | `company`, `job`, `company_email` |
| Internet | `url`, `domain_name`, `mac_address` |
| Text | `text`, `sentence`, `paragraph`, `word` |
| Finance | `credit_card_number`, `iban`, `currency_code` |
| Automotive | `license_plate` |
| Color | `color_name`, `hex_color`, `rgb_color` |

---

## Essential Patterns

### 1. Array Selection (pick from a list)

```sql
-- Equal probability across options
status string DEFAULT array_element(['ok','warn','error','offline'], (rand() % 4) + 1)
```

### 2. Weighted Distribution

Use `multi_if` (NOT `CASE WHEN`) for conditional logic. Use the **same seed** for all `rand()` calls within one `multi_if` so every condition evaluates the same random number:

```sql
-- 60% regular, 20% premium, 20% VIP
-- rand(5) used consistently so thresholds compare the same value
customer_type string DEFAULT multi_if(
    (rand(5) % 100) < 60, 'regular',
    (rand(5) % 100) < 80, 'premium',
    'vip'
)
```

### 3. String Composition

```sql
email string DEFAULT concat(
    random_printable_ascii(8),
    '@',
    array_element(['gmail.com', 'yahoo.com', 'company.com'], (rand() % 3) + 1)
),
user_id string DEFAULT concat('user-', to_string(rand() % 10000))
```

### 4. Numeric Ranges

```sql
-- Integer in range [min, max)
score  uint8   DEFAULT (rand() % 101)::uint8,            -- 0..100
port   uint16  DEFAULT (1024 + rand() % 64511)::uint16,  -- 1024..65535

-- Float with rounding
price  float64 DEFAULT round(rand_uniform(5.0, 500.0), 2),
temp   float32 DEFAULT round(rand_normal(22.0, 8.0)::float32, 1)
```

### 5. Geographic Coordinates

```sql
latitude  float64 DEFAULT round(rand_uniform(40.0, 45.0), 6),
longitude float64 DEFAULT round(rand_uniform(-125.0, -70.0), 6)
```

### 6. Time-based Patterns

```sql
-- Simulate traffic that varies by hour of day
traffic_volume uint32 DEFAULT multi_if(
    to_hour(now()) >= 7  AND to_hour(now()) <= 9,  rand_poisson(300),  -- Rush hour
    to_hour(now()) >= 22 OR  to_hour(now()) <= 6,  rand_poisson(50),   -- Night
    rand_poisson(150)                                                    -- Regular
)::uint32
```

### 7. Related Field Dependencies

Fields can reference each other through `multi_if`:

```sql
price    float64 DEFAULT round(exp(rand_normal(3.5, 1.2)), 2),
quantity uint32  DEFAULT (1 + rand() % 100)::uint32

-- Note: computed fields that depend on other random fields
-- should use the same random seed trick or be computed downstream
-- (e.g., in a materialized view)
```

### 8. Inline JSON / Raw String Events

```sql
raw string DEFAULT concat(
    '{"user_id":"u-', to_string(rand() % 10000),
    '","event":"', array_element(['click','scroll','submit'], (rand() % 3) + 1),
    '","x":', to_string(rand() % 1920),
    ',"y":', to_string(rand() % 1080),
    ',"ts":', to_string(to_unix_timestamp(now())), '}'
)
```

---

## Practical Examples

### IoT Sensor Data

```sql
CREATE RANDOM STREAM IF NOT EXISTS iot_sensors (
    device_id   string   DEFAULT concat('sensor-', to_string(rand(0) % 50)),
    location    string   DEFAULT array_element(['warehouse-a','warehouse-b','rooftop','basement'], (rand(1) % 4) + 1),
    temperature float32  DEFAULT round(rand_normal(22.0, 8.0)::float32, 1),
    humidity    float32  DEFAULT round(rand_uniform(20.0, 80.0)::float32, 1),
    pressure    float32  DEFAULT round(rand_uniform(1000.0, 1050.0)::float32, 1),
    battery     uint8    DEFAULT (rand(2) % 101)::uint8,
    status      string   DEFAULT array_element(['ok','warn','error','offline'], (rand(3) % 4) + 1)
)
SETTINGS eps = 20;
```

### E-Commerce Events

```sql
CREATE RANDOM STREAM IF NOT EXISTS ecommerce_events (
    event_id    string   DEFAULT random_printable_ascii(12),
    user_id     string   DEFAULT concat('user-', to_string(rand(0) % 10000)),
    session_id  string   DEFAULT concat('sess-', to_string(rand(1) % 100000)),
    event_type  string   DEFAULT array_element(['page_view','add_to_cart','checkout','purchase','refund'], (rand(2) % 5) + 1),
    product_id  string   DEFAULT concat('prod-', to_string(rand(3) % 500)),
    category    string   DEFAULT array_element(['electronics','clothing','food','books','sports'], (rand(4) % 5) + 1),
    amount      float64  DEFAULT round(rand_uniform(5.0, 500.0), 2),
    country     string   DEFAULT array_element(['US','GB','DE','JP','BR','CA','FR'], (rand(5) % 7) + 1)
)
SETTINGS eps = 50;
```

### Web Access Logs

```sql
CREATE RANDOM STREAM IF NOT EXISTS web_logs (
    ip          string   DEFAULT random_in_type('ipv4'),
    method      string   DEFAULT array_element(['GET','POST','PUT','DELETE'], (rand(0) % 4) + 1),
    path        string   DEFAULT array_element(['/api/users','/api/orders','/api/products','/health','/login'], (rand(1) % 5) + 1),
    status_code uint16   DEFAULT array_element([200, 200, 200, 201, 400, 401, 403, 404, 500], (rand(2) % 9) + 1),
    latency_ms  uint32   DEFAULT (10 + rand(3) % 990)::uint32,
    user_agent  string   DEFAULT array_element(['Chrome/120','Firefox/121','Safari/17','curl/8.0'], (rand(4) % 4) + 1)
)
SETTINGS eps = 100;
```

### Financial Trades

```sql
CREATE RANDOM STREAM IF NOT EXISTS trades (
    trade_id    string   DEFAULT uuid(),
    symbol      string   DEFAULT array_element(['AAPL','GOOGL','MSFT','TSLA','AMZN','META','NVDA'], (rand(0) % 7) + 1),
    side        string   DEFAULT array_element(['buy','sell'], (rand(1) % 2) + 1),
    quantity    uint32   DEFAULT (1 + rand(2) % 1000)::uint32,
    price       float64  DEFAULT round(rand_uniform(50.0, 5000.0), 2),
    trader_id   string   DEFAULT concat('trader-', to_string(rand(3) % 100))
)
SETTINGS eps = 200;
```

### Realistic Person & Company Data

```sql
CREATE RANDOM STREAM IF NOT EXISTS crm_leads (
    lead_id     string   DEFAULT uuid(),
    full_name   string   DEFAULT generate('name',         rand(0)),
    email       string   DEFAULT generate('email',        rand(1)),
    phone       string   DEFAULT generate('phone_number', rand(2)),
    company     string   DEFAULT generate('company',      rand(3)),
    city        string   DEFAULT generate('city',         rand(4)),
    country     string   DEFAULT generate('country',      rand(5)),
    lead_score  uint8    DEFAULT (rand(6) % 101)::uint8,
    status      string   DEFAULT array_element(['new','contacted','qualified','converted'], (rand(7) % 4) + 1)
)
SETTINGS eps = 5;
```

---

## Rate Control

```sql
-- Default: 1 event/sec
CREATE RANDOM STREAM slow_stream (id uint64 DEFAULT rand64())
SETTINGS eps = 1;

-- Trickle: one event every 10 seconds
CREATE RANDOM STREAM very_slow (id uint64 DEFAULT rand64())
SETTINGS eps = 0.1;

-- High throughput stress test
CREATE RANDOM STREAM load_test (id uint64 DEFAULT rand64())
SETTINGS eps = 100000;

-- Batched: emit 2000 events in bursts every 500ms
CREATE RANDOM STREAM batch_stream (id uint64 DEFAULT rand64())
SETTINGS eps = 2000, interval_time = 500;
```

---

## One-Shot Batch with `table()`

Use `table()` to read a single static snapshot (~65,409 rows) instead of a continuous stream:

```sql
SELECT device_id, avg(temperature) AS avg_temp
FROM table(iot_sensors)
GROUP BY device_id;
```

---

## Using Random Streams as Pipeline Input

Random streams work just like native streams — pipe them through materialized views:

```sql
-- 1. Random input stream
CREATE RANDOM STREAM IF NOT EXISTS raw_trades (
    symbol  string  DEFAULT array_element(['AAPL','MSFT','GOOGL'], (rand(0) % 3) + 1),
    price   float64 DEFAULT round(rand_uniform(100.0, 500.0), 2),
    qty     uint32  DEFAULT (1 + rand(1) % 100)::uint32,
    side    string  DEFAULT array_element(['buy','sell'], (rand(2) % 2) + 1)
) SETTINGS eps = 10;

-- 2. Output stream
CREATE STREAM IF NOT EXISTS trade_summary (
    window_start datetime64(3),
    symbol       string,
    trade_count  uint64,
    total_volume float64,
    vwap         float64
);

-- 3. Materialized view: aggregate from random stream
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_trade_summary
INTO trade_summary AS
SELECT
    window_start,
    symbol,
    count()                     AS trade_count,
    sum(price * qty)            AS total_volume,
    sum(price * qty) / sum(qty) AS vwap
FROM tumble(raw_trades, 1m)
GROUP BY window_start, symbol;
```

---

## Drop a Random Stream

```sql
DROP STREAM IF EXISTS iot_sensors
```

---

## Best Practices Checklist

- Use `array_element([...], (rand(N) % K) + 1)` for picking from a fixed list
- Use `multi_if(...)` instead of `CASE WHEN` for conditional logic
- **Use a unique integer seed for each `rand()` call across columns** — e.g. `rand(0)`, `rand(1)`, `rand(2)` — to ensure independent values
- **Within a single `multi_if` weighted distribution, use the same seed** for all conditions so they compare the same random number
- All parameters in `rand_*` distribution functions must be **constants**
- Apply realistic statistical distributions (`rand_normal`, `rand_log_normal`, `rand_poisson`) instead of pure `rand()` where appropriate
- Cast numeric results to the target type explicitly: `(rand() % 100)::uint8`
- Use `round(..., 2)` for monetary values
- Use `uuid()` for globally unique identifiers
- Use `generate('type', rand())` for realistic human-readable fake data
- Use `random_in_type('ipv4')` instead of hand-crafting IP strings
- Set `eps` appropriate to your test goal — typical range is 1–1000; use higher values only for stress testing
- Always use `IF NOT EXISTS` in `CREATE` statements for idempotent scripts