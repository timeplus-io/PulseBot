# Getting Data Into Timeplus

## 1. CREATE STREAM (Native Streams)

### Append Stream (default — immutable event log)

```sql
CREATE STREAM IF NOT EXISTS sensor_data (
    device_id   string,
    temperature float32,
    humidity    float32,
    location    string,
    ts          datetime64(3, 'UTC') DEFAULT now64(3, 'UTC')
)
SETTINGS
    event_time_column    = 'ts',
    logstore_retention_ms = 86400000,   -- 1 day retention
    shards               = 1,
    replication_factor   = 1;
```

Key `CREATE STREAM` settings:

| Setting | Default | Description |
|---------|---------|-------------|
| `event_time_column` | `_tp_time` | Column to use as event time |
| `logstore_retention_ms` | 604800000 | Log retention in ms (7 days) |
| `logstore_retention_bytes` | ∞ | Log retention in bytes |
| `shards` | 1 | Number of shards (parallelism) |
| `replication_factor` | 1 | Replication factor |
| `logstore_codec` | none | Compression: `none`, `zstd`, `lz4` |
| `storage_type` | `streaming` | `streaming`, `hybrid`, `memory` |

**TTL (auto-expiry):**
```sql
CREATE STREAM events (
    id string,
    payload string
) TTL _tp_time + INTERVAL 7 DAY;
```

---

### Versioned KV Stream (latest value per key)

Use for dimension tables / lookup tables that change over time.

```sql
CREATE STREAM IF NOT EXISTS products (
    product_id string,
    name       string,
    price      float32,
    category   string
)
PRIMARY KEY (product_id)
SETTINGS mode = 'versioned_kv';
```

- Only the **latest** row per primary key is retained for lookups.
- You can JOIN an append stream to a versioned_kv stream to enrich events.
- Composite primary keys: `PRIMARY KEY (tenant_id, product_id)`.

---

### Changelog KV Stream (insert / update / delete tracking)

```sql
CREATE STREAM IF NOT EXISTS inventory (
    item_id   string,
    quantity  int32,
    updated   datetime64(3) DEFAULT now64(3)
)
PRIMARY KEY (item_id)
SETTINGS mode = 'changelog_kv';
```

Write `_tp_delta = 1` for INSERT/UPDATE, `_tp_delta = -1` for DELETE.

---

### Mutable Stream (Enterprise — full row-level mutations)

```sql
CREATE MUTABLE STREAM IF NOT EXISTS user_profiles (
    user_id   string,
    name      string,
    email     string,
    score     float32,
    INDEX idx_email (email) UNIQUE
)
PRIMARY KEY (user_id)
SETTINGS ttl_seconds = 604800;
```

Supports `UPDATE` and `DELETE` statements. Good for entity tables.

---

## 2. INSERT INTO (Direct Write)

```sql
-- Single row
INSERT INTO sensor_data (device_id, temperature, humidity, location)
VALUES ('dev-001', 23.5, 61.2, 'warehouse-a');

-- Multiple rows
INSERT INTO sensor_data (device_id, temperature, humidity, location) VALUES
('dev-002', 19.1, 70.0, 'office'),
('dev-003', 31.4, 45.5, 'rooftop');

-- From another stream (batch copy)
INSERT INTO sensor_data SELECT device_id, temperature, humidity, location
FROM table(sensor_data_archive);
```

**Via curl:**
```bash
echo "INSERT INTO sensor_data (device_id, temperature) VALUES ('dev-1', 22.0)" | \
  curl "http://${TIMEPLUS_HOST}:8123/" \
    -H "X-ClickHouse-User: ${TIMEPLUS_USER}" \
    -H "X-ClickHouse-Key: ${TIMEPLUS_PASSWORD}" \
    --data-binary @-
```

---

## 3. REST Ingest API (port 3218)

Push JSON batch payloads directly.

```bash
# Push a batch of rows
curl -s -X POST "http://${TIMEPLUS_HOST}:3218/proton/v1/ingest/streams/sensor_data" \
  -H "Content-Type: application/json" \
  -d '{
    "columns": ["device_id", "temperature", "humidity"],
    "data": [
      ["dev-001", 23.5, 61.2],
      ["dev-002", 19.1, 70.0],
      ["dev-003", 31.4, 45.5]
    ]
  }'
```

**With authentication:**
```bash
curl -s -X POST "http://${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}@${TIMEPLUS_HOST}:3218/proton/v1/ingest/streams/sensor_data" \
  -H "Content-Type: application/json" \
  -d '{"columns":["device_id","temperature"],"data":[["dev-1",22.5]]}'
```

---

## 4. External Streams (Kafka, Pulsar, Timeplus)

External streams read from and write to external systems without copying data.

### Kafka / Confluent / Redpanda / MSK

```sql
-- Read raw messages
CREATE EXTERNAL STREAM IF NOT EXISTS kafka_raw (
    raw string
)
SETTINGS
    type       = 'kafka',
    brokers    = 'kafka-broker:9092',
    topic      = 'my_topic',
    data_format = 'RawBLOB';
```

```sql
-- Read structured JSON
CREATE EXTERNAL STREAM IF NOT EXISTS kafka_orders (
    order_id string,
    user_id  string,
    amount   float32,
    status   string
)
SETTINGS
    type        = 'kafka',
    brokers     = 'kafka-broker:9092',
    topic       = 'orders',
    data_format = 'JSONEachRow';
```

```sql
-- With authentication (SASL_SSL)
CREATE EXTERNAL STREAM IF NOT EXISTS kafka_secure (raw string)
SETTINGS
    type               = 'kafka',
    brokers            = 'pkc-xxxx.us-east-1.aws.confluent.cloud:9092',
    topic              = 'secure_topic',
    data_format        = 'RawBLOB',
    security_protocol  = 'SASL_SSL',
    sasl_mechanism     = 'PLAIN',
    username           = 'api_key',
    password           = 'api_secret';
```

**Supported data formats:** `RawBLOB`, `JSONEachRow`, `CSV`, `TSV`, `Avro`, `ProtobufSingle`, `Protobuf`.

**Virtual columns available in Kafka external streams:**

| Column | Type | Description |
|--------|------|-------------|
| `_tp_time` | datetime64(3) | Message timestamp |
| `_tp_message_key` | string | Kafka message key |
| `_tp_shard` | int32 | Kafka partition |
| `_tp_sn` | int64 | Kafka offset |
| `_tp_message_headers` | map(string,string) | Kafka headers |

**Seek to position when reading:**
```sql
SELECT raw FROM kafka_raw SETTINGS seek_to = 'earliest';
SELECT raw FROM kafka_raw SETTINGS seek_to = '2025-01-01T00:00:00.000';
SELECT raw FROM kafka_raw SETTINGS shards  = '0,2';  -- specific partitions
```

### Pulsar

```sql
CREATE EXTERNAL STREAM IF NOT EXISTS pulsar_events (raw string)
SETTINGS
    type        = 'pulsar',
    service_url = 'pulsar://pulsar-broker:6650',
    topic       = 'persistent://public/default/my_topic',
    data_format = 'RawBLOB';
```

### Cross-Timeplus External Stream

```sql
CREATE EXTERNAL STREAM IF NOT EXISTS remote_events (id string, value float32)
SETTINGS
    type     = 'timeplus',
    address  = 'remote-timeplus-host:8463',
    stream   = 'source_stream',
    user     = 'default',
    password = '';
```

---

## 5. External Tables (ClickHouse, MySQL, PostgreSQL, S3)

External tables allow bounded historical reads from external systems.

```sql
-- ClickHouse
CREATE EXTERNAL TABLE IF NOT EXISTS ch_users
SETTINGS
    type     = 'clickhouse',
    address  = 'clickhouse:9000',
    user     = 'default',
    password = '',
    database = 'mydb',
    table    = 'users';

-- MySQL
CREATE EXTERNAL TABLE IF NOT EXISTS mysql_orders
SETTINGS
    type     = 'mysql',
    address  = 'mysql:3306',
    user     = 'root',
    password = 'secret',
    database = 'shop',
    table    = 'orders';

-- PostgreSQL
CREATE EXTERNAL TABLE IF NOT EXISTS pg_customers
SETTINGS
    type     = 'postgresql',
    address  = 'postgres:5432',
    user     = 'postgres',
    password = 'secret',
    database = 'crm',
    table    = 'customers';
```

Query external tables like any other table:
```sql
SELECT * FROM ch_users WHERE created_at > '2025-01-01';
```

---

## 6. Other Ingestion Methods

### Kafka Connect Source Connector
Deploy the Timeplus Kafka Connect sink connector to push data from Kafka into Timeplus.

### Redpanda Connect (Benthos)
Use the Timeplus output plugin for Redpanda Connect pipelines.

### JDBC/ODBC Drivers
Connect tools like DBeaver, Tableau, or custom Java apps via the ClickHouse-compatible JDBC driver on port 8123.

### SDK Libraries
- **Python**: `pip install timeplus` → `client.insert(stream, rows)`
- **Go**: `github.com/timeplus-io/go-proton-driver`
- **Java**: Use ClickHouse JDBC driver pointing to port 8123
- **Rust**: `timeplus-rs` crate
