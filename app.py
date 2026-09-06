from flask import Flask, render_template, request, send_from_directory
import os, yt_dlp, uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    # FORM madhun URL ghe - JSON nahi
    url = request.form.get('url')
    if not url:
        return "Link tak bhava!", 400
    try:
        unique_id = str(uuid.uuid4())[:8]
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s_{unique_id}.%(ext)s',
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        # Direct file download de
        return send_from_directory(DOWNLOAD_FOLDER, os.path.basename(filename), as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)} <br><br><a href='/'>Parat ja</a>", 500

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
