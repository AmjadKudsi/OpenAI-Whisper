#!/bin/sh
# This script will be run when the environment is initialized.
# Add any setup logic here.

echo "Setting up environment…"

cd /usercode/FILESYSTEM

source /bootstrap-apps/.virtualenvs/playwright/bin/activate

mkdir -p resources

wget https://assets.s3.amazonaws.com/uploads/1736399347134/sample_video.mp3 -O 'resources/sample_audio.mp3'
wget https://assets.s3.amazonaws.com/uploads/1736399347656/sample_video.mp4 -O 'resources/sample_video.mp4'

python app.py