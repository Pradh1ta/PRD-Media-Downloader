from pathlib import Path
import yt_dlp


def download_media(
    url,
    save_folder,
    quality="Best",
    media_format="Video",
    progress_callback=None
):
    save_folder = Path(save_folder)

    print("FORMAT DITERIMA:", media_format)
    print("QUALITY DITERIMA:", quality)

    if quality == "1080p":
        video_format = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"

    elif quality == "720p":
        video_format = "bestvideo[height<=720]+bestaudio/best[height<=720]"

    elif quality == "480p":
        video_format = "bestvideo[height<=480]+bestaudio/best[height<=480]"

    else:
        video_format = "bestvideo+bestaudio/best"

    def progress_hook(data):
        if data["status"] == "downloading":
            downloaded = data.get("downloaded_bytes", 0)
            total = data.get("total_bytes") or data.get("total_bytes_estimate")

            if total and progress_callback:
                percent = downloaded / total
                progress_callback(percent)

        elif data["status"] == "finished":
            if progress_callback:
                progress_callback(1)

    from pathlib import Path
import yt_dlp


def download_media(
    url,
    save_folder,
    quality="Best",
    media_format="Video",
    progress_callback=None
):
    save_folder = Path(save_folder)

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

    with yt_dlp.YoutubeDL(options) as downloader:
        info = downloader.extract_info(
            url,
            download=True
        )

        file_path = downloader.prepare_filename(info)

        return file_path

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