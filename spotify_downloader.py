import subprocess
import sys
import os
from rich.console import Console

console = Console()

def download_spotify(url, output_dir="downloads", log_callback=None):
    """
    Tải nhạc từ Spotify sử dụng spotdl (chạy qua command line).
    """
    def log(msg, style=""):
         if log_callback: log_callback(msg, style)
         else: console.print(f"[{style}]{msg}[/{style}]") if style else console.print(msg)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    log(f"Đang xử lý link Spotify: {url}", "bold green")
    log("Đang tìm và tải nhạc từ YouTube (spotdl)...", "yellow")

    current_dir = os.getcwd()
    try:
        os.chdir(output_dir)
        # Dùng python -m spotdl để tránh lỗi PATH
        command = [sys.executable, "-m", "spotdl", url]
        
        process = subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        # Đọc output realtime
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                clean_output = output.strip()
                if clean_output:
                     # Filter some spammy logs if needed, for now send all
                     log(clean_output, "dim")
        
        rc = process.poll()
        if rc == 0:
            log("Tải hoàn tất!", "bold green")
            return True
        else:
             # Đọc phần còn lại của stderr nếu có lỗi
            error_out = process.stderr.read()
            log(f"Có lỗi xảy ra: {error_out}", "bold red")
            return False

    except FileNotFoundError:
        log("Lỗi: Không tìm thấy lệnh 'spotdl'.", "bold red")
        return False
    except Exception as e:
        log(f"Lỗi không xác định: {str(e)}", "bold red")
        return False
    finally:
        os.chdir(current_dir)
