from pathlib import Path
import sys
import os
import yt_dlp


def get_ffmpeg_path():
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, "bin")


def download_media(
    url,
    save_folder,
    quality="Best",
    media_format="Video",
    progress_callback=None
):
    save_folder = Path(save_folder)
    ffmpeg_path = get_ffmpeg_path()

    def progress_hook(data):
        if data["status"] == "downloading":
            downloaded = data.get("downloaded_bytes", 0)
            total = data.get("total_bytes") or data.get("total_bytes_estimate")

            if total and progress_callback:
                progress_callback(downloaded / total)

        elif data["status"] == "finished":
            if progress_callback:
                progress_callback(1)

    if media_format == "Audio":
        bitrate = quality.replace(" kbps", "")

        options = {
            "outtmpl": str(save_folder / "%(title)s.%(ext)s"),
            "format": "bestaudio/best",
            "retries": 5,
            "fragment_retries": 5,
            "socket_timeout": 30,
            "progress_hooks": [progress_hook],
            "ffmpeg_location": ffmpeg_path,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": bitrate,
                }
            ],
        }

    else:
        if quality == "1080p":
            video_format = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
        elif quality == "720p":
            video_format = "bestvideo[height<=720]+bestaudio/best[height<=720]"
        elif quality == "480p":
            video_format = "bestvideo[height<=480]+bestaudio/best[height<=480]"
        else:
            video_format = "bestvideo+bestaudio/best"

        options = {
            "outtmpl": str(save_folder / "%(title)s.%(ext)s"),
            "format": video_format,
            "retries": 5,
            "fragment_retries": 5,
            "socket_timeout": 30,
            "progress_hooks": [progress_hook],
            "ffmpeg_location": ffmpeg_path,
        }

    with yt_dlp.YoutubeDL(options) as downloader:
        info = downloader.extract_info(
            url,
            download=True
        )

        return downloader.prepare_filename(info)


def get_media_info(url):
    options = {
        "quiet": True,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(options) as downloader:
        info = downloader.extract_info(
            url,
            download=False
        )

        return {
            "title": info.get("title", "Unknown Title"),
            "uploader": info.get("uploader", "Unknown"),
            "extractor": info.get("extractor_key", "Unknown"),
            "thumbnail": info.get("thumbnail"),
        }