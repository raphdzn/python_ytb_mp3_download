# YouTube MP3 Downloader

A user-friendly desktop application to batch download YouTube videos as high-quality MP3 files from a list of links.

![App Screenshot](assets/logo.ico) 
*(Note: App icon shown. The actual UI is a simple window with drag-and-drop support.)*

## Features

- **Batch Downloading**: Process multiple YouTube links from a single `.txt` file.
- **High-Quality Audio**: Converts videos to MP3 files at 320kbps.
- **Simple Interface**: A clean, modern GUI built with PyQt6.
- **Drag & Drop**: Easily select your links file by dragging it onto the application window.
- **Standalone Executable**: Can be packaged into a single executable file for easy distribution.

## Technical Stack

- **Python 3.8+**
- **yt-dlp**: The core engine for downloading from YouTube.
- **PyQt6**: For the graphical user interface.
- **FFmpeg**: For audio extraction and conversion to MP3.

---

## Prerequisites

1.  **Python 3.8 or newer**:
    - Download from [python.org](https://www.python.org/downloads/).
    - During installation on Windows, ensure "Add Python to PATH" is checked.

2.  **FFmpeg**:
    - **Windows**:
        1.  Download an FFmpeg build (e.g., from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)).
        2.  Extract the archive.
        3.  From the `bin` folder of the extracted files, copy `ffmpeg.exe` and `ffprobe.exe` into the `ffmpeg/` directory at the root of this project.
    - **Linux (Debian/Ubuntu-based)**:
        - Install it via the system's package manager. The application will use the system-wide installation.
          ```sh
          sudo apt update && sudo apt install ffmpeg
          ```

---

## Development Setup

To run or modify the project in a development environment:

1.  **Clone the repository:**
    ```sh
    git clone <YOUR_REPO_URL>
    cd python_ytb_mp3_download
    ```

2.  **Create and activate a virtual environment:**
    - **Windows (PowerShell):**
      ```sh
      python -m venv venv
      .\venv\Scripts\Activate.ps1
      ```
    - **macOS/Linux:**
      ```sh
      python -m venv venv
      source venv/bin/activate
      ```

3.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```sh
    python dl.py
    ```

---

## How to Use the Application

1.  Create a text file (e.g., `links.txt`).
2.  Add one YouTube URL per line in the file.
3.  Launch the application.
4.  Either **drag and drop** the `.txt` file onto the window or click the **"Choose a file..."** button to select it.
5.  Click **"Start Download"**.
6.  The MP3 files will be saved in the `output/` folder, which is created where the application is running.

---

## Compiling the Application (Packaging)

You can package the application into a single standalone executable using **PyInstaller**.

1.  **Install PyInstaller:**
    ```sh
    pip install pyinstaller
    ```

2.  **Prepare the icon (Optional):**
    - For a custom icon on Windows, you need an `.ico` file. Convert the `assets/logo.png` to `assets/logo.ico` using an online converter and place it in the `assets` folder.

3.  **Run the build command:**
    - **For Windows:**
      ```sh
      pyinstaller --onefile --noconsole --icon "assets/logo.ico" --add-data "ffmpeg;ffmpeg" --add-data "assets;assets" dl.py
      ```
    - **For Linux:**
      ```sh
      pyinstaller --onefile --noconsole --icon "assets/logo.png" --add-data "ffmpeg:ffmpeg" --add-data "assets:assets" dl.py
      ```

    **Command breakdown:**
    - `--onefile`: Bundles everything into a single `.exe` (or executable file on Linux).
    - `--noconsole`: Hides the background command-line window.
    - `--icon`: Sets the file icon (and default window icon).
    - `--add-data "SOURCE:DEST"`: Bundles additional files/folders. The path separator is `;` for Windows and `:` for Linux/macOS.

4.  **Find the executable:**
    - The final application will be located in the `dist/` directory.

---

## Project Structure

```
├───assets/
│   └───logo.ico      # Application icon (Windows)
│   └───logo.png      # Application icon (Linux/Source)
├───ffmpeg/
│   ├───ffmpeg.exe    # For Windows
│   └───ffprobe.exe   # For Windows
├───dl.py             # Main application script (PyQt6 UI and logic)
├───requirements.txt  # Python dependencies
└───README.md         # This file
```

Feel free to open issues or contribute!
