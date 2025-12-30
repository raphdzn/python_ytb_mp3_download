import os
import sys

import yt_dlp
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# --- Helper for PyInstaller ---


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# --- Business Logic ---


def create_output_directory(output_dir="output"):
    """Create the output folder if it does not exist."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


class DownloaderThread(QThread):
    """Worker thread for downloading files to prevent UI freezing."""

    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(str)

    def __init__(self, links_file):
        super().__init__()
        self.links_file = links_file

    def run(self):
        """The actual download logic that runs in the thread."""
        try:
            create_output_directory()
            self._download_youtube_to_mp3()
        except Exception as e:
            error_msg = f"An unexpected error occurred: {e}"
            self.finished_signal.emit(error_msg)

    def _download_youtube_to_mp3(self, output_dir="output"):
        """Download YouTube videos as MP3 from a text file."""
        # Use resource_path to find ffmpeg
        ffmpeg_path = resource_path("ffmpeg")

        if not os.path.exists(
            os.path.join(ffmpeg_path, "ffmpeg.exe")
        ) or not os.path.exists(os.path.join(ffmpeg_path, "ffprobe.exe")):
            self.finished_signal.emit(
                "FFmpeg not found. Please check the ffmpeg folder."
            )
            return

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
            "noplaylist": True,
            "ffmpeg_location": ffmpeg_path,
        }

        try:
            with open(self.links_file, "r", encoding="utf-8") as file:
                links = [line.strip() for line in file if line.strip()]
            if not links:
                self.finished_signal.emit("The selected file is empty.")
                return
        except Exception as e:
            self.finished_signal.emit(f"Error reading the file: {e}")
            return

        success_count = 0
        fail_count = 0
        total_links = len(links)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for i, link in enumerate(links):
                try:
                    self.progress_signal.emit(
                        f"Downloading link {i + 1} of {total_links}..."
                    )
                    ydl.download([link])
                    success_count += 1
                except Exception as e:
                    print(f"Error downloading {link}: {e}")
                    fail_count += 1

        result_msg = f"Finished. Success: {success_count}, Failed: {fail_count}"
        self.finished_signal.emit(result_msg)


# --- PyQt6 GUI ---


class DropLabel(QLabel):
    """A custom label that accepts file drops."""

    file_dropped = pyqtSignal(str)

    def __init__(self, text):
        super().__init__(text)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                padding: 20px;
                font-size: 16px;
                color: #888;
            }
        """)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            file_path = event.mimeData().urls()[0].toLocalFile()
            if file_path.endswith(".txt"):
                event.acceptProposedAction()
                self.setStyleSheet("border-color: #3A8DFF;")

    def dragLeaveEvent(self, event):
        self.setStyleSheet("border-color: #aaa;")

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.file_dropped.emit(file_path)
        self.setStyleSheet("border-color: #aaa;")


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube to MP3 Downloader")
        self.setGeometry(100, 100, 480, 250)

        # Set the window icon
        self.setWindowIcon(QIcon(resource_path("assets/logo.ico")))

        self.links_file = None
        self.downloader_thread = None

        # --- UI Elements ---
        self.drop_label = DropLabel("Drag & drop a .txt file here\nor")
        self.drop_label.file_dropped.connect(self.handle_file_path)

        self.choose_button = QPushButton("Choose a file...")
        self.choose_button.clicked.connect(self.open_file_dialog)

        self.status_label = QLabel("Select a file to start.")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.start_button = QPushButton("Start Download")
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self.start_download)

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.drop_label)
        layout.addWidget(self.choose_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Choose the file containing the links", "", "Text files (*.txt)"
        )
        if file_path:
            self.handle_file_path(file_path)

    def handle_file_path(self, file_path):
        self.links_file = file_path
        filename = os.path.basename(file_path)
        self.status_label.setText(f"File selected: {filename}")
        self.start_button.setEnabled(True)

    def start_download(self):
        if not self.links_file:
            QMessageBox.warning(self, "No file", "Please select a file first.")
            return

        self.start_button.setEnabled(False)
        self.choose_button.setEnabled(False)
        self.setAcceptDrops(False)  # Disable dropping during download

        self.downloader_thread = DownloaderThread(self.links_file)
        self.downloader_thread.progress_signal.connect(self.update_status)
        self.downloader_thread.finished_signal.connect(self.on_download_finished)
        self.downloader_thread.start()

    def update_status(self, message):
        self.status_label.setText(message)

    def on_download_finished(self, message):
        self.update_status(message)
        self.start_button.setEnabled(True)
        self.choose_button.setEnabled(True)
        self.setAcceptDrops(True)
        self.links_file = None


def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
