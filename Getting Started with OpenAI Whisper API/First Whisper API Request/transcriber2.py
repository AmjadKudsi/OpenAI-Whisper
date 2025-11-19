# Making Your First Whisper API Request
from openai import OpenAI
import requests

# TODO: Define the OpenAI client
client = OpenAI()


def transcribe_remote(url):
    """
    Transcribe a remote video file from a URL using OpenAI's Whisper API.
    """
    try:
        # TODO: Download the content using the `requests` library
        response = requests.get(url)		# fetches the remote file.
        response.raise_for_status()			# stops execution if the request failed.
        content = response.content			# contains the raw bytes of the MP4 video.
        
        # TODO: Send the content to OpenAI API
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=("video.mp4", content)		# a tuple containing a filename (with its format) and the raw bytes.
        )
        return transcript.text
        
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    remote_video_url = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4"
    print(transcribe_remote(remote_video_url))