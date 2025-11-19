from flask import Flask, render_template, request, jsonify, send_from_directory
from transcriber import transcribe
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Sample audio files (in practice, you'd scan a directory or use a database)
AUDIO_FILES = {
    'resources/sample_audio.mp3': 'Sample MP3 Audio',
    'resources/sample_video.mp4': 'Sample MP4 Video',
}

@app.route('/')
def index():
    return render_template('index.html', audio_files=AUDIO_FILES)


@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    file_path = request.json.get('file_path')
    if not file_path:
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        transcription = transcribe(file_path)
        return jsonify({'transcription': transcription})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/resources/<path:filename>')
def serve_audio(filename):
    return send_from_directory('resources', filename)
    try:
        transcription = transcribe(file_path)
        return jsonify({'transcription': transcription})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=3000, host='0.0.0.0', debug=True)
