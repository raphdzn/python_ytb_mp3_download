# YouTube MP3 Downloader

A Python script to download YouTube videos as MP3 files from a text file containing links. Includes a modern graphical interface (Tkinter).

## Requirements
- **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/).
- **Tkinter**: Usually included with Python on Windows. If missing, see below.
- **FFmpeg**: Place the FFmpeg binaries in the `ffmpeg/` folder (see instructions below).
- A virtual environment (venv) is recommended for dependency management.

## Installation

```sh
git clone <REPO_URL>
cd python_ytb_mp3_download
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

## Running the App

```sh
python dl.py
```

## Installing Tkinter
- **Windows**: Tkinter is included by default with the official Python installer. If you get an error like `No module named 'tkinter'`, reinstall Python and ensure "tcl/tk and IDLE" is selected during installation.
- **Linux (Debian/Ubuntu/WSL)**:
  ```sh
  sudo apt update
  sudo apt install python3-tk
  ```
- **macOS**: Tkinter is included with the official Python installer from python.org.

## Installing FFmpeg
1. Download FFmpeg for your OS:
   - [FFmpeg Windows builds](https://www.gyan.dev/ffmpeg/builds/)
   - [FFmpeg macOS/Linux](https://ffmpeg.org/download.html)
2. Extract/copy the following files into the `ffmpeg/` folder in your project directory:
   - `ffmpeg.exe` (Windows) or `ffmpeg` (Linux/macOS)
   - `ffprobe.exe` (Windows) or `ffprobe` (Linux/macOS)
   - (Optional) `ffplay.exe` or `ffplay`
3. The folder structure should look like:
   ```
   python_ytb_mp3_download/
     ffmpeg/
       ffmpeg.exe
       ffprobe.exe
       ffplay.exe
   ```

## Usage
- Prepare a text file (e.g. `links.txt`) with one YouTube link per line.
- Launch the app: `python dl.py`
- Use the interface to select your links file and start downloading.
- MP3 files will be saved in the `output/` folder.

## Packaging as an EXE (Windows)
1. Install PyInstaller:
   ```sh
   pip install pyinstaller
   ```
2. Build the executable:
   ```sh
   pyinstaller --onefile --add-data "ffmpeg;ffmpeg" dl.py
   ```
   The exe will be in the `dist/` folder.

---

Feel free to open issues or contribute!
