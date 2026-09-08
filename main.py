import yt_dlp

print("=== PRD MEDIA DOWNLOADER ===")

url = input("Paste URL: ")

options = {
    "outtmpl": "downloads/%(title)s.%(ext)s",
    "ffmpeg_location": r"C:\Users\ACER\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin"
}

with yt_dlp.YoutubeDL(options) as downloader:
    downloader.download([url])

print("Download selesai!")