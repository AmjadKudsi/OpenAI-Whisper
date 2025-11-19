from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import shutil
from linkedin_service import LinkedInService
from google_drive_service import GoogleDriveService
from transcriber import MediaProcessorService
import tempfile

app = Flask(__name__)
TEMP_DIR = 'temp_resources'
os.makedirs(TEMP_DIR, exist_ok=True)

media_processor = MediaProcessorService()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process-url', methods=['POST'])
def process_url():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        temp_dir = tempfile.mkdtemp(dir=TEMP_DIR)
        
        if LinkedInService.is_linkedin_url(url):
            video_path = LinkedInService.download_video(url)
        elif GoogleDriveService.is_google_drive_url(url):
            video_path = GoogleDriveService.download_file(url)
        else:
            return jsonify({'error': 'Unsupported URL format'}), 400

        # Sanitize the filename - replace spaces and special characters
        original_filename = os.path.basename(video_path)
        safe_filename = ''.join(c for c in original_filename if c.isalnum() or c in '._-') 
        new_path = os.path.join(temp_dir, safe_filename)
        
        try:
            shutil.move(video_path, new_path)
        except Exception as e:
            print(f"Error moving file: {e}")
            try:
                shutil.copy2(video_path, new_path)
                os.unlink(video_path)
            except Exception as copy_error:
                print(f"Error during copy fallback: {copy_error}")
                raise
        
        original_dir = os.path.dirname(video_path)
        if original_dir != temp_dir and os.path.exists(original_dir):
            try:
                os.rmdir(original_dir)
            except Exception:
                pass

        duration = media_processor.get_audio_duration(new_path)
        
        # Get the path relative to TEMP_DIR
        relative_path = os.path.relpath(new_path, TEMP_DIR)
        
        return jsonify({
            'success': True,
            'filename': relative_path,
            'video_path': new_path,
            'duration': round(duration, 2) if duration else None
        })
    except Exception as e:
        import traceback
        print(f"Error processing URL: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


@app.route('/transcribe', methods=['POST'])
def transcribe_video():
    filename = request.json.get('file_path')  # This will now be just the filename
    if not filename:
        return jsonify({'error': 'No file path provided'}), 400
    
    try:
        # Construct the full path using the filename
        local_path = os.path.join(TEMP_DIR, filename)
        
        print(f"Transcribing file: {local_path}")
        print(f"File exists: {os.path.exists(local_path)}")
        
        if not os.path.exists(local_path):
            print(f"Contents of {TEMP_DIR}:")
            for root, dirs, files in os.walk(TEMP_DIR):
                for name in files:
                    print(os.path.join(root, name))
            return jsonify({'error': f'File not found: {local_path}'}), 404

        transcription = media_processor.transcribe_audio(local_path)
        if not transcription:
            return jsonify({'error': 'Transcription failed'}), 500

        duration = media_processor.get_audio_duration(local_path)
        
        return jsonify({
            'transcription': transcription,
            'duration': round(duration, 2) if duration else None
        })
    except Exception as e:
        import traceback
        print(f"Error during transcription: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


@app.route('/temp_resources/<path:filename>')
def serve_temp_file(filename):
    # Split the path into directory and filename
    directory = os.path.dirname(filename)
    basename = os.path.basename(filename)
    
    # Construct the full directory path
    full_dir = os.path.join(TEMP_DIR, directory) if directory else TEMP_DIR
    
    print(f"Serving file: {filename}")
    print(f"Full directory: {full_dir}")
    print(f"Basename: {basename}")
    
    return send_from_directory(full_dir, basename)


if __name__ == '__main__':
    app.run(port=3000, host='0.0.0.0', debug=True)