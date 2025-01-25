from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Set up Whisper model
model = whisper.load_model("base")

# Set the allowed file extensions
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files['audio']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        # Transcribe the audio file using Whisper
        transcription = transcribe_audio(file_path)

        # Clean up the uploaded file
        os.remove(file_path)

        return jsonify({"transcription": transcription})
    else:
        return jsonify({"error": "Invalid audio file format"}), 400

def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result['text']

if __name__ == "__main__":
    # Create the uploads folder if it doesn't exist
    os.makedirs('uploads', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
