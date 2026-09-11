import customtkinter as ctk
from tkinter import filedialog
from downloader import download_media, get_media_info
import threading
from PIL import Image
from io import BytesIO
from urllib.request import urlopen


ctk.set_appearance_mode("light")

app = ctk.CTk()

app.title("PRD Media Downloader")
app.geometry("900x720")
app.resizable(False, False)


# =========================
# Main Container
# =========================

main_frame = ctk.CTkFrame(
    app,
    fg_color="white",
    corner_radius=0
)
main_frame.pack(fill="both", expand=True)


# =========================
# Branding
# =========================

brand = ctk.CTkLabel(
    main_frame,
    text="PRD.",
    font=("Arial", 24, "bold"),
    text_color="#111111"
)
brand.place(x=50, y=35)


# =========================
# Title
# =========================

title = ctk.CTkLabel(
    main_frame,
    text="Media Downloader",
    font=("Arial", 32, "bold"),
    text_color="#111111"
)
title.place(x=50, y=100)

subtitle = ctk.CTkLabel(
    main_frame,
    text="Download media from your favorite platforms.",
    font=("Arial", 14),
    text_color="#737373"
)
subtitle.place(x=50, y=145)


# =========================
# URL Input
# =========================

url_entry = ctk.CTkEntry(
    main_frame,
    width=680,
    height=48,
    placeholder_text="Paste media URL...",
    fg_color="white",
    text_color="#111111",
    placeholder_text_color="#9A9A9A",
    border_color="#DADADA",
    border_width=1,
    corner_radius=8,
    font=("Arial", 14)
)
url_entry.place(x=50, y=200)


def paste_url():
    try:
        clipboard_text = app.clipboard_get()

        url_entry.delete(0, "end")
        url_entry.insert(0, clipboard_text)

    except Exception:
        pass


paste_button = ctk.CTkButton(
    main_frame,
    text="PASTE",
    width=100,
    height=48,
    fg_color="white",
    hover_color="#F2F2F2",
    text_color="#111111",
    border_color="#DADADA",
    border_width=1,
    corner_radius=8,
    font=("Arial", 13, "bold"),
    command=paste_url
)
paste_button.place(x=750, y=200)




# =========================
# Format & Quality
# =========================

format_label = ctk.CTkLabel(
    main_frame,
    text="FORMAT",
    font=("Arial", 12, "bold"),
    text_color="#737373"
)
format_label.place(x=50, y=285)

quality_label = ctk.CTkLabel(
    main_frame,
    text="QUALITY",
    font=("Arial", 12, "bold"),
    text_color="#737373"
)
quality_label.place(x=460, y=285)

def change_format(selected_format):
    if selected_format == "Video":
        quality_menu.configure(
            values=["Best", "1080p", "720p", "480p"]
        )
        quality_menu.set("Best")

    elif selected_format == "Audio":
        quality_menu.configure(
            values=["320 kbps", "192 kbps", "128 kbps"]
        )
        quality_menu.set("320 kbps")
        
format_menu = ctk.CTkOptionMenu(
    main_frame,
    values=["Video", "Audio"],
    width=390,
    height=48,
    fg_color="white",
    button_color="white",
    button_hover_color="#F2F2F2",
    text_color="#111111",
    dropdown_fg_color="white",
    dropdown_text_color="#111111",
    dropdown_hover_color="#F2F2F2",
    corner_radius=8,
    font=("Arial", 14),
    command=change_format
)

format_menu.place(x=50, y=315)


quality_menu = ctk.CTkOptionMenu(
    main_frame,
    values=["Best", "1080p", "720p", "480p"],
    width=390,
    height=48,
    fg_color="white",
    button_color="white",
    button_hover_color="#F2F2F2",
    text_color="#111111",
    dropdown_fg_color="white",
    dropdown_text_color="#111111",
    dropdown_hover_color="#F2F2F2",
    corner_radius=8,
    font=("Arial", 14)
)
quality_menu.place(x=460, y=315)


# =========================
# Save Location
# =========================

save_label = ctk.CTkLabel(
    main_frame,
    text="SAVE TO",
    font=("Arial", 12, "bold"),
    text_color="#737373"
)
save_label.place(x=50, y=395)


save_entry = ctk.CTkEntry(
    main_frame,
    width=680,
    height=48,
    fg_color="white",
    text_color="#111111",
    border_color="#DADADA",
    border_width=1,
    corner_radius=8,
    font=("Arial", 14)
)
save_entry.place(x=50, y=425)


def browse_folder():
    folder = filedialog.askdirectory()

    if folder:
        save_entry.delete(0, "end")
        save_entry.insert(0, folder)


browse_button = ctk.CTkButton(
    main_frame,
    text="BROWSE",
    width=100,
    height=48,
    fg_color="white",
    hover_color="#F2F2F2",
    text_color="#111111",
    border_color="#DADADA",
    border_width=1,
    corner_radius=8,
    font=("Arial", 13, "bold"),
    command=browse_folder
)
browse_button.place(x=750, y=425)


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
            lambda: preview_failed(error)
        )

def show_preview(info, thumbnail_data):
    preview_title.configure(
        text=info["title"]
    )

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
                image=thumbnail
            )

            thumbnail_label.image = thumbnail

        except Exception as error:
            print("Thumbnail gagal:", error)

    preview_button.configure(
        text="PREVIEW",
        state="normal"
    )


def preview_failed(error):
    print("Gagal ambil info:", error)

    preview_button.configure(
        text="PREVIEW",
        state="normal"
    )

def fetch_info():
    url = url_entry.get()

    if not url:
        print("URL kosong")
        return

    preview_button.configure(
        text="LOADING...",
        state="disabled"
    )

    thread = threading.Thread(
        target=run_fetch_info,
        args=(url,),
        daemon=True
    )

    thread.start()

preview_button = ctk.CTkButton(
    main_frame,
    text="PREVIEW",
    width=100,
    height=36,
    fg_color="#111111",
    hover_color="#2A2A2A",
    text_color="white",
    corner_radius=8,
    font=("Arial", 12, "bold"),
    command=fetch_info
)

preview_button.place(x=750, y=255)

preview_title = ctk.CTkLabel(
    main_frame,
    text="",
    font=("Arial", 14, "bold"),
    text_color="#111111"
)
preview_title.place(x=50, y=620)


preview_meta = ctk.CTkLabel(
    main_frame,
    text="",
    font=("Arial", 12),
    text_color="#737373"
)
preview_meta.place(x=50, y=645)

def download_finished():
    download_button.configure(
        text="DOWNLOAD COMPLETE",
        state="normal"
    )

    progress_bar.set(1)
    progress_label.configure(text="100%")

    print("Download selesai!")


def download_failed(error):
    download_button.configure(
        text="DOWNLOAD",
        state="normal"
    )

    progress_bar.set(0)
    progress_label.configure(text="0%")

    print("Error:", error)

def update_progress(value):
    progress_bar.set(value)

    percent = int(value * 100)
    progress_label.configure(text=f"{percent}%")
        
def run_download(url, save_folder, quality, media_format):
    try:
        download_media(
        url=url,
        save_folder=save_folder,
        quality=quality,
        media_format=media_format,
        progress_callback=lambda value: app.after(
            0,
            update_progress,
            value
        )
)

        app.after(0, download_finished)

    except Exception as error:
        app.after(
            0,
            lambda: download_failed(error)
        )


def start_download():
    url = url_entry.get()
    save_folder = save_entry.get()
    quality = quality_menu.get()
    media_format = format_menu.get()

    if not url:
        print("URL kosong")
        return

    if not save_folder:
        print("Folder belum dipilih")
        return

    download_button.configure(
        text="DOWNLOADING...",
        state="disabled"
    )

    progress_bar.set(0)
    progress_label.configure(text="0%")

    thread = threading.Thread(
        target=run_download,
        args=(url, save_folder, quality, media_format),
        daemon=True
    )

    thread.start()


# =========================
# Download Button
# =========================

download_button = ctk.CTkButton(
    main_frame,
    text="DOWNLOAD",
    width=800,
    height=52,
    fg_color="#111111",
    hover_color="#2A2A2A",
    text_color="white",
    corner_radius=8,
    font=("Arial", 14, "bold"),
    command=start_download
)
download_button.place(x=50, y=510)


# =========================
# Progress Bar
# =========================

progress_bar = ctk.CTkProgressBar(
    main_frame,
    width=800,
    height=10,
    corner_radius=5,
    fg_color="#EAEAEA",
    progress_color="#111111"
)
progress_bar.place(x=50, y=585)
progress_bar.set(0)


progress_label = ctk.CTkLabel(
    main_frame,
    text="0%",
    font=("Arial", 12),
    text_color="#737373"
)
progress_label.place(x=815, y=605)

# =========================
# Media Preview
# =========================
thumbnail_label = ctk.CTkLabel(
    main_frame,
    text="",
    width=120,
    height=68
)
thumbnail_label.place(x=50, y=625)

preview_title = ctk.CTkLabel(
    main_frame,
    text="",
    font=("Arial", 14, "bold"),
    text_color="#111111",
    anchor="w",
    width=700
)
preview_title.place(x=190, y=625)

preview_meta = ctk.CTkLabel(
    main_frame,
    text="",
    font=("Arial", 12),
    text_color="#737373",
    anchor="w",
    width=700
)
preview_meta.place(x=190, y=655)

# =========================
# Start App
# =========================

app.mainloop()