# verify a Google Drive URL and extract the file ID, if available
from urllib.parse import urlparse, parse_qs

class GoogleDriveVideoDownloader:
    @staticmethod
    def extract_and_verify(file_url):
        parsed = urlparse(file_url)
        # TODO: Implement the missing part for parsing document id from the URL
        
        if 'drive.google.com' in parsed.netloc:
            path_parts = parsed.path.strip("/").split("/")

            # Pattern 1: /file/d/<id>/view
            if len(path_parts) >= 3 and path_parts[0] == "file" and path_parts[1] == "d":
                return path_parts[2]

            # Pattern 2: /open?id=<id>
            if parsed.path == "/open":
                query = parse_qs(parsed.query)
                return query.get("id", [None])[0]
                    
        return None

# Test cases
url1 = "https://drive.google.com/file/d/0B8ZoywgQPrLWTGJSZndfekVRMME/view"
url2 = "https://drive.google.com/open?id=0B8ZoywgQPrLWTGJSZndfekVRMME"
url3 = "https://drive.google.com/open/0B8ZoywgQPrLWTGJSZndfekVRMME"
url4 = "https://drive.youtube.com/open?id=0B8ZoywgQPrLWTGJSZndfekVRMME"
print(GoogleDriveVideoDownloader.extract_and_verify(url1))  # Should print: '0B8ZoywgQPrLWTGJSZndfekVRMME'
print(GoogleDriveVideoDownloader.extract_and_verify(url2))  # Should print: '0B8ZoywgQPrLWTGJSZndfekVRMME'
print(GoogleDriveVideoDownloader.extract_and_verify(url3))  # Should print: None
print(GoogleDriveVideoDownloader.extract_and_verify(url4))  # Should print: None