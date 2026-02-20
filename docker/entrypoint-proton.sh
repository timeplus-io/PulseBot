#!/bin/bash
# Entrypoint for Proton-based all-in-one image

# Set default environment variables
export TIMEPLUS_HOST="${TIMEPLUS_HOST:-localhost}"
export TIMEPLUS_USER="${TIMEPLUS_USER:-pulsebot}"
export TIMEPLUS_PASSWORD="${TIMEPLUS_PASSWORD:-}"

# If no command is provided, start all services
if [ $# -eq 0 ]; then
    exec /usr/local/bin/start-all-in-one.sh
else
    # Otherwise, execute the provided command
    exec "$@"
fi