# PRD Media Downloader

A simple and modern desktop application for downloading video and audio from multiple platforms.

Built with Python, CustomTkinter, and yt-dlp.

## Features

- Download video and audio
- Video quality options: Best, 1080p, 720p, 480p
- Extract audio as MP3
- Audio bitrate options: 320 kbps, 192 kbps, 128 kbps
- Media preview with thumbnail and metadata
- Real-time download progress
- Custom download location
- Simple and modern graphical interface

## Supported Platforms

PRD Media Downloader uses yt-dlp and supports many websites, including:

- YouTube
- TikTok
- Instagram
- X / Twitter
- Facebook
- And more

> Platform availability may change depending on yt-dlp updates and changes made by individual websites.

## Download

The easiest way to use PRD Media Downloader is by downloading the pre-built Windows executable from the **Releases** section of this repository.

No Python or manual FFmpeg installation is required when using the pre-built executable.

> PRD Media Downloader is currently in beta. Bugs and compatibility issues may occur.

## Run From Source

### Requirements

- Python
- Git
- FFmpeg

Clone the repository:

```bash
git clone https://github.com/Pradh1ta/PRD-Media-Downloader.git
cd PRD-Media-Downloader
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### FFmpeg Setup

FFmpeg binaries are not included in the repository due to their file size.

Create a `bin` folder inside the project directory and place `ffmpeg.exe` and `ffprobe.exe` inside it.

The project structure should look like this:

```text
PRD-Media-Downloader/
├── assets/
├── bin/
│   ├── ffmpeg.exe
│   └── ffprobe.exe
├── downloader.py
├── gui.py
├── README.md
└── requirements.txt
```

Then run the application:

```bash
python gui.py
```

## Usage

1. Paste a supported media URL.
2. Choose between Video or Audio.
3. Select the desired quality.
4. Choose a download location.
5. Click **Download**.
6. Wait for the download to complete.

Downloaded media will be saved to the selected folder.

## Tech Stack

- Python
- CustomTkinter
- yt-dlp
- FFmpeg
- Pillow
- PyInstaller

## Beta Notice

PRD Media Downloader is currently under active development.

Some websites or media links may not work correctly due to platform changes, yt-dlp compatibility, authentication requirements, or other restrictions.

Features, interface elements, and functionality may change in future releases.

## Disclaimer

Only download content you own or have permission to download.

PRD Media Downloader is not affiliated with YouTube, TikTok, Instagram, X, Facebook, or yt-dlp.

Users are responsible for how they use this software.