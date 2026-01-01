#!/bin/bash
# Background README fetching with logging

LIMIT=${1:-55000}
DELAY=${2:-0.5}
LOG_FILE="logs/readme_fetch.log"
PID_FILE="logs/readme_fetch.pid"

echo "Starting README fetch in background..."
echo "Limit: $LIMIT repos"
echo "Delay: $DELAY seconds"
echo "Log: $LOG_FILE"
echo "PID will be written to $PID_FILE"

# Ensure logs directory exists
mkdir -p logs

# Activate virtual environment and run in background
nohup .venv/bin/python scripts/fetch_readmes.py --limit "$LIMIT" --delay "$DELAY" \
    > "$LOG_FILE" 2>&1 &

PID=$!
echo $PID > "$PID_FILE"

echo "Background process started: PID $PID"
echo "Monitor with: tail -f $LOG_FILE"
echo "Check status: python scripts/check_fetch_status.py"
echo "Stop with: kill $PID"
