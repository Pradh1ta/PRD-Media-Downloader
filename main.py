import os
import time
from colorama import Fore, Style, init
init (autoreset=True)
def clear():
    os.system('cls' if os.name == "nt" else 'clear')
from pathlib import Path
import subprocess
import yt_dlp

print(Fore.YELLOW + "=== PRD MEDIA DOWNLOADER ===")

url = input("Paste URL: ")
title = input("File name: ")

download_folder = Path.home() / "Downloads"

options = {
    "outtmpl": str(download_folder / f"{title}.%(ext)s"),
    "format": "bestvideo+bestaudio/best",
    "retries": 5,
    "fragment_retries": 5,
    "socket_timeout": 30,
}

try:
    max_retry = 5

    for attempt in range(1, max_retry + 1):
        try:
            with yt_dlp.YoutubeDL(options) as downloader:
                info = downloader.extract_info(url, download=True)
                file_path = Path(downloader.prepare_filename(info))

            break

        except yt_dlp.utils.DownloadError:
            if attempt < max_retry:
                print(Fore.RED + f"Download error. Retry {attempt}/{max_retry}...")
                time.sleep(3)
            else:
                raise

    print(Fore.GREEN + "Download selesai!")
    time.sleep(2)
    clear()
    print(Fore.YELLOW + "Checking codec...")

    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=codec_name",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(file_path)
        ],
        capture_output=True,
        text=True
    )

    codec = result.stdout.strip().lower()

    print(f"Video codec: {codec}")
    time.sleep(2)

    if codec in ["hevc", "h265"]:
        print("HEVC detected!")
        print("Converting to H.264...")

        converted_file = file_path.with_name(
            file_path.stem + "_h264.mp4"
        )

        subprocess.run(
            [
                "ffmpeg",
                 "-hide_banner",
                "-loglevel", "error",
                "-i", str(file_path),
                "-c:v", "libx264",
                "-crf", "18",
                "-preset", "medium",
                "-c:a", "aac",
                "-b:a", "192k",
                str(converted_file)
            ],
            check=True
        )

        file_path.unlink()
        final_file = file_path.with_suffix(".mp4")
        converted_file.rename(final_file)

        print(f"\nConvert selesai: {converted_file.name}")

    else:
        print("Codec sudah kompatibel, tidak perlu convert.")
        time.sleep(2)
        clear()
        print(Fore.GREEN + "Video berhasil di download !")

except yt_dlp.utils.DownloadError:
    print("Download gagal.")
    print("URL tidak didukung, video tidak tersedia, atau platform sedang memblokir downloader.")

except subprocess.CalledProcessError:
    print("\nFFmpeg gagal melakukan convert.")