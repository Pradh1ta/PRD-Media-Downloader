from pathlib import Path
import yt_dlp

print("=== PRD MEDIA DOWNLOADER ===")

url = input("Paste URL: ")

download_folder = Path.home() / "Downloads"

options = {
    "outtmpl": str(download_folder / "%(title)s.%(ext)s")
}

with yt_dlp.YoutubeDL(options) as downloader:
    downloader.download([url])

print("Download selesai!")