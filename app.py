from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS
import yt_dlp
import os
import urllib.parse

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return render_template('https://donvidtik.vercel.app')

@app.route('/music')
def music():
    return render_template('#')

@app.route('/contact')
def contact():
    return render_template('#')

@app.route('/download', methods=['POST'])
def download():
    if request.is_json:
        data = request.get_json()
        url = data.get('url', '')
    else:
        url = request.form.get('url', '')

    if not url:
        return jsonify({'error': 'URL parameter missing'}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'static/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info_dict)
            mp3_file = file_name.rsplit('.', 1)[0] + '.mp3'

            # Ambil judul dan thumbnail dari info_dict
            title = info_dict.get('title', 'No Title')
            thumbnail_url = info_dict.get('thumbnail', '')

            # Encode URL file MP3
            audio_url = urllib.parse.quote(f'/static/{os.path.basename(mp3_file)}')

    except Exception as e:
        return jsonify({'error': f'Error downloading audio: {str(e)}'}), 500

    return jsonify({
        'title': title,
        'thumbnailUrl': thumbnail_url,
        'audioUrl': audio_url,
    })

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(host='0.0.0.0', port=3000, debug=True)
