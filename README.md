# Antigravity Music Downloader

Công cụ tải nhạc tự động từ Spotify và Nhaccuatui (NCT).

## Tính năng
- **Spotify**: Tải bài hát, album, playlist (sử dụng `spotdl` để tải file chất lượng cao từ YouTube).
- **Nhaccuatui**: Tải bài hát từ link trực tiếp (hỗ trợ `yt-dlp` generic extraction).

## Cài đặt
1. Cài Python (đã có).
2. Cài đặt thư viện:
   ```bash
   pip install -r requirements.txt
   ```
3. Cài FFmpeg (quan trọng cho Spotify):
   ```bash
   python -m spotdl --download-ffmpeg
   ```

## Sử dụng
Chạy lệnh sau trong terminal:
```bash
python main.py
```

## Lưu ý
- Nhạc tải về sẽ nằm trong thư mục `MusicOutput`.
- Với Spotify, tool sẽ tìm bài hát tương ứng trên YouTube Music để tải, nên đôi khi phiên bản có thể hơi khác (ví dụ MV ver).
