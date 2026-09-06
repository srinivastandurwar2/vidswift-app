from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health():
    return "OK"
CORS(app)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return jsonify({"status": "success", "file": filename, "title": info.get('title')})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
