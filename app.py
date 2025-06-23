from flask import Flask, request, render_template, send_from_directory
import os
import whisper
from whisper.utils import get_writer
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_DIR = 'uploads'
SUBS_DIR = 'subs'
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(SUBS_DIR, exist_ok=True)

# Load Whisper model on startup
model = whisper.load_model("base")

@app.route('/', methods=['GET', 'POST'])
def index():
    subtitle_url = None
    error = None

    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            error = "No file selected"
        else:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_DIR, filename)
            file.save(file_path)

            try:
                # Transcribe & Translate (like your code)
                result = model.transcribe(file_path, language="en", task="translate")

                # Write subtitles
                base_filename = os.path.splitext(filename)[0]
                writer = get_writer("srt", SUBS_DIR)
                writer(result, base_filename)

                subtitle_url = f'/subs/{base_filename}.srt'

            except Exception as e:
                error = f"Error processing file: {e}"

    return render_template("index.html", subtitle_url=subtitle_url, error=error)

@app.route('/subs/<path:filename>')
def download_subtitle(filename):
    return send_from_directory(SUBS_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
