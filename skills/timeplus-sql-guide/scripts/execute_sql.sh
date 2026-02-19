#!/usr/bin/env bash
# execute_sql.sh — Execute Timeplus SQL via the ClickHouse-compatible HTTP interface
#
# Usage:
#   ./execute_sql.sh "SELECT version()"
#   ./execute_sql.sh "SELECT * FROM table(my_stream) LIMIT 10" JSONEachRow
#   echo "CREATE STREAM ..." | ./execute_sql.sh
#   cat query.sql | ./execute_sql.sh - JSONEachRow
#
# Required environment variables:
#   TIMEPLUS_HOST      — hostname or IP (default: localhost)
#   TIMEPLUS_USER      — username (default: default)
#   TIMEPLUS_PASSWORD  — password (default: empty)
#
# Optional environment variables:
#   TIMEPLUS_PORT      — HTTP port (default: 8123)

set -euo pipefail

TIMEPLUS_HOST="${TIMEPLUS_HOST:-localhost}"
TIMEPLUS_USER="${TIMEPLUS_USER:-default}"
TIMEPLUS_PASSWORD="${TIMEPLUS_PASSWORD:-}"
TIMEPLUS_PORT="${TIMEPLUS_PORT:-8123}"

BASE_URL="http://${TIMEPLUS_HOST}:${TIMEPLUS_PORT}/"

# ── Health check ────────────────────────────────────────────────────────────────
if [[ "${1:-}" == "--health" ]]; then
  echo "Checking Timeplus at ${BASE_URL} ..."
  response=$(curl -sf -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" "${BASE_URL}" || echo "FAILED")
  if [[ "$response" == "Ok." ]]; then
    echo "✅ Timeplus is healthy at ${BASE_URL}"
  else
    echo "❌ Timeplus health check failed. Response: ${response}"
    exit 1
  fi
  exit 0
fi

# ── Format argument ──────────────────────────────────────────────────────────────
FORMAT="${2:-TabSeparated}"
FORMAT_PARAM=""
if [[ -n "$FORMAT" ]]; then
  FORMAT_PARAM="?default_format=${FORMAT}"
fi

# ── Read SQL from argument or stdin ─────────────────────────────────────────────
if [[ "${1:-}" == "-" ]] || [[ "${1:-}" == "" ]]; then
  # Read from stdin
  SQL_INPUT="$(cat)"
elif [[ -f "${1:-}" ]]; then
  # File path provided
  SQL_INPUT="$(cat "$1")"
else
  # SQL provided directly as argument
  SQL_INPUT="$1"
fi

if [[ -z "$SQL_INPUT" ]]; then
  echo "Usage: $0 \"<SQL>\" [format]" >&2
  echo "       echo \"<SQL>\" | $0 - [format]" >&2
  echo "       cat query.sql | $0 [format]" >&2
  exit 1
fi

# ── Execute ──────────────────────────────────────────────────────────────────────
echo "${SQL_INPUT}" | curl -sf "${BASE_URL}${FORMAT_PARAM}" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
