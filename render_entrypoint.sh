#!/bin/bash

# Start the API
echo "Starting Application API..."
python start.py && python -m uvicorn app_api.main:app --host 0.0.0.0 --port 10000 &

# Start the Worker
echo "Starting Application Worker..."
# Run alembic migrations first
alembic upgrade head
python start.py && python app_worker/main.py &

# Generate Config from Env Vars
echo "Generating configuration..."
python render_config.py

# Start the Bot
echo "Starting Application Bot..."
python start.py && python app_bot/main.py &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
