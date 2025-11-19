# Making Your First Whisper API Request

from openai import OpenAI
import requests
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# URL of the mp3 file
url = "https://dare.wisc.edu/wp-content/uploads/sites/1051/2008/04/Arthur.mp3"

# TODO: Download the mp3 file from the URL
response = requests.get(url)
response.raise_for_status()
file_path = "Arthur.mp3"
with open(file_path, "wb") as f:
    f.write(response.content)

# TODO: Open the audio file in binary mode
with open(file_path, "rb") as audio_file:

# TODO: Create a transcription request with a timeout and specific model
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        timeout=30
    )

# TODO: Print the transcribed text
print(transcript.text)
