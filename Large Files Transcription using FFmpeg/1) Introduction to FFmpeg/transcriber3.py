# Your task is to modify the audio duration script so that it traverses the resources folder (non-recursively) and prints the audio durations for all files within that directory. Ensure you filter for only media files with appropriate extensions like .mp3, .mp4, .wav, etc.

import subprocess
import os


def get_audio_duration(file_path):
    """Get the duration of an audio file using ffprobe"""
    # TODO: Given the media file path, calculate its duration by calling `ffmpeg` on it using `subprocess.check_output`
    if not os.path.exists(file_path):
        print("File does not exist: {file_path}")
        return None
    
    try:
        output = subprocess.check_output(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                file_path
            ],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        duration = float(output.strip())
        return duration
    except (subprocess.CalledProcessError, ValueError, FileNotFoundError) as e:
        print(f"Failed to get duration for {file_path}: {e}")
        return None

def traverse_and_print_durations(directory):
    """Traverse the specified directory and print durations of media files"""

    valid_extensions = ('.mp3', '.mp4', '.wav')
    # TODO: Use `os.listdir(directory)` to get all files in the directory
    try:
        for entry in os.listdir(directory):
            file_path = os.path.join(directory, entry)
            if os.path.isfile(file_path) and entry.lower().endswith(valid_extensions):
                duration = get_audio_duration(file_path)
                if duration is not None:
                    print(f"Duration of {entry}: {int(duration)} seconds")
    except FileNotFoundError:
        print(f"Directory not found: {directory}")


if __name__ == "__main__":
    traverse_and_print_durations("resources")