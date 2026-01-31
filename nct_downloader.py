import yt_dlp
import os
from rich.console import Console

console = Console()

import requests
from bs4 import BeautifulSoup
import re

def get_nct_playlist_songs(url, log_callback=None):
    """
    Lấy danh sách link bài hát từ playlist/album/top100 NCT.
    """
    def log(msg, style=""):
         if log_callback: log_callback(msg, style)
         else: console.print(f"[{style}]{msg}[/{style}]") if style else console.print(msg)

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        song_links = []
        
        links = soup.find_all('a', class_='name_song')
        
        for link in links:
            href = link.get('href')
            if href:
                song_links.append(href)
        
        return list(set(song_links))
        
    except Exception as e:
        log(f"Lỗi khi lấy playlist NCT: {e}", "red")
        return []

def download_nct(url, output_dir="downloads", log_callback=None):
    """
    Tải nhạc từ Nhaccuatui sử dụng yt-dlp.
    Hỗ trợ cả bài lẻ và playlist.
    """
    def log(msg, style=""):
         if log_callback: log_callback(msg, style)
         else: console.print(f"[{style}]{msg}[/{style}]") if style else console.print(msg)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    is_playlist = any(x in url for x in ['/playlist/', '/top-100/', '/album/'])
    
    if is_playlist:
        log(f"Phát hiện Playlist/Album NCT: {url}", "bold cyan")
        log("Đang lấy danh sách bài hát...", "yellow")
        songs = get_nct_playlist_songs(url, log_callback)
        
        if not songs:
            log("Không tìm thấy bài hát nào trong playlist này!", "red")
            return False
            
        log(f"Tìm thấy {len(songs)} bài hát. Bắt đầu tải...", "green")
        
        count = 0
        for song_url in songs:
             if download_nct(song_url, output_dir, log_callback):
                 count += 1
        
        log(f"Hoàn tất playlist! Tải được {count}/{len(songs)} bài.", "bold green")
        return True

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }

    log(f"Đang xử lý: {url}", "cyan")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown Title')
            log(f"Tìm thấy bài hát: {title}", "green")
            log("Đang tải xuống...", "yellow")
            ydl.download([url])
            log("Tải thành công!", "bold green")
            return True
    except Exception as e:
        log(f"Lỗi khi tải bài hát: {str(e)}", "bold red")
        return False

