from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import os
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Set up Whisper model
model = whisper.load_model("base")

# Set the allowed file extensions
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac'}

# Load API key and Search Engine ID from environment variables
API_KEY = os.getenv("API_KEY") 
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")  

def allowed_file(filename):
    """Check if the uploaded file is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def transcribe_audio(file_path):
    """Transcribe audio using the Whisper model."""
    try:
        result = model.transcribe(file_path)
        return result['text']
    except Exception as e:
        return f"Error transcribing audio: {str(e)}"

def search_movie_transcription(transcription):
    """Search Google Custom Search API for transcription results, including images."""
    if not API_KEY or not SEARCH_ENGINE_ID:
        return "API key or Search Engine ID not configured properly."

    search_query = transcription  # The transcribed text from the audio
    url = f'https://www.googleapis.com/customsearch/v1?q={search_query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}&searchType=image'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'items' in data:
                results = []
                for item in data['items']:
                    title = item.get('title', 'No Title')
                    link = item.get('link', 'No Link')
                    snippet = item.get('snippet', 'No Description')
                    image = item.get('link', '')  # Use the direct link for images
                    results.append({
                        'title': title,
                        'link': link,
                        'snippet': snippet,
                        'image': image
                    })
                return results
            else:
                return []
        else:
            return f"Error with status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    """Handle audio upload, transcription, and search."""
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files['audio']
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            os.makedirs('uploads', exist_ok=True)
            file.save(file_path)

            # Transcribe the audio file using Whisper
            transcription = transcribe_audio(file_path)

            # Search for the movie based on the transcription text
            search_results = search_movie_transcription(transcription)

            # Clean up the uploaded file
            os.remove(file_path)

            # Return the transcription and search results
            return jsonify({
                "transcription": transcription,
                "search_results": {
                    "count": len(search_results) if isinstance(search_results, list) else 0,
                    "items": search_results if isinstance(search_results, list) else []
                }
            })
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid audio file format"}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
