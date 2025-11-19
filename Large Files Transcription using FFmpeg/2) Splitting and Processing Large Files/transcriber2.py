# Splitting and Processing Large Files with FFmpeg

import subprocess
import sys
import shutil
import os

from openai import OpenAI

client = OpenAI()


def check_ffmpeg_installed():
    """Check if FFmpeg is installed and accessible."""
    if shutil.which("ffmpeg") is None:
        print("FFmpeg is not installed or not in the system path.", file=sys.stderr)
        sys.exit(1)


def transcribe(file_path):
    """
    Transcribe an audio file using OpenAI's Whisper API.
    """
    try:
        with open(file_path, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                timeout=60
            )
            return transcript.text
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")


def get_audio_duration(file_path):
    """Get the duration of an audio file using ffprobe"""

    # TODO: Add FFmpeg command
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey1',
        file_path
    ]
    try:
        output = subprocess.check_output(cmd)
        return float(output)
    except:
        return None


# Function to split media into chunks and log the process
def split_into_chunks(file_path, start_time, duration, chunk_number):
    temp_file_path = f"resources/chunk_{chunk_number}.mp3"
    
    # TODO: Add FFmpeg command
    cmd = [
        'ffmpeg',
        '-i', file_path,
        '-ss', str(start_time),
        '-t', str(duration),
        '-c', 'copy',
        '-y',
        temp_file_path
    ]
    
    # Redirect stderr to stdout
    return_code = subprocess.call(cmd, stderr=subprocess.STDOUT)
    
    if return_code != 0:
        print(f"Encoding failed for chunk {chunk_number}.", file=sys.stderr)
        sys.exit(1)

    return temp_file_path

# Check if FFmpeg is installed before attempting to split
check_ffmpeg_installed()

# Split the media file starting from the 30th second into a 60-second chunk as an example
print(f"Chunk saved at: {split_into_chunks('resources/sample_audio.mp3', 5, 10, 1)}")