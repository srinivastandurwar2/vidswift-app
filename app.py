from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import yt_dlp

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except:
        # jar templates madhe nasel tar root madhun de
        if os.path.exists('index.html'):
            return send_from_directory('.', 'index.html')
        else:
            return "<h1>VidSwift Live Aahe! ✅</h1><p>index.html sapdat nahi, templates folder madhe tak.</p>"

@app.route('/health')
def health():
    return "OK"

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({"status": "error", "error": "URL nahi"})
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return jsonify({"status": "success", "file": filename, "title": info.get('title')})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
