from flask import Flask, render_template, request, send_from_directory
import os, yt_dlp, uuid

app = Flask(__name__)
os.makedirs("downloads", exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url','').strip()
    if not url:
        return "<h3>Link taka bhava!</h3><a href='/'>Parat ja</a>", 400

    try:
        # Unique name
        uid = uuid.uuid4().hex[:6]
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'downloads/%(title)s_{uid}.%(ext)s',
            'noplaylist': True,
            'merge_output_format': 'mp4',
            # BOT BYPASS - saglya platform sathi
            'extractor_args': {
                'youtube': {'player_client': ['android','ios','web']},
                'facebook': {'player_client': ['android']},
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
            },
            'no_check_certificate': True,
            'quiet': True,
        }

        # Jar cookies.txt file asel tar vapra (Instagram sathi khup mahatvacha)
        if os.path.exists('cookies.txt'):
            ydl_opts['cookiefile'] = 'cookies.txt'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # merge zalyavar extension badalto
            base = os.path.splitext(filename)[0]
            # mp4 shodha
            for f in os.listdir('downloads'):
                if uid in f:
                    filename = os.path.join('downloads', f)
                    break

        return send_from_directory('downloads', os.path.basename(filename), as_attachment=True)

    except Exception as e:
        err = str(e)
        msg = f"<h3>Error: {err}</h3>"
        if "bot" in err.lower() or "sign in" in err.lower():
            msg += "<p>YouTube ne IP block kela. 2 min nantar parat try kara.</p>"
        if "login" in err.lower() or "cookies" in err.lower():
            msg += "<p>Instagram la cookies lagtat. Khali sangto kasa karaycha.</p>"
        msg += "<br><a href='/'>Parat ja</a>"
        return msg, 500

@app.route('/health')
def health(): return "OK - Insta FB YT Ready"
