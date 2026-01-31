import sys
import os
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text

# Import modules
from nct_downloader import download_nct
from spotify_downloader import download_spotify

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    # clear_screen()
    title = Text("Antigravity Music Downloader", style="bold magenta", justify="center")
    subtitle = Text("Hỗ trợ: Spotify & Nhaccuatui", style="cyan", justify="center")
    panel = Panel(Text.assemble(title, "\n", subtitle), border_style="green", expand=False)
    console.print(panel)

def process_batch(file_path):
    if not os.path.exists(file_path):
        console.print(f"[bold red]File {file_path} không tồn tại![/bold red]")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            links = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not links:
            console.print("[yellow]File không có link nào hợp lệ.[/yellow]")
            return

        total = len(links)
        console.print(f"[bold]Tìm thấy {total} link. Bắt đầu xử lý...[/bold]")
        
        output_dir = os.path.join(os.getcwd(), "MusicOutput")
        success_count = 0

        for i, url in enumerate(links, 1):
            console.print(f"\n[bold cyan]--- Link {i}/{total} ---[/bold cyan]")
            result = False
            if "spotify.com" in url:
                result = download_spotify(url, output_dir)
            elif "nhaccuatui.com" in url:
                result = download_nct(url, output_dir)
            else:
                # Mặc định thử NCT downloader (generic)
                result = download_nct(url, output_dir)
            
            if result:
                success_count += 1
        
        console.print(f"\n[bold green]Hoàn tất! Thành công: {success_count}/{total}[/bold green]")

    except Exception as e:
        console.print(f"[bold red]Lỗi khi đọc file:[/bold red] {str(e)}")

def main():
    while True:
        print_banner()
        
        console.print("\n[bold]Chọn chế độ:[/bold]")
        console.print("1. [green]Spotify[/green] (Nhập link trực tiếp)")
        console.print("2. [cyan]Nhaccuatui[/cyan] (Nhập link trực tiếp)")
        console.print("3. [yellow]Tải hàng loạt từ file (links.txt)[/yellow]")
        console.print("4. [red]Thoát[/red]")
        
        choice = Prompt.ask("Lựa chọn của bạn", choices=["1", "2", "3", "4"], default="1")
        
        if choice == "4":
            console.print("[bold yellow]Tạm biệt![/bold yellow]")
            sys.exit()
            
        output_dir = os.path.join(os.getcwd(), "MusicOutput")
        
        if choice == "3":
            process_batch(os.path.join(os.getcwd(), "links.txt"))
        else:
            url = Prompt.ask("Nhập Link bài hát/playlist")
            if choice == "1":
                if "spotify.com" in url:
                    download_spotify(url, output_dir)
                else:
                    console.print("[bold red]Link không hợp lệ! Phải là link Spotify.[/bold red]")
            elif choice == "2":
                download_nct(url, output_dir)
                
        console.print("\n[dim]Nhấn Enter để tiếp tục...[/dim]")
        input()
        clear_screen()

if __name__ == "__main__":
    main()
