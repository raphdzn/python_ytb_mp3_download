import os
import sys
import yt_dlp
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QLabel, QFileDialog, QMessageBox
)

# --- App Stylesheet ---

STYLESHEET = """
QWidget {
    background-color: #1e2a3b;
    color: #e0e0e0;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}

QMainWindow {
    background-color: #1e2a3b;
}

QLabel {
    background-color: transparent;
}

QPushButton {
    background-color: #3a8dff;
    color: #ffffff;
    border: none;
    padding: 10px 15px;
    border-radius: 8px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #50a1ff;
}

QPushButton:pressed {
    background-color: #2a7de0;
}

QPushButton:disabled {
    background-color: #40506b;
    color: #a0a0a0;
}

/* Custom styling for the DropLabel */
#DropLabel {
    border: 2px dashed #40506b;
    border-radius: 12px;
    padding: 20px;
    font-size: 16px;
    color: #a0a0a0;
}

/* Style for when a file is being dragged over the DropLabel */
#DropLabel[draggedOver="true"] {
    border-color: #3a8dff;
    background-color: #2a3b50;
}
"""

# --- Helper for PyInstaller ---

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Business Logic ---

def create_output_directory(output_dir="output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

class DownloaderThread(QThread):
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(str)

    def __init__(self, links_file):
        super().__init__()
        self.links_file = links_file

    def run(self):
        try:
            create_output_directory()
            self._download_youtube_to_mp3()
        except Exception as e:
            self.finished_signal.emit(f"An unexpected error occurred: {e}")

    def _download_youtube_to_mp3(self, output_dir="output"):
        ffmpeg_path = resource_path("ffmpeg")
        if not os.path.exists(os.path.join(ffmpeg_path, "ffmpeg.exe")) or \
           not os.path.exists(os.path.join(ffmpeg_path, "ffprobe.exe")):
            self.finished_signal.emit("FFmpeg not found. Please check the ffmpeg folder.")
            return

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'}],
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'ffmpeg_location': ffmpeg_path,
        }

        try:
            with open(self.links_file, 'r', encoding='utf-8') as file:
                links = [line.strip() for line in file if line.strip()]
            if not links:
                self.finished_signal.emit("The selected file is empty.")
                return
        except Exception as e:
            self.finished_signal.emit(f"Error reading the file: {e}")
            return

        success_count, fail_count, total_links = 0, 0, len(links)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for i, link in enumerate(links):
                try:
                    self.progress_signal.emit(f"Downloading link {i + 1} of {total_links}...")
                    ydl.download([link])
                    success_count += 1
                except Exception as e:
                    print(f"Error downloading {link}: {e}")
                    fail_count += 1
        self.finished_signal.emit(f"Finished. Success: {success_count}, Failed: {fail_count}")

# --- PyQt6 GUI ---

class DropLabel(QLabel):
    file_dropped = pyqtSignal(str)

    def __init__(self, text):
        super().__init__(text)
        self.setObjectName("DropLabel")
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setProperty("draggedOver", False)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            file_path = event.mimeData().urls()[0].toLocalFile()
            if file_path.endswith('.txt'):
                event.acceptProposedAction()
                self.setProperty("draggedOver", True)
                self.style().polish(self)

    def dragLeaveEvent(self, event):
        self.setProperty("draggedOver", False)
        self.style().polish(self)

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.setProperty("draggedOver", False)
        self.style().polish(self)
        self.file_dropped.emit(file_path)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TubeStealer")
        self.setGeometry(100, 100, 480, 280)
        self.setWindowIcon(QIcon(resource_path('assets/logo.ico')))

        self.links_file = None
        self.downloader_thread = None

        self.drop_label = DropLabel("Drag & drop a .txt file here\nor")
        self.drop_label.file_dropped.connect(self.handle_file_path)

        self.choose_button = QPushButton("Choose a file...")
        self.choose_button.clicked.connect(self.open_file_dialog)
        
        self.status_label = QLabel("Select a file to start.")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.start_button = QPushButton("Start Download")
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self.start_download)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        layout.addWidget(self.drop_label)
        layout.addWidget(self.choose_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose file", "", "Text files (*.txt)")
        if file_path:
            self.handle_file_path(file_path)

    def handle_file_path(self, file_path):
        self.links_file = file_path
        self.status_label.setText(f"File: {os.path.basename(file_path)}")
        self.start_button.setEnabled(True)

    def start_download(self):
        if not self.links_file:
            QMessageBox.warning(self, "No File", "Please select a file first.")
            return

        self.start_button.setEnabled(False)
        self.choose_button.setEnabled(False)
        self.drop_label.setAcceptDrops(False)

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
        self.drop_label.setAcceptDrops(True)
        self.links_file = None

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    window = App()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
