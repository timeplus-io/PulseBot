# Sending Data Out of Timeplus

## Overview

Data flows out of Timeplus through:

1. **External Streams** → write back to Kafka / Pulsar
2. **External Tables** → write to ClickHouse, MySQL, PostgreSQL, S3
3. **Materialized Views → External target** — continuous push pipeline
4. **Query results** → curl HTTP response (pull)
5. **REST API** — query endpoint for applications
6. **Sinks** (Enterprise Cloud) — built-in connectors to Slack, webhooks, email, etc.

---

## 1. Write to Kafka via External Stream

Create a Kafka external stream as the write target, then route data into it
via a materialized view or a direct `INSERT INTO`.

### Step 1: Create the Kafka output external stream

```sql
CREATE EXTERNAL STREAM IF NOT EXISTS kafka_alerts_out (
    device_id   string,
    temperature float32,
    alert_level string,
    ts          datetime64(3)
)
SETTINGS
    type        = 'kafka',
    brokers     = 'kafka-broker:9092',
    topic       = 'device_alerts',
    data_format = 'JSONEachRow';
```

### Step 2: Continuously push alerts into Kafka

```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_push_alerts
INTO kafka_alerts_out AS
SELECT
    device_id,
    temperature,
    CASE WHEN temperature > 40 THEN 'critical'
         WHEN temperature > 30 THEN 'warning'
         ELSE 'ok' END AS alert_level,
    _tp_time AS ts
FROM sensor_data
WHERE temperature > 30;
```

### Write RawBLOB (single string column) to Kafka

```sql
CREATE EXTERNAL STREAM IF NOT EXISTS kafka_raw_out (raw string)
SETTINGS
    type        = 'kafka',
    brokers     = 'kafka-broker:9092',
    topic       = 'output_topic',
    data_format = 'RawBLOB';

-- Write JSON-formatted strings
CREATE MATERIALIZED VIEW mv_to_kafka INTO kafka_raw_out AS
SELECT to_string(map('id', order_id, 'amount', to_string(amount))) AS raw
FROM orders;
```

### Write with Kafka message key

```sql
CREATE EXTERNAL STREAM IF NOT EXISTS kafka_keyed_out (
    _tp_message_key string,   -- becomes the Kafka message key
    payload         string
)
SETTINGS
    type        = 'kafka',
    brokers     = 'kafka-broker:9092',
    topic       = 'keyed_output',
    data_format = 'JSONEachRow';

CREATE MATERIALIZED VIEW mv_keyed INTO kafka_keyed_out AS
SELECT user_id AS _tp_message_key, to_json(event) AS payload
FROM user_events;
```

---

## 2. Write to ClickHouse via External Table

### Create the external table pointing to ClickHouse

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS ch_alerts
SETTINGS
    type     = 'clickhouse',
    address  = 'clickhouse:9000',
    user     = 'default',
    password = '',
    database = 'analytics',
    table    = 'device_alerts';
```

### Continuously push into ClickHouse

```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_to_clickhouse
INTO ch_alerts AS
SELECT
    device_id,
    temperature,
    now64(3) AS alert_time
FROM sensor_data
WHERE temperature > 35;
```

---

## 3. Write to MySQL / PostgreSQL

```sql
-- MySQL sink
CREATE EXTERNAL TABLE IF NOT EXISTS mysql_events
SETTINGS
    type     = 'mysql',
    address  = 'mysql:3306',
    user     = 'root',
    password = 'secret',
    database = 'app_db',
    table    = 'processed_events';

-- PostgreSQL sink
CREATE EXTERNAL TABLE IF NOT EXISTS pg_summaries
SETTINGS
    type     = 'postgresql',
    address  = 'postgres:5432',
    user     = 'postgres',
    password = 'secret',
    database = 'analytics',
    table    = 'hourly_summaries';
```

---

## 4. Write to S3 / Object Storage (via External Table)

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS s3_archive
SETTINGS
    type       = 's3',
    url        = 's3://my-bucket/timeplus/events/',
    aws_access_key_id     = 'AKIAIOSFODNN7EXAMPLE',
    aws_secret_access_key = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    format     = 'Parquet';
```

---

## 5. Webhook / HTTP Sink (via Remote UDF or Materialized View)

For HTTP webhooks, use a remote UDF as the push mechanism:

```sql
-- Create a remote function that POSTs to your webhook
CREATE REMOTE FUNCTION send_alert(payload string)
RETURNS string
URL 'https://hooks.slack.com/services/xxx/yyy/zzz'
AUTH_METHOD 'none';

-- Call in a streaming query or view
SELECT send_alert(
    concat('{"text":"Alert: device ', device_id, ' temp=', to_string(temperature), '"}')
)
FROM sensor_data
WHERE temperature > 40;
```

---

## 6. Pull Query Results via curl

Applications can pull results by sending a query to port 8123.

```bash
# Pull latest aggregated data
echo "SELECT region, sum(amount) AS revenue
FROM table(orders)
WHERE _tp_time > now() - INTERVAL 1 HOUR
GROUP BY region
ORDER BY revenue DESC" | \
curl "http://${TIMEPLUS_HOST}:8123/?default_format=JSONEachRow" \
  -H "X-ClickHouse-User: ${TIMEPLUS_USER}" \
  -H "X-ClickHouse-Key: ${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

**Output formats for downstream consumption:**

```bash
# CSV output
echo "SELECT * FROM table(alerts) LIMIT 100" | \
curl "http://${TIMEPLUS_HOST}:8123/?default_format=CSV" \
  -H "X-ClickHouse-User: ${TIMEPLUS_USER}" \
  -H "X-ClickHouse-Key: ${TIMEPLUS_PASSWORD}" \
  --data-binary @-

# JSON output with schema
echo "SELECT * FROM table(alerts) LIMIT 100" | \
curl "http://${TIMEPLUS_HOST}:8123/?default_format=JSON" \
  -H "X-ClickHouse-User: ${TIMEPLUS_USER}" \
  -H "X-ClickHouse-Key: ${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

---

## 7. Enterprise Cloud Sinks

In Timeplus Enterprise Cloud, built-in sink connectors are available via the UI
or API. These include:

- **Kafka / Confluent / Redpanda** — streaming output
- **Slack** — alert notifications
- **Webhook** — HTTP POST to any endpoint
- **Email** — SMTP alerts
- **ClickHouse** — batch or streaming write
- **Amazon Kinesis** — AWS streaming
- **Timeplus Cloud (cross-tenant)** — multi-region replication

Create sinks via the Timeplus REST Management API:

```bash
curl -X POST "http://${TIMEPLUS_HOST}:8000/api/v1beta2/sinks" \
  -H "Authorization: ApiKey ${TIMEPLUS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "slack_alerts",
    "type": "slack",
    "query": "SELECT * FROM alerts WHERE severity = '"'"'critical'"'"'",
    "properties": {
      "url": "https://hooks.slack.com/services/xxx/yyy/zzz"
    }
  }'
```

---

## 8. Common Full Pipeline Example

```sql
-- Full end-to-end: Kafka in → enrich → alert → Kafka out

-- 1. Input external stream (Kafka)
CREATE EXTERNAL STREAM kafka_iot_in (raw string)
SETTINGS type='kafka', brokers='kafka:9092', topic='iot_raw', data_format='RawBLOB';

-- 2. Native stream for enriched events
CREATE STREAM enriched_events (
    device_id   string,
    temperature float32,
    location    string,
    alert_level string
);

-- 3. Parse and enrich via materialized view
CREATE MATERIALIZED VIEW mv_parse_and_enrich INTO enriched_events AS
SELECT
    raw:device_id    AS device_id,
    to_float(raw:temp)   AS temperature,
    raw:location     AS location,
    CASE
        WHEN to_float(raw:temp) > 40 THEN 'critical'
        WHEN to_float(raw:temp) > 30 THEN 'warning'
        ELSE 'ok'
    END AS alert_level
FROM kafka_iot_in;

-- 4. Output external stream (Kafka)
CREATE EXTERNAL STREAM kafka_alerts_out (
    device_id string, temperature float32, alert_level string
)
SETTINGS type='kafka', brokers='kafka:9092', topic='iot_alerts', data_format='JSONEachRow';

-- 5. Push only alerts to Kafka
CREATE MATERIALIZED VIEW mv_push_critical INTO kafka_alerts_out AS
SELECT device_id, temperature, alert_level
FROM enriched_events
WHERE alert_level IN ('critical', 'warning');
```
