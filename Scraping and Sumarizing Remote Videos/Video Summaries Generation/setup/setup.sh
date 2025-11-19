#!/bin/sh
# This script will run when the environment is initialized and restart the app if it fails.

echo "Setting up environment..."

cd /usercode/FILESYSTEM
source /bootstrap-apps/.virtualenvs/playwright/bin/activate

mkdir -p temp_resources

chmod 755 temp_resources

# Function to start the app
start_app() {
    while true; do
        echo "Starting application..."
        python app.py
        exit_code=$?
        
        if [ $exit_code -ne 0 ]; then
            echo "Application crashed with exit code $exit_code. Restarting in 5 seconds..."
            sleep 5
        else
            echo "Application terminated normally."
            break
        fi
    done
}

# Start the app with automatic restart
start_app