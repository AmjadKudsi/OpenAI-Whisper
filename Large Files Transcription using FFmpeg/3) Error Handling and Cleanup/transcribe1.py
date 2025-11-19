# The goal is to provide a robust solution that efficiently handles these errors and ensures temporary files are cleaned up at the end of the transcription process.

import math
import os
import subprocess
import tempfile
import random

from openai import OpenAI

client = OpenAI()


def run_command_with_output(cmd, desc=None):
    """Run a command and stream its output in real-time"""
    if desc:
        print(f"\n{desc}")
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    for line in iter(process.stdout.readline, ''):
        print(line, end='')
    
    process.stdout.close()
    return_code = process.wait()

    if return_code != 0:
        raise subprocess.CalledProcessError(return_code, cmd)


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
        output = subprocess.check_output(cmd)
        return float(output)
    except:
        return None


def split_media(file_path, chunk_size_mb=20):
    """Split media file into chunks smaller than the API limit"""
    duration = get_audio_duration(file_path)
    
    if not duration:
        raise Exception("Could not determine media duration")
    
    file_size = os.path.getsize(file_path)
    chunk_duration = duration * (chunk_size_mb * 1024 * 1024) / file_size
    num_chunks = math.ceil(duration / chunk_duration)
    
    chunks = []
    for i in range(num_chunks):
        start_time = i * chunk_duration
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(file_path)[1]
        )
        
        cmd = [
            'ffmpeg',
            '-i', file_path,
            '-ss', str(start_time),
            '-t', str(chunk_duration),
            '-c', 'copy',
            '-y',
            temp_file.name
        ]
        
        run_command_with_output(
            cmd, 
            f"Extracting chunk {i + 1}/{num_chunks}"
        )
        chunks.append(temp_file.name)
    print(f"Split media into {len(chunks)} chunk(s): {chunks}")
    return chunks


def cleanup_temp_files(file_path):
    """Clean up temporary files and directories"""
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            for root, dirs, files in os.walk(file_path, topdown=False):
                for name in files:
                    os.unlink(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(file_path)
    except Exception as e:
        print(f"Warning: Could not clean up {file_path}: {e}")


def transcribe_small_media(file_path):
    """
    Transcribe an media file using OpenAI's Whisper API.
    Simulate occasional errors to mimic real-world API failures.
    """
    try:
        # Randomly throw an exception to simulate API failure
        if random.randint(1, 3) == 1: # 33% chance
            raise Exception("Simulated API failure")
        
        with open(file_path, 'rb') as media_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=media_file,
                timeout=60
            )
            return transcript.text
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")


def transcribe(file_path):
    """ Transcribe a large media file by splitting it into chunks """
    chunks = []
    try:
        chunks = split_media(file_path) # 20Mb chunks
        transcriptions = []
        
        for chunk_id, chunk in enumerate(chunks):
            try:
                print(f"Transcribing chunk {chunk_id + 1}/{len(chunks)} via Whisper API...")
                text = transcribe_small_media(chunk)
            except Exception as e:
                print(e)
                text = None
            if text:
                transcriptions.append(text)
        return ' '.join(transcriptions)
    except Exception as e:
        print(f"Error processing large file: {e}")
        return None
    finally:
        # Clean up all chunks in finally block
        for chunk in chunks:
            cleanup_temp_files(chunk)