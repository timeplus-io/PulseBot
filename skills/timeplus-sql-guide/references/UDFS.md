# User-Defined Functions (UDFs) in Timeplus

Timeplus supports four kinds of UDFs:

| Kind | Engine | Best For |
|------|--------|----------|
| **JavaScript UDF / UDAF** | V8 (embedded) | Fast scalar transforms, stateful aggregations, no external service |
| **Python UDF** | Python 3.10 (embedded) | ML inference, numpy/pandas, complex logic (Enterprise 2.7+) |
| **Remote UDF** | HTTP webhook | External APIs, any language, microservice logic |
| **SQL Lambda** | Pure SQL | Simple expressions without external code |

---

## 1. JavaScript UDF (Scalar)

JavaScript UDFs use the V8 engine embedded in Timeplus. **Inputs are batched as arrays** — the function receives an array of values and must return an array of results of the same length.

### Basic Pattern

```sql
CREATE OR REPLACE FUNCTION function_name(param1 type1, param2 type2)
RETURNS return_type
LANGUAGE JAVASCRIPT AS $$
  function function_name(param1_values, param2_values) {
    // param1_values is an array of values
    // return an array of results
    return param1_values.map((v, i) => {
      // your logic here
      return result;
    });
  }
$$;
```

The **JavaScript function name must exactly match** the SQL function name.

### Examples

```sql
-- Mask an email address
CREATE OR REPLACE FUNCTION mask_email(email string)
RETURNS string
LANGUAGE JAVASCRIPT AS $$
  function mask_email(emails) {
    return emails.map(email => {
      const [local, domain] = email.split('@');
      return local[0] + '***@' + domain;
    });
  }
$$;

-- Classify temperature
CREATE OR REPLACE FUNCTION classify_temp(temp float32)
RETURNS string
LANGUAGE JAVASCRIPT AS $$
  function classify_temp(temps) {
    return temps.map(t => {
      if (t > 40) return 'critical';
      if (t > 30) return 'warning';
      if (t > 0)  return 'normal';
      return 'freeze';
    });
  }
$$;

-- Parse a custom log format
CREATE OR REPLACE FUNCTION parse_log(raw string)
RETURNS string
LANGUAGE JAVASCRIPT AS $$
  function parse_log(raws) {
    return raws.map(raw => {
      try {
        const m = raw.match(/(\d{4}-\d{2}-\d{2}) (\w+) (.+)/);
        if (!m) return '{}';
        return JSON.stringify({ date: m[1], level: m[2], msg: m[3] });
      } catch(e) {
        return '{}';
      }
    });
  }
$$;

-- Multi-param function: compute revenue
CREATE OR REPLACE FUNCTION calc_revenue(price float64, qty int32, discount float32)
RETURNS float64
LANGUAGE JAVASCRIPT AS $$
  function calc_revenue(prices, qtys, discounts) {
    return prices.map((p, i) => p * qtys[i] * (1 - discounts[i]));
  }
$$;
```

### Type Mapping (SQL ↔ JavaScript)

| SQL Type | JavaScript Type |
|----------|----------------|
| `int8`..`int64`, `uint8`..`uint64` | `number` |
| `float32`, `float64` | `number` |
| `string` | `string` |
| `bool` | `boolean` |
| `array(T)` | `Array` |
| `map(K, V)` | `Object` |
| `datetime64` | `number` (unix ms) |
| `nullable(T)` | `T | null` |

### Use UDFs in Queries

```sql
-- In SELECT
SELECT mask_email(user_email), classify_temp(temperature)
FROM sensor_data;

-- In WHERE
SELECT * FROM sensor_data WHERE classify_temp(temperature) = 'critical';

-- In materialized view
CREATE MATERIALIZED VIEW mv_classified INTO classified_events AS
SELECT device_id, temperature, classify_temp(temperature) AS level
FROM sensor_data;
```

---

## 2. JavaScript UDAF (User-Defined Aggregate Function)

UDAFs maintain state across rows within a window or group.

```sql
CREATE AGGREGATE FUNCTION udaf_name(param type)
RETURNS return_type
LANGUAGE JAVASCRIPT AS $$
{
  initialize: function() {
    // Initialize state — called once per group/window
    this.state = { ... };
  },
  process: function(values) {
    // Called with a batch of values
    for (let i = 0; i < values.length; i++) {
      // Update this.state with values[i]
    }
  },
  finalize: function() {
    // Return the final aggregation result
    return this.state.result;
  },
  serialize: function() {
    // Serialize state to string (for checkpointing/merging)
    return JSON.stringify(this.state);
  },
  deserialize: function(serialized) {
    // Restore state from string
    this.state = JSON.parse(serialized);
  },
  merge: function(otherSerialized) {
    // Merge another shard's serialized state into this one
    const other = JSON.parse(otherSerialized);
    // combine this.state with other
  }
}
$$;
```

### UDAF Examples

```sql
-- Second-largest value
CREATE AGGREGATE FUNCTION second_largest(value float64)
RETURNS float64
LANGUAGE JAVASCRIPT AS $$
{
  initialize: function() { this.max = -Infinity; this.second = -Infinity; },
  process: function(values) {
    for (let v of values) {
      if (v > this.max) { this.second = this.max; this.max = v; }
      else if (v > this.second) { this.second = v; }
    }
  },
  finalize: function() { return this.second === -Infinity ? null : this.second; },
  serialize: function() { return JSON.stringify({ max: this.max, second: this.second }); },
  deserialize: function(s) { let o = JSON.parse(s); this.max = o.max; this.second = o.second; },
  merge: function(s) {
    let other = JSON.parse(s);
    if (other.max > this.max) { this.second = Math.max(this.max, other.second); this.max = other.max; }
    else if (other.max > this.second) { this.second = other.max; }
  }
}
$$;

-- Running count of distinct values (HLL approx)
CREATE AGGREGATE FUNCTION count_unique_approx(val string)
RETURNS uint64
LANGUAGE JAVASCRIPT AS $$
{
  initialize: function() { this.seen = {}; },
  process: function(vals) { for (let v of vals) this.seen[v] = 1; },
  finalize: function() { return Object.keys(this.seen).length; },
  serialize: function() { return JSON.stringify(this.seen); },
  deserialize: function(s) { this.seen = JSON.parse(s); },
  merge: function(s) { Object.assign(this.seen, JSON.parse(s)); }
}
$$;
```

### Use UDAFs in queries

```sql
SELECT device_id, second_largest(temperature)
FROM tumble(sensor_data, 5m)
GROUP BY window_start, device_id;
```

---

## 3. Python UDF (Enterprise 2.7+)

Python UDFs run in an embedded Python 3.10 interpreter. They receive
**lists of values** and must return a list of results.

### Install Python Packages

```bash
echo "SYSTEM INSTALL PYTHON PACKAGE 'numpy'" | \
  curl "http://${TIMEPLUS_HOST}:8123/" \
    -H "X-ClickHouse-User: ${TIMEPLUS_USER}" \
    -H "X-ClickHouse-Key: ${TIMEPLUS_PASSWORD}" \
    --data-binary @-

echo "SYSTEM INSTALL PYTHON PACKAGE 'scikit-learn'" | \
  curl "http://${TIMEPLUS_HOST}:8123/" \
    -H "X-ClickHouse-User: ${TIMEPLUS_USER}" \
    -H "X-ClickHouse-Key: ${TIMEPLUS_PASSWORD}" \
    --data-binary @-
```

Pre-installed: `numpy`. Installable: `pandas`, `scipy`, `scikit-learn`, `requests`, etc.

### Python UDF Pattern

```sql
CREATE OR REPLACE FUNCTION function_name(param type, ...)
RETURNS return_type
LANGUAGE PYTHON AS $$
import numpy as np

def function_name(param_values, ...):
    # param_values is a list
    # return a list of results of same length
    return [your_logic(v) for v in param_values]
$$;
```

### Python UDF Examples

```sql
-- Z-score normalization using numpy
CREATE OR REPLACE FUNCTION normalize(values array(float64))
RETURNS float64
LANGUAGE PYTHON AS $$
import numpy as np

def normalize(value_lists):
    results = []
    for arr in value_lists:
        np_arr = np.array(arr)
        mean, std = np_arr.mean(), np_arr.std()
        results.append(float((arr[-1] - mean) / std) if std > 0 else 0.0)
    return results
$$;

-- Anomaly score using IQR
CREATE OR REPLACE FUNCTION anomaly_score(value float64, p25 float64, p75 float64)
RETURNS float64
LANGUAGE PYTHON AS $$
def anomaly_score(values, p25s, p75s):
    results = []
    for v, q1, q3 in zip(values, p25s, p75s):
        iqr = q3 - q1
        if iqr == 0:
            results.append(0.0)
        else:
            results.append(abs(v - (q1 + q3) / 2) / iqr)
    return results
$$;

-- JSON parsing with Python
CREATE OR REPLACE FUNCTION extract_tags(payload string)
RETURNS array(string)
LANGUAGE PYTHON AS $$
import json

def extract_tags(payloads):
    result = []
    for p in payloads:
        try:
            data = json.loads(p)
            result.append(data.get('tags', []))
        except Exception:
            result.append([])
    return result
$$;

-- Text classification (rule-based)
CREATE OR REPLACE FUNCTION classify_message(msg string)
RETURNS string
LANGUAGE PYTHON AS $$
def classify_message(messages):
    categories = []
    for msg in messages:
        msg_lower = msg.lower()
        if any(w in msg_lower for w in ['error', 'fail', 'exception', 'crash']):
            categories.append('error')
        elif any(w in msg_lower for w in ['warn', 'slow', 'timeout']):
            categories.append('warning')
        else:
            categories.append('info')
    return categories
$$;
```

### Create Python UDF via curl

```bash
cat <<'EOF' | curl "http://${TIMEPLUS_HOST}:8123/" \
  -H "X-ClickHouse-User: ${TIMEPLUS_USER}" \
  -H "X-ClickHouse-Key: ${TIMEPLUS_PASSWORD}" \
  --data-binary @-
CREATE OR REPLACE FUNCTION add_prefix(s string)
RETURNS string
LANGUAGE PYTHON AS $$
def add_prefix(strings):
    return ['prefix_' + s for s in strings]
$$
EOF
```

---

## 4. Remote UDF (HTTP Webhook)

Remote UDFs call an external HTTP endpoint. Timeplus POSTs a JSON batch and
expects a JSON array of results back.

```sql
CREATE REMOTE FUNCTION geo_lookup(ip string)
RETURNS string
URL 'https://api.ipgeo.example.com/lookup'
AUTH_METHOD 'auth_header'
AUTH_HEADER 'Authorization'
AUTH_KEY 'Bearer my-api-token'
EXECUTION_TIMEOUT 5000;    -- ms, default 10000
```

**Auth methods:** `none`, `auth_header`, `query_param`.

**Request format** (Timeplus → your service):
```json
{ "input": [["192.168.1.1"], ["10.0.0.1"]] }
```

**Response format** (your service → Timeplus):
```json
{ "output": ["US", "DE"] }
```

**Create via curl:**
```bash
echo "CREATE REMOTE FUNCTION sentiment(text string)
RETURNS float32
URL 'https://your-ml-api.example.com/sentiment'
AUTH_METHOD 'none'
EXECUTION_TIMEOUT 3000" | \
curl "http://${TIMEPLUS_HOST}:8123/" \
  -H "X-ClickHouse-User: ${TIMEPLUS_USER}" \
  -H "X-ClickHouse-Key: ${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

---

## 5. SQL Lambda UDF

Pure SQL expressions — no external code, no runtime overhead.

```sql
-- Simple arithmetic
CREATE FUNCTION celsius_to_fahrenheit AS (c) -> c * 9 / 5 + 32;

-- String manipulation
CREATE FUNCTION full_name AS (first, last) -> concat(first, ' ', last);

-- Multi-arg expression
CREATE FUNCTION bmi AS (weight_kg, height_m) -> weight_kg / (height_m * height_m);

-- Conditional
CREATE FUNCTION grade AS (score) ->
    CASE
        WHEN score >= 90 THEN 'A'
        WHEN score >= 80 THEN 'B'
        WHEN score >= 70 THEN 'C'
        ELSE 'F'
    END;

-- Color hex from RGB
CREATE FUNCTION rgb_to_hex AS (r, g, b) ->
    '#' || lower(hex(r::uint8)) || lower(hex(g::uint8)) || lower(hex(b::uint8));
```

**Create via curl:**
```bash
echo "CREATE OR REPLACE FUNCTION c2f AS (c) -> c * 9 / 5 + 32" | \
  curl "http://${TIMEPLUS_HOST}:8123/" \
    -H "X-ClickHouse-User: ${TIMEPLUS_USER}" \
    -H "X-ClickHouse-Key: ${TIMEPLUS_PASSWORD}" \
    --data-binary @-
```

---

## Managing UDFs

```bash
# List all functions
echo "SHOW FUNCTIONS" | curl "http://${TIMEPLUS_HOST}:8123/" \
  -H "X-ClickHouse-User: ${TIMEPLUS_USER}" \
  -H "X-ClickHouse-Key: ${TIMEPLUS_PASSWORD}" \
  --data-binary @-

# Drop a function
echo "DROP FUNCTION IF EXISTS mask_email" | curl "http://${TIMEPLUS_HOST}:8123/" \
  -H "X-ClickHouse-User: ${TIMEPLUS_USER}" \
  -H "X-ClickHouse-Key: ${TIMEPLUS_PASSWORD}" \
  --data-binary @-

# Test a UDF immediately
echo "SELECT mask_email('gang@timeplus.com')" | curl "http://${TIMEPLUS_HOST}:8123/" \
  -H "X-ClickHouse-User: ${TIMEPLUS_USER}" \
  -H "X-ClickHouse-Key: ${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

---

## UDF Decision Guide

| Scenario | Recommended |
|----------|-------------|
| Simple string/math transform | SQL Lambda |
| Complex logic, no dependencies | JavaScript UDF |
| Custom aggregation | JavaScript UDAF |
| numpy, pandas, ML inference | Python UDF |
| External API, non-Python/JS | Remote UDF |
| High throughput (>100K rows/s) | JavaScript UDF (lowest overhead) |
| Large ML model | Remote UDF (stateless microservice) |
