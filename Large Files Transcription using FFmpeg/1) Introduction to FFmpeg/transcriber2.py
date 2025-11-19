# Your task is to modify the get_audio_duration function to use subprocess.check_output and add proper error handling for cases when the file doesn't exist or when ffprobe fails.
import subprocess
import os


def get_audio_duration(file_path):
    """Get the duration of an audio file using ffprobe"""
    # cmd = f'ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{file_path}"'
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        file_path
    ]
    
    #return float(output) if output else None    
    #output = os.system(cmd)
    #return float(output) if output else None
    try:
        output = subprocess.check_output(cmd, stderr= subprocess.STDOUT)
        return float(output)
    except subprocess.CalledProcessError:
        return None    
    

if __name__ == "__main__":
    # Example usage
    test_file = "resources/sample_audio.mp3"
    duration = get_audio_duration(test_file)
    if duration:
        print(f"Duration of {test_file}: {duration:.2f} seconds")
    else:
        print(f"Could not determine duration of {test_file}")