from pathlib import Path
import sys
import os
import yt_dlp
import subprocess   
_cached_url = None
_cached_info = None


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
    custom_name="",
    progress_callback=None
):
    save_folder = Path(save_folder)

    if custom_name:
        invalid_chars = '<>:"/\\|?*'

        for char in invalid_chars:
            custom_name = custom_name.replace(char, "_")

        output_name = f"{custom_name}.%(ext)s"
    else:
        output_name = "%(title)s.%(ext)s"

    ffmpeg_path = get_ffmpeg_path()

    global _cached_url, _cached_info

    cached_info = None

    if url == _cached_url:
        cached_info = _cached_info

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
        if media_format == "Audio":
            if quality == "Best":
                bitrate = "320"
            else:
                bitrate = quality.replace(" kbps", "")
        options = {
            "outtmpl": str(save_folder / output_name),
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


        is_youtube = "youtube.com" in url or "youtu.be" in url

        if not is_youtube:
            quality = "Best"

        if quality == "1080p":
            video_format = "bestvideo[height<=1080][vcodec^=avc1]+bestaudio[acodec^=mp4a]/best[height<=1080]"

        elif quality == "720p":
            video_format = "bestvideo[height<=720][vcodec^=avc1]+bestaudio[acodec^=mp4a]/best[height<=720]"

        elif quality == "480p":
            video_format = "bestvideo[height<=480][vcodec^=avc1]+bestaudio[acodec^=mp4a]/best[height<=480]"

        else:
            video_format = "bestvideo[vcodec^=avc1]+bestaudio[acodec^=mp4a]/best"

        needs_conversion = False

        if not is_youtube:
            check_options = {
                "quiet": True,
                "skip_download": True,
                "format": video_format,
            }

            with yt_dlp.YoutubeDL(check_options) as checker:
                if cached_info:
                    selected_info = checker.process_ie_result(
                        cached_info,
                        download=False
                    )
                else:
                    selected_info = checker.extract_info(
                        url,
                        download=False
                    )

            codec = selected_info.get("vcodec", "")

            print("Codec:", codec)

            if codec.startswith(("hev1", "hvc1", "hevc", "h265")):
                needs_conversion = True

            print("Needs conversion:", needs_conversion)



        options = {
            "outtmpl": str(save_folder / output_name),
            "format": video_format,
            "merge_output_format": "mp4",
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

        final_file = downloader.prepare_filename(info)

        if media_format == "Video" and needs_conversion:
            temp_file = str(Path(final_file).with_suffix(".h264.mp4"))

            ffmpeg_exe = os.path.join(ffmpeg_path, "ffmpeg.exe")

            subprocess.run([
                ffmpeg_exe,
                "-y",
                "-i", final_file,
                "-c:v", "libx264",
                "-c:a", "aac",
                "-movflags", "+faststart",
                temp_file
            ], check=True, creationflags=subprocess.CREATE_NO_WINDOW)

            os.replace(temp_file, final_file)

        return final_file


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

        global _cached_url, _cached_info

        _cached_url = url
        _cached_info = info

        formats = info.get("formats", [])

        best_size = None

        for f in reversed(formats):
            filesize = f.get("filesize") or f.get("filesize_approx")

            if filesize:
                best_size = filesize
                break
            
        if best_size:
            best_size_mb = best_size / (1024 * 1024)
            size_text = f"{best_size_mb:.1f} MB"
        else:
            size_text = "Unknown size"

        return {
            "title": info.get("title", "Unknown Title"),
            "uploader": info.get("uploader", "Unknown"),
            "extractor": info.get("extractor_key", "Unknown"),
            "thumbnail": info.get("thumbnail"),
            "size": size_text,
}