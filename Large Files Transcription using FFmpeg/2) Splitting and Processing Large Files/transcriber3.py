# Fill in the missing parts of the code corresponding to proper FFmpeg commands to split the given media file into 5 equal-duration chunks. Each chunk should be saved in the resources folder. Hint: To convert the output chunk to mp3 given the input file in mp4, provide -acodec libmp3lame parameter to FFmpeg - it will retrieve the chunk in mp3 format.

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


def split_into_chunks(file_path):
    """Split the media file into 5 equal-duration chunks."""
    print("\nSplitting media into chunks...")
    
    duration = get_audio_duration(file_path)
    if not duration:
        raise Exception("Could not determine audio duration")
        
    num_chunks = 5
    chunk_duration = duration / num_chunks  
    
    resources_dir = os.path.dirname(file_path)

    for i in range(num_chunks):
        start_time = i * chunk_duration
        output_file = os.path.join(resources_dir, f"codesignal_beyond_chunk_{i+1}.mp3")

        cmd = [
            "ffmpeg",
            "-y",
            "-ss", str(start_time),        # seek first (faster)
            "-i", file_path,
            "-t", str(chunk_duration),
            "-vn",
            "-acodec", "libmp3lame",
            output_file
        ]

        subprocess.run(cmd, check=True)



if __name__ == "__main__":
    check_ffmpeg_installed()
    split_into_chunks('resources/codesignal_beyond.mp4')