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
app.geometry("920x670")
app.resizable(False, False)


# =========================
# Main Container
# =========================

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
    height=760,
    fg_color="white",
    corner_radius=0
)
main_frame.pack()
main_frame.pack_propagate(False)


# =========================
# Branding
# =========================

brand = ctk.CTkLabel(
    main_frame,
    text="PRD.",
    font=("Poppins", 24, "bold"),
    text_color="#111111"
)
brand.place(x=50, y=35)


# =========================
# Title
# =========================

title = ctk.CTkLabel(
    main_frame,
    text="Media Downloader",
    font=("Poppins", 30, "bold"),
    text_color="#111111"
)
title.place(x=50, y=100)

subtitle = ctk.CTkLabel(
    main_frame,
    text="Download media from your favorite platforms.",
    font=("Poppins", 22, "bold"),
    text_color="#737373"
)
subtitle.place(x=50, y=145)


# =========================
# URL Input
# =========================

url_entry = ctk.CTkEntry(
    main_frame,
    width=760,
    height=52,
    placeholder_text="Paste media URL...",
    fg_color="white",
    text_color="#111111",
    placeholder_text_color="#000000",
    border_color="#000000",
    border_width=2,
    corner_radius=26,
    font=("Poppins", 12)
)

url_entry.place(x=50, y=195)


def paste_url():
    try:
        clipboard_text = app.clipboard_get()

        url_entry.delete(0, "end")
        url_entry.insert(0, clipboard_text)

    except Exception:
        pass


paste_button = ctk.CTkButton(
    main_frame,
    text="↗",
    width=36,
    height=36,
    fg_color="#111111",
    hover_color="#333333",
    text_color="white",
    corner_radius=100,
    font=("Poppins", 16, "bold"),
    command=paste_url
)
paste_button.place(x=825, y=203)




# =========================
# Format & Quality
# =========================

format_label = ctk.CTkLabel(
    main_frame,
    text="FORMAT",
    font=("Poppins", 12, "bold"),
    text_color="#111111"
)
format_label.place(x=50, y=260)


quality_label = ctk.CTkLabel(
    main_frame,
    text="QUALITY",
    font=("Poppins", 12, "bold"),
    text_color="#111111"
)
quality_label.place(x=460, y=260)


def change_format(selected_format):
    global quality_value, quality_options

    if selected_format == "Video":
        quality_value = "Best"
        quality_options = ["Best", "1080p", "720p", "480p"]

    elif selected_format == "Audio":
        quality_value = "320 kbps"
        quality_options = ["320 kbps", "192 kbps", "128 kbps"]

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
            text_color="white",
            corner_radius=12,
            font=("Poppins", 13),
            anchor="w",
            command=lambda v=value: choose_quality(v)
        )

        option.place(x=10, y=8 + (i * 39))


format_value = "Video"


def toggle_format_dropdown():
    if format_dropdown.winfo_ismapped():
        format_dropdown.place_forget()
    else:
        format_dropdown.place(x=50, y=338)
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
    fg_color="#111111",
    hover_color="#2A2A2A",
    text_color="white",
    corner_radius=21,
    font=("Poppins", 13, "bold"),
    anchor="w",
    command=toggle_format_dropdown
)

format_button.place(x=50, y=290)


format_dropdown = ctk.CTkFrame(
    main_frame,
    width=180,
    height=88,
    fg_color="#111111",
    corner_radius=16
)


video_option = ctk.CTkButton(
    format_dropdown,
    text="Video",
    width=160,
    height=34,
    fg_color="transparent",
    hover_color="#2A2A2A",
    text_color="white",
    corner_radius=12,
    font=("Poppins", 13),
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
    hover_color="#2A2A2A",
    text_color="white",
    corner_radius=12,
    font=("Poppins", 13),
    anchor="w",
    command=lambda: choose_format("Audio")
)
audio_option.place(x=10, y=47)


quality_value = "Best"


def toggle_quality_dropdown():
    if quality_dropdown.winfo_ismapped():
        quality_dropdown.place_forget()
    else:
        quality_dropdown.place(x=460, y=338)
        quality_dropdown.lift()


def choose_quality(value):
    global quality_value

    quality_value = value
    quality_button.configure(text=f"{value}   ▾")
    quality_dropdown.place_forget()


quality_button = ctk.CTkButton(
    main_frame,
    text="Best   ▾",
    width=100,
    height=42,
    fg_color="#111111",
    hover_color="#2A2A2A",
    text_color="white",
    corner_radius=21,
    font=("Poppins", 13, "bold"),
    anchor="w",
    command=toggle_quality_dropdown
)

quality_button.place(x=460, y=290)


quality_dropdown = ctk.CTkFrame(
    main_frame,
    width=180,
    height=166,
    fg_color="#111111",
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
        hover_color="#2A2A2A",
        text_color="white",
        corner_radius=12,
        font=("Poppins", 13),
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
    font=("Poppins", 12, "bold"),
    text_color="#737373"
)
save_label.place(x=50, y=350)


save_entry = ctk.CTkEntry(
    main_frame,
    width=760,
    height=48,
    fg_color="white",
    text_color="#111111",
    border_color="#000000",
    border_width=2,
    corner_radius=26,
    font=("Poppins", 14)
)
save_entry.place(x=50, y=380)


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
    fg_color="#111111",
    hover_color="#333333",
    text_color="white",
    corner_radius=100,
    font=("Poppins", 16, "bold"),
    command=browse_folder
)

browse_button.place(x=825, y=387)


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

    global is_preview_loading

    is_preview_loading = False

    preview_button.configure(
        text="↗",
        state="normal"
)


def preview_failed(error):
    print("Gagal ambil info:", error)

    preview_button.configure(
        text="PREVIEW",
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
    fg_color="#111111",
    hover_color="#333333",
    text_color="white",
    corner_radius=100,
    font=("Poppins", 16, "bold"),
    command=fetch_info
)

preview_button.place(x=825, y=203)

preview_title = ctk.CTkLabel(
    main_frame,
    text="",
    font=("Poppins", 14, "bold"),
    text_color="#111111"
)
preview_title.place(x=50, y=620)


preview_meta = ctk.CTkLabel(
    main_frame,
    text="",
    font=("Poppind", 12),
    text_color="#737373"
)
preview_meta.place(x=50, y=645)

def download_finished():
    download_button.configure(
        text="COMPLETE",
        fg_color="#22C55E",
        hover_color="#16A34A",
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
    quality = quality_value
    media_format = format_value

    if not url:
        print("URL kosong")
        return

    if not save_folder:
        print("Folder belum dipilih")
        return

    download_button.configure(
        text="DOWNLOADING",
        fg_color="#111111",
        hover_color="#2A2A2A",
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
    text="Download",
    width=155,
    height=48,
    fg_color="#111111",
    hover_color="#2A2A2A",
    text_color="white",
    corner_radius=24,
    font=("Poppins", 14, "bold"),
    command=start_download
)

download_button.place(x=715, y=460)

# =========================
# Progress Bar
# =========================

progress_bar = ctk.CTkProgressBar(
    main_frame,
    width=620,
    height=10,
    corner_radius=5,
    fg_color="#EAEAEA",
    progress_color="#111111"
)
progress_bar.place(x=50, y=480)
progress_bar.set(0)


progress_label = ctk.CTkLabel(
    main_frame,
    text="0%",
    font=("Poppins", 12),
    text_color="#737373"
)
progress_label.place(x=50, y=500)

# =========================
# Media Preview
# =========================
thumbnail_label = ctk.CTkLabel(
    main_frame,
    text="",
    width=120,
    height=68
)
thumbnail_label.place(x=50, y=570)

preview_title = ctk.CTkLabel(
    main_frame,
    text="",
    font=("Poppins", 14, "bold"),
    text_color="#111111",
    anchor="w",
    width=700
)
preview_title.place(x=190, y=570)

preview_meta = ctk.CTkLabel(
    main_frame,
    text="",
    font=("Poppins", 12),
    text_color="#737373",
    anchor="w",
    width=700
)
preview_meta.place(x=190, y=600)

# =========================
# Start App
# =========================

app.mainloop()