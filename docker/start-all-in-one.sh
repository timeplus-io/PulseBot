#!/bin/bash
# Script to start all services in the correct order

set -e

# Default values
PULSEBOT_API_PORT="${PULSEBOT_API_PORT:-8001}"
TIMEPLUS_HOST="${TIMEPLUS_HOST:-localhost}"
TIMEPLUS_USER="${TIMEPLUS_USER:-pulsebot}"
TIMEPLUS_PASSWORD="${TIMEPLUS_PASSWORD:-}"

# Admin credentials used during initialization (not exposed to PulseBot)
PROTON_ADMIN_USER="${PROTON_ADMIN_USER:-proton}"
PROTON_ADMIN_PASSWORD="${PROTON_ADMIN_PASSWORD:-proton@t+}"
TIMEPLUS_ADMIN_USER="${TIMEPLUS_ADMIN_USER:-proton}"
TIMEPLUS_ADMIN_PASSWORD="${TIMEPLUS_ADMIN_PASSWORD:-timeplus@t+}"

echo "Starting all services..."

# Function to wait for a service to be ready
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    echo "Waiting for $service_name to be ready..."
    
    until curl -f "$url" > /dev/null 2>&1; do
        if [ $attempt -ge $max_attempts ]; then
            echo "ERROR: $service_name did not become ready in time"
            exit 1
        fi
        
        echo "Attempt $attempt/$max_attempts: $service_name not ready yet..."
        attempt=$((attempt + 1))
        sleep 2
    done
    
    echo "$service_name is ready!"
}

# Start services based on which image we're using
DB_PID=""
if [ -f "/entrypoint.sh" ]; then
    # Proton image
    echo "Starting Proton..."
    /entrypoint.sh &
    DB_PID=$!

    # Wait for Proton to be ready
    wait_for_service "http://localhost:8123/" "Proton"

    # Initialize PulseBot user for Proton
    echo "Initializing PulseBot user..."
    proton-client --user="$PROTON_ADMIN_USER" --password="$PROTON_ADMIN_PASSWORD" --query="CREATE USER IF NOT EXISTS pulsebot IDENTIFIED WITH plaintext_password BY '';" || true
    proton-client --user="$PROTON_ADMIN_USER" --password="$PROTON_ADMIN_PASSWORD" --query="GRANT CREATE DATABASE ON *.* TO pulsebot;" || true
    proton-client --user="$PROTON_ADMIN_USER" --password="$PROTON_ADMIN_PASSWORD" --query="GRANT ALL ON pulsebot.* TO pulsebot;" || true
    proton-client --user="$PROTON_ADMIN_USER" --password="$PROTON_ADMIN_PASSWORD" --query="GRANT ALL ON default.* TO pulsebot;" || true
elif [ -f "/timeplus/entrypoint.sh" ]; then
    # Timeplus Enterprise image
    echo "Starting Timeplus Enterprise..."
    /timeplus/entrypoint.sh &
    DB_PID=$!

    # Wait for Timeplus to be ready
    wait_for_service "http://localhost:8123/" "Timeplus Enterprise"

    # Initialize PulseBot user for Timeplus Enterprise
    echo "Initializing PulseBot user..."
    /timeplus/bin/timeplusd client --user="$TIMEPLUS_ADMIN_USER" --password="$TIMEPLUS_ADMIN_PASSWORD" --query="CREATE USER IF NOT EXISTS pulsebot IDENTIFIED WITH plaintext_password BY '';" || true
    /timeplus/bin/timeplusd client --user="$TIMEPLUS_ADMIN_USER" --password="$TIMEPLUS_ADMIN_PASSWORD" --query="GRANT CREATE DATABASE ON *.* TO pulsebot;" || true
    /timeplus/bin/timeplusd client --user="$TIMEPLUS_ADMIN_USER" --password="$TIMEPLUS_ADMIN_PASSWORD" --query="GRANT ALL ON pulsebot.* TO pulsebot;" || true
    /timeplus/bin/timeplusd client --user="$TIMEPLUS_ADMIN_USER" --password="$TIMEPLUS_ADMIN_PASSWORD" --query="GRANT ALL ON default.* TO pulsebot;" || true
else
    echo "ERROR: Unknown image type"
    exit 1
fi

# Export environment variables for PulseBot
export TIMEPLUS_HOST
export TIMEPLUS_USER
export TIMEPLUS_PASSWORD

# Start PulseBot API server in background
echo "Starting PulseBot API server on port $PULSEBOT_API_PORT..."
pulsebot serve --host 0.0.0.0 --port $PULSEBOT_API_PORT &
API_PID=$!

# Start PulseBot Agent in background
echo "Starting PulseBot Agent..."
pulsebot run &
AGENT_PID=$!

echo "All services started successfully!"
echo "PulseBot API is available at http://localhost:$PULSEBOT_API_PORT"
echo "Press Ctrl+C to stop all services"

# Wait for any process to exit
wait -n $DB_PID $API_PID $AGENT_PID

# Exit with status of process that exited first
exit $?