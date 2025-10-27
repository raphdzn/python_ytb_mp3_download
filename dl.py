import os
import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox


def create_output_directory(output_dir="output"):
    """Create the output folder if it does not exist."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def download_youtube_to_mp3(links_file, output_dir="output"):
    """Download YouTube videos as MP3 from a text file.

    Returns a tuple (success_count, fail_count).
    """
    # Get the absolute path of the ffmpeg folder in the project
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_path = os.path.join(script_dir, "ffmpeg")

    # Check if FFmpeg binaries exist
    if not os.path.exists(os.path.join(ffmpeg_path, "ffmpeg.exe")):
        raise FileNotFoundError("ffmpeg.exe not found in the ffmpeg folder. Make sure it is included in the project.")
    if not os.path.exists(os.path.join(ffmpeg_path, "ffprobe.exe")):
        raise FileNotFoundError("ffprobe.exe not found in the ffmpeg folder. Make sure it is included in the project.")

    # yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'ffmpeg_location': ffmpeg_path,  # Use local ffmpeg folder
    }

    # Read links from the text file
    try:
        with open(links_file, 'r', encoding='utf-8') as file:
            links = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: The file {links_file} was not found.")
        return 0, 0
    except Exception as e:
        print(f"Error reading the file: {e}")
        return 0, 0

    success_count = 0
    fail_count = 0

    # Download each link
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for link in links:
            try:
                print(f"Downloading: {link}")
                ydl.download([link])
                print(f"Download finished for: {link}")
                success_count += 1
            except Exception as e:
                print(f"Error downloading {link}: {e}")
                fail_count += 1

    return success_count, fail_count


def choose_file_dialog(root):
    """Open a dialog to choose a file and return its path."""
    file_path = filedialog.askopenfilename(
        parent=root,
        title="Choose the file containing the links (1 link per line)",
        filetypes=[("Text files", "*.txt"), ("All files", "*")]
    )
    return file_path


def run_gui():
    root = tk.Tk()
    root.title("YouTube to MP3 Downloader")
    root.geometry("480x170")
    root.resizable(False, False)

    # --- Modern dark theme colors ---
    bg_main = "#18191A"  # almost black
    bg_frame = "#23272F"  # dark gray
    fg_text = "#F1F1F1"   # light text
    accent = "#3A8DFF"    # blue accent
    btn_bg = "#23272F"
    btn_fg = fg_text
    btn_active = "#31343B"
    border_color = "#222"
    font_main = ("Segoe UI", 11)
    font_bold = ("Segoe UI", 11, "bold")

    root.configure(bg=bg_main)

    selected_file_var = tk.StringVar(value="No file selected")

    def on_choose_file():
        path = choose_file_dialog(root)
        if path:
            selected_file_var.set(path)

    def on_start():
        links_file = selected_file_var.get()
        if not links_file or links_file == "No file selected":
            messagebox.showwarning("No file", "Please choose a file containing the links first.")
            return
        try:
            create_output_directory()
            success, fail = download_youtube_to_mp3(links_file)
            message = f"Finished. Success: {success}, Failed: {fail}"
            messagebox.showinfo("Finished", message)
        except FileNotFoundError as fnf:
            messagebox.showerror("FFmpeg Error", str(fnf))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # --- Frame ---
    frame = tk.Frame(root, bg=bg_frame, padx=18, pady=18, bd=0, relief="flat")
    frame.pack(fill=tk.BOTH, expand=True, padx=18, pady=18)

    # --- Label ---
    label = tk.Label(
        frame,
        textvariable=selected_file_var,
        wraplength=420,
        anchor='w',
        justify='left',
        bg=bg_frame,
        fg=fg_text,
        font=font_main,
        bd=0,
        highlightthickness=0
    )
    label.pack(fill=tk.X, pady=(0, 14))

    # --- Buttons ---
    btn_frame = tk.Frame(frame, bg=bg_frame)
    btn_frame.pack(fill=tk.X)

    style = {
        "bg": btn_bg,
        "fg": btn_fg,
        "activebackground": btn_active,
        "activeforeground": accent,
        "font": font_bold,
        "bd": 0,
        "relief": "flat",
        "highlightthickness": 0,
        "cursor": "hand2",
        "padx": 18,
        "pady": 8,
    }

    choose_btn = tk.Button(
        btn_frame,
        text="Choose file",
        command=on_choose_file,
        **style
    )
    choose_btn.pack(side=tk.LEFT, padx=(0, 10))

    start_btn = tk.Button(
        btn_frame,
        text="Start download",
        command=on_start,
        **style
    )
    start_btn.pack(side=tk.LEFT)

    # --- Rounded corners (Windows 11+ only, best effort) ---
    try:
        root.wm_attributes('-transparentcolor', '#123456')  # hack for rounded corners if using custom window shape
    except Exception:
        pass

    # --- Modern font for all widgets ---
    root.option_add("*Font", font_main)

    # --- Remove focus border on buttons ---
    root.option_add("*Button.highlightThickness", 0)

    root.mainloop()


def main():
    # Launch the graphical interface
    run_gui()


if __name__ == "__main__":
    main()
