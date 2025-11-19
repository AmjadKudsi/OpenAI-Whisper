# Introduction to FFmpeg

import subprocess
from openai import OpenAI

client = OpenAI()


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
    cmd = [
        'ffprobe', 
        '-v', 'quiet',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        file_path
    ]
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return float(output)
    except subprocess.CalledProcessError:
        return None