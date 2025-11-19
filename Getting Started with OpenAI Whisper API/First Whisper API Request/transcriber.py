#Making Your First Whisper API Request
from openai import OpenAI

client = OpenAI()


def transcribe(file_path):
    """
    Transcribe an audio file using OpenAI's API.
    """
    try:
        with open(file_path, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            return transcript.text
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")