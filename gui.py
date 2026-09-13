import customtkinter as ctk
from tkinter import filedialog
from downloader import download_media, get_media_info
import threading
from PIL import Image
from io import BytesIO
from urllib.request import urlopen
from pathlib import Path
import sys
import os
import webbrowser
import ctypes

def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

def register_font(font_path):
    FR_PRIVATE = 0x10

    ctypes.windll.gdi32.AddFontResourceExW(
        str(font_path),
        FR_PRIVATE,
        0
    )

if getattr(sys, "frozen", False):
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path(__file__).resolve().parent

register_font(
    base_path / "assets" / "fonts" / "space-grotesk.regular.ttf"
)

register_font(
    base_path / "assets" / "fonts" / "space-grotesk.bold.ttf"
)

ctk.set_appearance_mode("light")

app = ctk.CTk()

app.title("PRD Media Downloader")
app.geometry("920x670")
app.resizable(False, False)

def open_github():
    webbrowser.open("https://github.com/Pradh1ta/PRD-Media-Downloader")

def open_changelog():
    changelog_window = ctk.CTkToplevel(app)

    changelog_window.transient(app)
    changelog_window.lift()
    changelog_window.focus_force()
    changelog_window.grab_set()

    changelog_window.title("Changelog")
    changelog_window.geometry("460x360")
    changelog_window.resizable(False, False)
    changelog_window.configure(fg_color="#F5F5F5")

    card = ctk.CTkFrame(
        changelog_window,
        width=400,
        height=300,
        fg_color="white",
        border_width=2,
        border_color="#111111",
        corner_radius=24
    )
    card.place(x=30, y=30)

    badge = ctk.CTkLabel(
        card,
        text="UPDATE",
        width=72,
        height=28,
        fg_color="#B8F95B",
        text_color="#111111",
        corner_radius=14,
        font=("Space Grotesk", 11, "bold")
    )
    badge.place(x=24, y=22)

    title = ctk.CTkLabel(
        card,
        text="v1.3.0 Beta",
        font=("Space Grotesk", 22, "bold"),
        text_color="#111111",
        anchor="w"
    )
    title.place(x=24, y=65)

    date = ctk.CTkLabel(
        card,
        text="Latest update",
        font=("Space Grotesk", 12),
        text_color="#737373"
    )
    date.place(x=24, y=100)

    changes = ctk.CTkLabel(
        card,
        text=(
            "• Redesigned user interface\n"
            "• Automatic media preview\n"
            "• Preview metadata caching\n"
            "• Improved download reliability\n"
            "• Better error handling\n"
            "• UI and performance improvements"
        ),
        font=("Space Grotesk", 13),
        text_color="#333333",
        justify="left",
        anchor="w"
    )
    changes.place(x=24, y=140)

def open_about():
    about_window = ctk.CTkToplevel(app)

    about_window.transient(app)
    about_window.lift()
    about_window.focus_force()
    
    about_window.title("About")
    about_window.geometry("460x330")
    about_window.resizable(False, False)
    about_window.configure(fg_color="#F5F5F5")

    card = ctk.CTkFrame(
        about_window,
        width=400,
        height=270,
        fg_color="white",
        border_width=2,
        border_color="#111111",
        corner_radius=24
    )
    card.place(x=30, y=30)
    card.pack_propagate(False)

    badge = ctk.CTkLabel(
        card,
        text="About",
        width=58,
        height=28,
        fg_color="#B8F95B",
        text_color="#111111",
        corner_radius=14,
        font=("Space Grotesk", 12, "bold")
    )
    badge.place(x=24, y=22)

    title = ctk.CTkLabel(
        card,
        text="PRD Media Downloader",
        font=("Space Grotesk", 22, "bold"),
        text_color="#111111",
        anchor="w"
    )
    title.place(x=24, y=65)

    version = ctk.CTkLabel(
        card,
        text="v1.3.0 Beta",
        font=("Space Grotesk", 12),
        text_color="#737373"
    )
    version.place(x=24, y=100)

    description = ctk.CTkLabel(
        card,
        text="A simple and modern media downloader\nbuilt with Python, yt-dlp and FFmpeg.",
        font=("Space Grotesk", 13),
        text_color="#333333",
        justify="left",
        anchor="w"
    )
    description.place(x=24, y=140)

    creator = ctk.CTkLabel(
        card,
        text="Created by Pradhita",
        font=("Space Grotesk", 12, "bold"),
        text_color="#111111"
    )
    creator.place(x=24, y=205)

    github_button = ctk.CTkButton(
        card,
        text="GitHub ↗",
        width=90,
        height=32,
        fg_color="#111111",
        hover_color="#333333",
        text_color="white",
        corner_radius=16,
        font=("Space Grotesk", 12, "bold"),
        command=open_github
    )
    github_button.place(x=280, y=200)
    

# =========================
# Main Container
# =========================

scroll_frame = ctk.CTkScrollableFrame(
    app,
    fg_color="white",
    corner_radius=0
)
scroll_frame.pack(fill="both", expand=True)

main_frame = ctk.CTkFrame(
    scroll_frame,
    width=880,
    height=1020,
    fg_color="white",
    corner_radius=0
)
main_frame.pack()
main_frame.pack_propagate(False)

img = Image.open(resource_path("assets/images/background.png"))

background_image = ctk.CTkImage(
    light_image=img,
    size=(500, int(500 * img.height / img.width))
)
background_label = ctk.CTkLabel(
    main_frame,
    image=background_image,
    text=""
)

background_label.place(x=400, y=40)

# =========================
# Branding
# =========================

brand_logo_raw = Image.open(resource_path("assets/logos/pradh.png")).convert("RGBA")

pixels = brand_logo_raw.load()

for y in range(brand_logo_raw.height):
    for x in range(brand_logo_raw.width):
        r, g, b, a = pixels[x, y]

        if a > 0:
            pixels[x, y] = (0, 0, 0, a)

brand_logo_img = ctk.CTkImage(
    light_image=brand_logo_raw,
    size=(30, 30)
)

brand_logo = ctk.CTkLabel(
    main_frame,
    image=brand_logo_img,
    text=""
)
brand_logo.place(x=50, y=35)


brand = ctk.CTkLabel(
    main_frame,
    text="   Pradh",
    font=("Space Grotesk", 20, "bold"),
    text_color="#212121"
    
)
brand.place(x=78, y=35)

about_button = ctk.CTkButton(
    main_frame,
    text="About",
    width=60,
    height=28,
    fg_color="transparent",
    hover_color="#EEEEEE",
    text_color="#111111",
    corner_radius=8,
    font=("Space Grotesk", 12, "bold"),
    command=open_about
)
about_button.place(x=680, y=35)

changelog_button = ctk.CTkButton(
    main_frame,
    text="Changelog",
    width=85,
    height=28,
    fg_color="white",
    hover_color="#EEEEEE",
    text_color="#111111",
    border_width=2,
    border_color="#111111",
    corner_radius=8,
    font=("Space Grotesk", 12, "bold"),
    command=open_changelog
)
changelog_button.place(x=755, y=35)

# =========================
# Title
# =========================

title = ctk.CTkLabel(
    main_frame,
    text="Download Media",
    font=("Space Grotesk", 40, "bold"),
    text_color="#212121"
)
title.place(x=50, y=100)

title = ctk.CTkLabel(
    main_frame,
    text="Without The",
    font=("Space Grotesk", 40, "bold"),
    text_color="#212121"
)
title.place(x=50, y=150)
title = ctk.CTkLabel(
    main_frame,
    text="Hassle.",
    font=("Space Grotesk", 40, "bold"),
    text_color="#212121"
)
title.place(x=50, y=200)
CONTENT_Y = 270

subtitle = ctk.CTkLabel(
    main_frame,
    text="Everything you need to save your favorite media in one place. \nPaste a link, choose the format and quality you want",
    font=("Space Grotesk", 13),
    text_color="#000000",
    justify="left",
    anchor="w",
    fg_color="transparent",
)
subtitle.place(x=50, y=270)

# =========================
# URL Input
# =========================

url_entry = ctk.CTkEntry(
    main_frame,
    width=760,
    height=52,
    placeholder_text="Paste media URL here !",
    fg_color="white",
    text_color="#212121",
    placeholder_text_color="#000000",
    border_color="#000000",
    border_width=2,
    corner_radius=26,
    font=("Space Grotesk", 14)
)

url_entry.place(x=50, y=195 + CONTENT_Y)

preview_job = None

def schedule_auto_preview(event=None):
    global preview_job

    if preview_job is not None:
        app.after_cancel(preview_job)

    url = url_entry.get().strip()

    if url.startswith("http://") or url.startswith("https://"):
        preview_job = app.after(800, fetch_info)

url_entry.bind("<KeyRelease>", schedule_auto_preview)

def reset_download_state(event=None):
    download_button.configure(
        text="Download",
        state="normal",
        fg_color="#212121",
        text_color="white"
    )

    progress_bar.set(0)
    progress_label.configure(text="0%")
    error_label.configure(text="")

    url = url_entry.get().lower()

    is_youtube = "youtube.com" in url or "youtu.be" in url

    if format_value == "Video":
        if url and not is_youtube:
            choose_quality("Best")
            quality_button.configure(state="disabled")
        else:
            quality_button.configure(state="normal")

# =========================
# Format & Quality
# =========================

format_label = ctk.CTkLabel(
    main_frame,
    text="FORMAT",
    font=("Space Grotesk", 12, "bold"),
    text_color="#212121"
)
format_label.place(x=50, y=260 + CONTENT_Y)


quality_label = ctk.CTkLabel(
    main_frame,
    text="QUALITY",
    font=("Space Grotesk", 12, "bold"),
    text_color="#212121"
)
quality_label.place(x=170, y=260 + CONTENT_Y)


def change_format(selected_format):
    global quality_value, quality_options

    if selected_format == "Video":
        quality_value = "Best"
        quality_options = ["Best", "1080p", "720p", "480p"]

    elif selected_format == "Audio":
        quality_value = "Best"
        quality_options = ["Best", "192 kbps", "128 kbps"]

    summary_format.configure(
    text=f"Format:     {selected_format}    |"

    )

    summary_quality.configure(
        text=f"Quality:     {quality_value}"
    )

    quality_button.configure(text=f"{quality_value}   ▾")
    
    quality_dropdown.configure(
        height=(len(quality_options) * 39) + 10
        

        
)

    for widget in quality_dropdown.winfo_children():
        widget.destroy()

    for i, value in enumerate(quality_options):
        option = ctk.CTkButton(
            quality_dropdown,
            text=value,
            width=160,
            height=34,
            fg_color="transparent",
            hover_color="#2A2A2A",
            text_color="black",
            corner_radius=12,
            font=("Space Grotesk", 13),
            anchor="w",
            command=lambda v=value: choose_quality(v)
        )

        option.place(x=10, y=8 + (i * 39))


format_value = "Video"


def toggle_format_dropdown():
    if format_dropdown.winfo_ismapped():
        format_dropdown.place_forget()
    else:
        format_dropdown.place(x=50, y=338 + CONTENT_Y)
        format_dropdown.lift()


def choose_format(value):
    global format_value

    format_value = value
    format_button.configure(text=f"{value}   ▾")
    format_dropdown.place_forget()

    change_format(value)


format_button = ctk.CTkButton(
    main_frame,
    text="Video   ▾",
    width=100,
    height=42,
    fg_color="#B8F95B",
    hover_color="#9CF520",
    text_color="black",
    corner_radius=21,
    font=("Space Grotesk", 13, "bold"),
    anchor="w",
    command=toggle_format_dropdown
)

format_button.place(x=50, y=290 + CONTENT_Y)


format_dropdown = ctk.CTkFrame(
    main_frame,
    width=180,
    height=88,
    fg_color="#B8F95B",
    corner_radius=16
)


video_option = ctk.CTkButton(
    format_dropdown,
    text="Video",
    width=160,
    height=34,
    fg_color="transparent",
    hover_color="white",
    text_color="black",
    corner_radius=12,
    font=("Space Grotesk", 13),
    anchor="w",
    command=lambda: choose_format("Video")
)
video_option.place(x=10, y=8)


audio_option = ctk.CTkButton(
    format_dropdown,
    text="Audio",
    width=160,
    height=34,
    fg_color="transparent",
    hover_color="white",
    text_color="black",
    corner_radius=12,
    font=("Space Grotesk", 13),
    anchor="w",
    command=lambda: choose_format("Audio")
)
audio_option.place(x=10, y=47)


quality_value = "Best"




def toggle_quality_dropdown():
    if quality_dropdown.winfo_ismapped():
        quality_dropdown.place_forget()
    else:
        quality_dropdown.place(x=170, y=338 + CONTENT_Y)
        quality_dropdown.lift()


def choose_quality(value):
    global quality_value
    
    quality_value = value
    quality_button.configure(text=f"{value}   ▾")
    quality_dropdown.place_forget()
    summary_quality.configure(
    text=f"Quality:     {quality_value}"
)


quality_button = ctk.CTkButton(
    main_frame,
    text="Best   ▾",
    width=100,
    height=42,
    fg_color="#B8F95B",
    hover_color="#9CF520",
    text_color="black",
    text_color_disabled="white",
    corner_radius=21,
    font=("Space Grotesk", 13, "bold"),
    anchor="w",
    command=toggle_quality_dropdown
)

quality_button.place(x=170, y=290 + CONTENT_Y)

custom_name_label = ctk.CTkLabel(
    main_frame,
    text="File Name",
    font=("Space Grotesk", 12, "bold"),
    text_color="#212121"
)
custom_name_label.place(x=290, y=260 + CONTENT_Y)


custom_name_entry = ctk.CTkEntry(
    main_frame,
    width=380,
    height=42,
    placeholder_text=" Optional — use original title if empty",
    fg_color="#212121",
    text_color="white",
    placeholder_text_color="white",
    corner_radius=0,
    font=("Space Grotesk", 13)
)

custom_name_entry.place(x=290, y=290 + CONTENT_Y)


quality_dropdown = ctk.CTkFrame(
    main_frame,
    width=180,
    height=166,
    fg_color="#B8F95B",
    corner_radius=16
)


quality_options = ["Best", "1080p", "720p", "480p"]

for i, value in enumerate(quality_options):
    option = ctk.CTkButton(
        quality_dropdown,
        text=value,
        width=160,
        height=34,
        fg_color="transparent",
        hover_color="white",
        text_color="black",
        corner_radius=12,
        font=("Space Grotesk", 13),
        anchor="w",
        command=lambda v=value: choose_quality(v)
    )

    option.place(x=10, y=8 + (i * 39))

# =========================
# Save Location
# =========================

save_label = ctk.CTkLabel(
    main_frame,
    text="SAVE TO",
    font=("Space Grotesk", 12, "bold"),
    text_color="#737373"
)
save_label.place(x=50, y=350 + CONTENT_Y)


save_entry = ctk.CTkEntry(
    main_frame,
    width=760,
    height=48,
    fg_color="white",
    text_color="#212121",
    border_color="#000000",
    border_width=2,
    corner_radius=26,
    font=("Space Grotesk", 14)
)
save_entry.place(x=50, y=380 + CONTENT_Y)
default_download_folder = Path.home() / "Downloads"
save_entry.insert(0, str(default_download_folder))


def browse_folder():
    folder = filedialog.askdirectory()

    if folder:
        save_entry.delete(0, "end")
        save_entry.insert(0, folder)


browse_button = ctk.CTkButton(
    main_frame,
    text="↗",
    width=36,
    height=36,
    fg_color="#212121",
    hover_color="#333333",
    text_color="white",
    corner_radius=100,
    font=("Space Grotesk", 16, "bold"),
    command=browse_folder
)

browse_button.place(x=825, y=387 + CONTENT_Y)


# =========================
# Download Functions
# =========================
def run_fetch_info(url):
    try:
        info = get_media_info(url)

        thumbnail_data = None
        thumbnail_url = info.get("thumbnail")

        if thumbnail_url:
            try:
                thumbnail_data = urlopen(thumbnail_url).read()
            except Exception as error:
                print("Thumbnail gagal:", error)

        app.after(
            0,
            lambda: show_preview(info, thumbnail_data)
        )

    except Exception as error:
        app.after(
            0,
            lambda e=error: preview_failed(e)
        )

def show_preview(info, thumbnail_data):
    title_text = info["title"]

    if len(title_text) > 30:
        title_text = title_text[:30] + "..."

    preview_title.configure(
        text=title_text
    )

    preview_meta.configure(
    text=f'{info["extractor"]} • {info["uploader"]} • {info["size"]}'
)

    preview_meta.place(x=200, y=78)
    
    
    extractor = info["extractor"].lower()

    if "youtube" in extractor:
        quality_button.configure(state="normal")
    else:
        choose_quality("Best")
        quality_button.configure(state="disabled")

        preview_meta.configure(
            text=f'{info["uploader"]} • {info["extractor"]}'
        )

    if thumbnail_data:
        try:
            image = Image.open(
                BytesIO(thumbnail_data)
            )

            thumbnail = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(120, 68)
            )

            thumbnail_label.configure(
                image=thumbnail,
                text="",
                fg_color="transparent"
)

            thumbnail_label.image = thumbnail

        except Exception as error:
            print("Thumbnail gagal:", error)

    global is_preview_loading

    is_preview_loading = False

    preview_button.configure(
        text="↗",
        state="normal"
)
    


def preview_failed(error):
    global is_preview_loading

    is_preview_loading = False

    print("Gagal ambil info:", error)

    preview_button.configure(
        text="↗",
        state="normal"
    )

spinner_frames = ["◐", "◓", "◑", "◒"]
spinner_index = 0
is_preview_loading = False


def animate_preview_spinner():
    global spinner_index

    if not is_preview_loading:
        return

    preview_button.configure(
        text=spinner_frames[spinner_index]
    )

    spinner_index = (spinner_index + 1) % len(spinner_frames)

    app.after(100, animate_preview_spinner)

def fetch_info():
    url = url_entry.get()

    if not url:
        print("URL kosong")
        return

    global is_preview_loading

    is_preview_loading = True

    preview_button.configure(
        state="disabled"
)

    animate_preview_spinner()

    thread = threading.Thread(
        target=run_fetch_info,
        args=(url,),
        daemon=True
    )

    thread.start()

preview_button = ctk.CTkButton(
    main_frame,
    text="↗",
    width=36,
    height=36,
    fg_color="#212121",
    hover_color="#333333",
    text_color="white",
    corner_radius=100,
    font=("Space Grotesk", 16, "bold"),
    command=fetch_info
)

preview_button.place(x=825, y=203 + CONTENT_Y)

preview_title = ctk.CTkLabel(
    main_frame,
    text="",
    font=("Space Grotesk", 14, "bold"),
    text_color="#212121"
    
)
preview_title.place(x=50, y=620 + CONTENT_Y)


preview_meta = ctk.CTkLabel(
    main_frame,
    text="",
    font=("Space Grotesk", 12),
    text_color="#737373"
)
preview_meta.place(x=50, y=645 + CONTENT_Y)

def download_finished():
    download_button.configure(
        text="COMPLETE",
        text_color="black",
        fg_color="#B8F95B",
        hover_color="#9CF520",
        state="normal"
)
    url_entry.configure(state="normal")

    progress_bar.set(1)
    progress_label.configure(text="100%")



    print("Download selesai!")


def download_failed(error):
    download_button.configure(
        text="FAILED",
        fg_color="#212121",
        hover_color="#2A2A2A",
        text_color="white",
        state="normal"
    )

    url_entry.configure(state="normal")

    progress_bar.set(0)
    progress_label.configure(text="0%")

    error_text = str(error).lower()

    if (
        "getaddrinfo failed" in error_text
        or "failed to resolve" in error_text
        or "network" in error_text
        or "timed out" in error_text
        or "connection" in error_text
    ):
        message = "Network error. Check your internet connection."

    elif (
        "unsupported url" in error_text
        or "invalid url" in error_text
        or "not a valid url" in error_text
        or "no suitable extractor" in error_text
    ):
        message = "Invalid or unsupported link."

    else:
        message = "Download failed. Please try again."

    error_label.configure(text=message)

    print("Error:", error)

def update_progress(value):
    if value > 0:
        download_button.configure(text="DOWNLOADING")

    progress_bar.set(value)

    percent = int(value * 100)
    progress_label.configure(text=f"{percent}%")
        
def run_download(url, save_folder, quality, media_format, custom_name):
    max_attempts = 3

    for attempt in range(1, max_attempts + 1):
        try:
            download_media(
                url=url,
                save_folder=save_folder,
                quality=quality,
                media_format=media_format,
                custom_name=custom_name,
                progress_callback=lambda value: app.after(
                    0,
                    update_progress,
                    value
                )
            )

            app.after(0, download_finished)
            return

        except Exception as error:
            print(f"Percobaan {attempt} gagal:", error)

            if attempt == max_attempts:
                app.after(
                    0,
                    lambda e=error: download_failed(e)
                )
            else:
                app.after(
                    0,
                    lambda a=attempt: download_button.configure(
                        text=f"RETRYING {a}/3..."
                    )
                )


def start_download():
    url = url_entry.get()
    save_folder = save_entry.get()
    quality = quality_value
    media_format = format_value
    custom_name = custom_name_entry.get().strip()

    if not url:
        print("URL kosong")
        return

    if not save_folder:
        print("Folder belum dipilih")
        return

    download_button.configure(
        text="PROCESSING",
        fg_color="#212121",
        hover_color="#2A2A2A",
        state="disabled"
)
    url_entry.configure(state="disabled")

    progress_bar.set(0)
    progress_label.configure(text="0%")

    thread = threading.Thread(
        target=run_download,
        args=(url, save_folder, quality, media_format, custom_name),
        daemon=True
    )

    thread.start()


# =========================
# Download Button
# =========================

download_button = ctk.CTkButton(
    main_frame,
    text="Download ↗",
    width=155,
    height=48,
    fg_color="#212121",
    hover_color="#2A2A2A",
    text_color="white",
    corner_radius=24,
    font=("Space Grotesk", 16, "bold"),
    command=start_download
)

download_button.place(x=715, y=460 + CONTENT_Y)

# =========================
# Progress Bar
# =========================

progress_bar = ctk.CTkProgressBar(
    main_frame,
    width=620,
    height=10,
    corner_radius=5,
    fg_color="#EAEAEA",
    progress_color="#212121"
)
progress_bar.place(x=50, y=480 + CONTENT_Y)
progress_bar.set(0)


progress_label = ctk.CTkLabel(
    main_frame,
    text="0%",
    font=("Space Grotesk", 12),
    text_color="#737373"
)
progress_label.place(x=50, y=500 + CONTENT_Y)

error_label = ctk.CTkLabel(
    main_frame,
    text="",
    font=("Space Grotesk", 12),
    text_color="#D92D20",
    anchor="w"
)

error_label.place(x=100, y=500 + CONTENT_Y)

url_entry.bind("<KeyRelease>", reset_download_state, add="+")

# =========================
# Media Preview
# =========================
preview_card = ctk.CTkFrame(
    main_frame,
    width=400,
    height=130,
    fg_color="white",
    border_width=2,
    border_color="#212121",
    corner_radius=24
)
preview_card.place(x=30, y=550 + CONTENT_Y)

preview_card.pack_propagate(False)

second_card = ctk.CTkFrame(
    main_frame,
    width=400,
    height=130,
    fg_color="#212121",
    border_width=2,
    border_color="#212121",
    corner_radius=24
)

download_icon_image = ctk.CTkImage(
    light_image=Image.open(resource_path("assets/images/downloads.png")),
    dark_image=Image.open(resource_path("assets/images/downloads.png")),
    size=(120, 120)
)

download_icon = ctk.CTkLabel(
    second_card,
    image=download_icon_image,
    text="",
    fg_color="transparent"
)

download_icon.place(x=270, y=5)


summary_title = ctk.CTkLabel(
    second_card,
    text="  Download Summary  ",
    font=("Space Grotesk", 20, "bold"),
    text_color="#212121",
    fg_color="#F2F2F2",
    anchor="w"
)
summary_title.place(x=30, y=40)


summary_format = ctk.CTkLabel(
    second_card,
    text="Format:     Video    |",
    font=("Space Grotesk", 11, "bold"),
    text_color="#F2F2F2",
    anchor="w"
)
summary_format.place(x=30, y=70)


summary_quality = ctk.CTkLabel(
    second_card,
    text="Quality:     Best",
    font=("Space Grotesk", 11, "bold"),
    text_color="#F2F2F2",
    anchor="w"
)
summary_quality.place(x=150, y=70)

second_card.place(x=450, y=550 + CONTENT_Y)
second_card.pack_propagate(False)


thumbnail_label = ctk.CTkLabel(
    preview_card,
    text="▧",
    width=170,
    height=96,
    fg_color="#EEEEEE",
    text_color="#AAAAAA",
    corner_radius=16,
    font=("Space Grotesk", 32)
)
thumbnail_label.place(x=16, y=17)


preview_title = ctk.CTkLabel(
    preview_card,
    text="Preview will appear here ...",
    font=("Space Grotesk", 14, "bold"),
    text_color="#212121",
    fg_color="transparent",
    anchor="w",
    justify="left",
    width=170,
    wraplength=165,
)
preview_title.place(x=200, y=30)


preview_meta = ctk.CTkLabel(
    preview_card,
    text="Paste a link and click preview",
    font=("Space Grotesk", 11),
    text_color="#737373",
    fg_color="transparent",
    anchor="w",
    justify="left",
    width=170,
    wraplength=165,
)
preview_meta.place(x=200, y=68)

# =========================
# Start App
# =========================

yt_raw = Image.open(resource_path("assets/logos/yt.png")).convert("LA").convert("RGBA")

youtube_img = ctk.CTkImage(
    light_image=yt_raw,
    size=(32, int(32 * yt_raw.height / yt_raw.width))
)

youtube_logo = ctk.CTkLabel(
    main_frame,
    image=youtube_img,
    text="",
    fg_color="transparent"
)

youtube_logo.place(x=50, y=350)
tt_raw = Image.open(resource_path("assets/logos/tt.png")).convert("LA").convert("RGBA")
tt_img = ctk.CTkImage(
    light_image=tt_raw,
    size=(32, int(32 * tt_raw.height / tt_raw.width))
)
tt_logo = ctk.CTkLabel(main_frame, image=tt_img, text="", fg_color="transparent")
tt_logo.place(x=110, y=350)


ig_raw = Image.open(resource_path("assets/logos/ig.png")).convert("LA").convert("RGBA")
ig_img = ctk.CTkImage(
    light_image=ig_raw,
    size=(32, int(32 * ig_raw.height / ig_raw.width))
)
ig_logo = ctk.CTkLabel(main_frame, image=ig_img, text="", fg_color="transparent")
ig_logo.place(x=170, y=350)


x_raw = Image.open(resource_path("assets/logos/x.png")).convert("LA").convert("RGBA")
x_img = ctk.CTkImage(
    light_image=x_raw,
    size=(32, int(32 * x_raw.height / x_raw.width))
)
x_logo = ctk.CTkLabel(main_frame, image=x_img, text="", fg_color="transparent")
x_logo.place(x=230, y=350)


fb_raw = Image.open(resource_path("assets/logos/fb.png")).convert("LA").convert("RGBA")
fb_img = ctk.CTkImage(
    light_image=fb_raw,
    size=(32, int(32 * fb_raw.height / fb_raw.width))
)
fb_logo = ctk.CTkLabel(main_frame, image=fb_img, text="", fg_color="transparent")
fb_logo.place(x=290, y=350)

beta_label = ctk.CTkLabel(
    main_frame,
    text="Beta Version",
    font=("Space Grotesk", 13, "bold"),
    text_color="#111111",
    fg_color="#B8F95B",
    corner_radius=4
)
beta_label.place(x=50, y=140 + CONTENT_Y)


beta_text = ctk.CTkLabel(
    main_frame,
    text="This app is still in development. Some features may change or behave unexpectedly.",
    font=("Space Grotesk", 10),
    text_color="#555555",
    anchor="w"
)
beta_text.place(x=150, y=140 + CONTENT_Y)

app.mainloop()