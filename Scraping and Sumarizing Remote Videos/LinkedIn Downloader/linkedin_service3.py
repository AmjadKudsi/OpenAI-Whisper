# Please keep in mind that in some countries, downloading and using LinkedIn videos might lead to legal consequences if done without proper authorization.
import os
import tempfile
from urllib.parse import urlparse
import yt_dlp


class LinkedInService:
    @staticmethod
    def is_linkedin_url(url):
        """Check if the given string is a LinkedIn URL"""
        try:
            parsed = urlparse(url)
            valid_paths = [
                '/feed/update/urn:li:activity:',  # Existing format
                '/posts/'  # New format to support
            ]
            return 'linkedin.com' in parsed.netloc and any(path in parsed.path for path in valid_paths)
        except Exception:
            return False

    @staticmethod
    def download_video(url):
        """Download LinkedIn video using yt-dlp and return path to downloaded file"""
        print("Downloading LinkedIn video...")
        
        temp_dir = tempfile.mkdtemp()
        output_template = os.path.join(temp_dir, '%(title)s.%(ext)s')
        
        try:
            # TODO: Define yt-dlp options:
            ytdlp_options = {
                'format': 'mp4', # mp4 format
                'outtmpl': output_template, # template for the output file name
                'quiet': True,
                'no_warnings': True,
                'progress': True,
            }

            # TODO: Create `YoutubeDL` instance based on options and call a `download` method on it
            with yt_dlp.YoutubeDL(ytdlp_options) as ydl:
                ydl.download([url])

            # TODO: Retrieve the downloaded file name based on the specified location
            # For easier search, you can use a temporary directory in the `outtmpl` property that's empty before calling `download`                
                
            files = os.listdir(temp_dir)
            if not files:
                raise Exception("No file downloaded")
                
            return os.path.join(temp_dir, files[0])
            
            # TODO: Don't forget to handle potential errors and exceptions properly
            
        except Exception as e:
            print (f"Error downloading video: {e}")
            raise ValueError(f"Failed to download LinkedIn video: {repr(e)}")
