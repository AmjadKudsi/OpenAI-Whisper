#!/bin/sh
# This script will run when the environment is initialized and restart the app if it fails.

echo "Setting up environment..."

cd /usercode/FILESYSTEM

source /bootstrap-apps/.virtualenvs/playwright/bin/activate

mkdir -p resources

# Download resources
wget https://codesignal-assets.s3.amazonaws.com/uploads/1736399347134/sample_video.mp3 -O 'resources/sample_audio.mp3'
wget https://codesignal-assets.s3.amazonaws.com/uploads/1736399347656/sample_video.mp4 -O 'resources/sample_video.mp4'
wget https://codesignal-assets.s3.us-east-1.amazonaws.com/uploads/learn/openai-whisper/codesignal_cosmo_feedback.mp4 -O 'resources/codesignal_cosmo_feedback.mp4'
wget 'https://codesignal-assets.s3.us-east-1.amazonaws.com/uploads/learn/openai-whisper/codesignal_conversation_practice+.mp4' -O 'resources/codesignal_conversation_practice.mp4'
wget https://codesignal-assets.s3.us-east-1.amazonaws.com/uploads/learn/openai-whisper/codesignal_beyond.mp4 -O 'resources/codesignal_beyond.mp4'
wget https://codesignal-assets.s3.us-east-1.amazonaws.com/uploads/learn/openai-whisper/codesignal_ai_interviewer_sales.mp4 -O 'resources/codesignal_ai_interviewer_sales.mp4'

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