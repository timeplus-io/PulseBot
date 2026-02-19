#!/usr/bin/env bash
# ingest.sh — Push JSON data into a Timeplus stream via the REST Ingest API (port 3218)
#
# Usage:
#   ./ingest.sh <stream_name> '{"columns":["col1","col2"],"data":[[v1,v2],[v3,v4]]}'
#   echo '{"columns":["col1"],"data":[["val"]]}' | ./ingest.sh <stream_name>
#
# Required environment variables:
#   TIMEPLUS_HOST      — hostname or IP (default: localhost)
#   TIMEPLUS_USER      — username (default: default)
#   TIMEPLUS_PASSWORD  — password (default: empty)
#
# Optional environment variables:
#   TIMEPLUS_INGEST_PORT — ingest API port (default: 3218)
#
# Payload format:
#   {
#     "columns": ["col1", "col2", ...],
#     "data": [[row1_val1, row1_val2], [row2_val1, row2_val2], ...]
#   }

set -euo pipefail

TIMEPLUS_HOST="${TIMEPLUS_HOST:-localhost}"
TIMEPLUS_USER="${TIMEPLUS_USER:-default}"
TIMEPLUS_PASSWORD="${TIMEPLUS_PASSWORD:-}"
TIMEPLUS_INGEST_PORT="${TIMEPLUS_INGEST_PORT:-3218}"

STREAM_NAME="${1:-}"
if [[ -z "$STREAM_NAME" ]]; then
  echo "Usage: $0 <stream_name> [json_payload]" >&2
  exit 1
fi

# Read payload from second arg or stdin
if [[ -n "${2:-}" ]]; then
  PAYLOAD="$2"
else
  PAYLOAD="$(cat)"
fi

if [[ -z "$PAYLOAD" ]]; then
  echo "Error: no JSON payload provided" >&2
  exit 1
fi

INGEST_URL="http://${TIMEPLUS_HOST}:${TIMEPLUS_INGEST_PORT}/proton/v1/ingest/streams/${STREAM_NAME}"

curl -sf -X POST "$INGEST_URL" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD"

echo ""
echo "✅ Data ingested into stream: ${STREAM_NAME}"
