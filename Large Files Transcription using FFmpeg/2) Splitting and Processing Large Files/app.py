from flask import Flask, render_template, request, jsonify, send_from_directory
from transcriber import transcribe, get_audio_duration
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


def get_file_info():
    """Get information about available audio files including duration"""
    audio_files = {}
    base_dir = 'resources'
    
    for filename in os.listdir(base_dir):
        if filename.lower().endswith(('.mp3', '.mp4', '.wav')):
            file_path = os.path.join(base_dir, filename)
            duration = get_audio_duration(file_path)
            
            audio_files[file_path] = {
                'name': filename,
                'duration': round(duration, 2) if duration else None
            }
    
    return audio_files


@app.route('/')
def index():
    return render_template('index.html', audio_files=get_file_info())


@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    file_path = request.json.get('file_path')
    if not file_path:
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        transcription = transcribe(file_path)
        duration = get_audio_duration(file_path)
        
        return jsonify({
            'transcription': transcription,
            'duration': round(duration, 2) if duration else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/resources/<path:filename>')
def serve_audio(filename):
    return send_from_directory('resources', filename)


if __name__ == '__main__':
    app.run(port=3000, host='0.0.0.0', debug=True)