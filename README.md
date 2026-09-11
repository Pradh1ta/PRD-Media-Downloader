# PRD Media Downloader

A simple media downloader with a graphical user interface, built with Python and yt-dlp.

## Features

- Download video and audio from supported platforms
- Video quality options: Best, 1080p, 720p, 480p
- Extract audio as MP3
- Audio bitrate options: 320 kbps, 192 kbps, 128 kbps
- Media preview with thumbnail and metadata
- Real-time download progress
- Custom download location
- Simple and minimal GUI

## Supported Platforms

Supports websites available through yt-dlp, including:

- YouTube
- TikTok
- Instagram
- X / Twitter
- Facebook
- And more

> Platform support may change depending on yt-dlp and the website.

## Requirements

- Python
- Git
- FFmpeg

## Installation

```bash
git clone https://github.com/Pradh1ta/PRD-Media-Downloader.git
cd PRD-Media-Downloader
pip install -r requirements.txt
winget install Gyan.FFmpeg
```

Restart the terminal after installing FFmpeg.

## Run

```bash
python gui.py
```

Paste a media URL, choose the format and quality, select a download location, then click **Download**.

## Disclaimer

Only download content you own or have permission to download.