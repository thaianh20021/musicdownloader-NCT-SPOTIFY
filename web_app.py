from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os
import threading

# Import downloader modules
from nct_downloader import download_nct
from spotify_downloader import download_spotify

app = Flask(__name__)
# Enable cors_allowed_origins if needed, * for now allows all
socketio = SocketIO(app, cors_allowed_origins="*")

OUTPUT_DIR = os.path.join(os.getcwd(), "MusicOutput")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start_download')
def handle_download(data):
    url = data.get('url')
    if not url:
        emit('log', {'msg': 'Vui lòng nhập URL!', 'style': 'red'})
        return

    emit('log', {'msg': f'Bắt đầu xử lý: {url}', 'style': 'bold cyan'})
    
    # Define callback to send logs to client
    def log_callback(msg, style=""):
        # Map rich styles to simple CSS classes or colors if needed
        # For simplicity, pass the style string directly and handle in JS
        socketio.emit('log', {'msg': msg, 'style': style})

    def run_download():
        try:
            if "spotify.com" in url:
                download_spotify(url, OUTPUT_DIR, log_callback)
            elif "nhaccuatui.com" in url:
                download_nct(url, OUTPUT_DIR, log_callback)
            else:
                # Try generic/NCT fallback
                download_nct(url, OUTPUT_DIR, log_callback)
            
            socketio.emit('done', {'msg': 'Quy trình kết thúc.'})
            
        except Exception as e:
            socketio.emit('log', {'msg': f'Lỗi hệ thống: {str(e)}', 'style': 'red'})

    # Run in a separate thread so it doesn't block the server
    thread = threading.Thread(target=run_download)
    thread.start()

if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    print("Server starting on http://localhost:5000")
    socketio.run(app, debug=True, port=5000, allow_unsafe_werkzeug=True)
