import os
import tempfile
from urllib.parse import urlparse
import yt_dlp


class LinkedInService:
    @staticmethod
    def is_linkedin_url(url):
        parsed = urlparse(url)
        valid_paths = [
            '/feed/update/urn:li:activity:',  # Existing format
            '/posts/'  # New format to support
        ]
        return 'linkedin.com' in parsed.netloc and any(path in parsed.path for path in valid_paths)

    @staticmethod
    def download_video(url):
        """Download LinkedIn video using yt-dlp and return path to downloaded file"""
        print("Downloading LinkedIn video... 'cookies.txt' existence: " + str(os.path.exists('cookies.txt')))
        
        # Create temporary directory for download
        temp_dir = tempfile.mkdtemp()
        output_template = os.path.join(temp_dir, '%(title)s.%(ext)s')
        
        try:
            # Download video using yt-dlp
            ydl_opts = {
                'format': 'mp4',
                'outtmpl': output_template,
                'quiet': True,
                'no_warnings': True,
                'progress': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Find the downloaded file
            files = os.listdir(temp_dir)
            if not files:
                raise Exception("No file downloaded")
            
            return os.path.join(temp_dir, files[0])
        except Exception as e:
            print(f"Error downloading video: {e}")
            raise ValueError(f"Failed to download LinkedIn video: {str(e)}")