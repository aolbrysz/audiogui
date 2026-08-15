import sys
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import APIC
from mutagen.flac import FLAC, Picture
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QFormLayout, QVBoxLayout, QHBoxLayout, QSlider, QFileDialog, QLineEdit
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AudioGUI")
        self.resize(1366, 768)
        self.setMinimumSize(800, 600)
        self.setMaximumSize(1920, 1080)

        main_layout = QHBoxLayout()

        # Metadata editor: text
        self.editor_layout = QFormLayout()
        self.editor_layout.setSpacing(30)

        self.audio = None

        self.header = QLabel("<h1>Welcome to AudioGUI!</h1>")
        self.header.setFixedWidth(500)
        self.editor_layout.addRow(self.header)
        self.setup_title_length_layout()
        self.setup_artist_layout()
        self.setup_album_year_layout()
        self.setup_disc_layout()
        self.setup_track_layout()
        self.setup_file_buttons()

        self.thumbnail_layout = QVBoxLayout()
        self.thumbnail_layout.setSpacing(20)

        # Metadata editor: thumbnail
        self.thumbnail_label = QLabel()
        self.thumbnail_pixmap = QPixmap('clippy.jpeg')
        self.thumbnail_label.setFixedSize(300, 300)
        self.thumbnail_label.setScaledContents(True)
        self.thumbnail_label.setPixmap(self.thumbnail_pixmap)
        self.thumbnail_layout.addWidget(self.thumbnail_label)

        thumbnail_button_layout = QHBoxLayout()
        self.thumbnail_choose_button = QPushButton("Choose new")
        self.thumbnail_choose_button.clicked.connect(self.choose_thumbnail)
        thumbnail_button_layout.addWidget(self.thumbnail_choose_button)
        self.thumbnail_previous_button = QPushButton("Previous thumbnail")
        self.thumbnail_previous_button.clicked.connect(self.previous_thumbnail)
        thumbnail_button_layout.addWidget(self.thumbnail_previous_button)
        self.thumbnail_update_button = QPushButton("Update")
        # TODO connect
        thumbnail_button_layout.addWidget(self.thumbnail_update_button)
        self.thumbnail_layout.addLayout(thumbnail_button_layout)

        # Window
        main_layout.addLayout(self.editor_layout)
        main_layout.addLayout(self.thumbnail_layout)

        window = QWidget()
        window.setLayout(main_layout)
        self.setCentralWidget(window)

    def setup_title_length_layout(self):
        title_length_layout = QHBoxLayout()
        title_length_layout.setSpacing(20)

        self.title_length = QLabel("Title: ")
        self.title_length.setStyleSheet("font-size: 18px;")
        self.title_length.setMinimumWidth(100)

        self.title_input = QLineEdit()
        self.title_input.setMinimumWidth(200)
        self.title_input.setMaximumWidth(600)
        self.title_input.setPlaceholderText("Edit title:")
        title_length_layout.addWidget(self.title_input)

        self.title_button = QPushButton("Update")
        self.title_button.clicked.connect(self.change_title)
        self.title_button.setMinimumWidth(50)
        self.title_button.setMaximumWidth(80)
        title_length_layout.addWidget(self.title_button)

        self.editor_layout.addRow(self.title_length, title_length_layout)

    def setup_artist_layout(self):
        artist_layout = QHBoxLayout()
        artist_layout.setSpacing(20)

        self.artist = QLabel("Artist: ")
        self.artist.setStyleSheet("font-size: 18px;")
        self.artist.setMinimumWidth(100)

        self.artist_input = QLineEdit()
        self.artist_input.setMinimumWidth(200)
        self.artist_input.setMaximumWidth(600)
        self.artist_input.setPlaceholderText("Edit artist:")
        artist_layout.addWidget(self.artist_input)

        self.artist_button = QPushButton("Update")
        self.artist_button.clicked.connect(self.change_artist)
        self.artist_button.setMinimumWidth(50)
        self.artist_button.setMaximumWidth(80)
        artist_layout.addWidget(self.artist_button)

        self.editor_layout.addRow(self.artist, artist_layout)

    def setup_album_year_layout(self):
        album_year_layout = QHBoxLayout()
        album_year_layout.setSpacing(10)

        self.album_year = QLabel("Album: ")
        self.album_year.setStyleSheet("font-size: 18px;")
        self.album_year.setMinimumWidth(100)

        self.album_input = QLineEdit()
        self.album_input.setMinimumWidth(200)
        self.album_input.setMaximumWidth(400)
        self.album_input.setPlaceholderText("Edit album:")
        album_year_layout.addWidget(self.album_input)

        self.album_button = QPushButton("Update")
        self.album_button.clicked.connect(self.change_album)
        self.album_button.setMinimumWidth(50)
        self.album_button.setMaximumWidth(80)
        album_year_layout.addWidget(self.album_button)

        self.year_input = QLineEdit()
        self.year_input.setMinimumWidth(50)
        self.year_input.setMaximumWidth(100)
        self.year_input.setPlaceholderText("Edit year:")
        album_year_layout.addWidget(self.year_input)

        self.year_button = QPushButton("Update")
        self.year_button.clicked.connect(self.change_year)
        self.year_button.setMinimumWidth(50)
        self.year_button.setMaximumWidth(80)
        album_year_layout.addWidget(self.year_button)

        self.editor_layout.addRow(self.album_year, album_year_layout)

    def setup_disc_layout(self):
        disc_layout = QHBoxLayout()
        disc_layout.setSpacing(20)
        disc_layout.setContentsMargins(0, 0, 0, 0)

        self.disc = QLabel("Disc ")
        self.disc.setStyleSheet("font-size: 18px;")
        self.disc.setMinimumWidth(100)

        self.disc_number_input = QLineEdit()
        self.disc_number_input.setMinimumWidth(100)
        self.disc_number_input.setMaximumWidth(200)
        self.disc_number_input.setPlaceholderText("Edit disc number:")
        disc_layout.addWidget(self.disc_number_input)

        self.disc_number_button = QPushButton("Update")
        self.disc_number_button.clicked.connect(self.change_disc_number)
        self.disc_number_button.setMinimumWidth(50)
        self.disc_number_button.setMaximumWidth(80)
        disc_layout.addWidget(self.disc_number_button)

        self.disc_total_input = QLineEdit()
        self.disc_total_input.setMinimumWidth(100)
        self.disc_total_input.setMaximumWidth(200)
        self.disc_total_input.setPlaceholderText("Edit disc total:")
        disc_layout.addWidget(self.disc_total_input)

        self.disc_total_button = QPushButton("Update")
        self.disc_total_button.clicked.connect(self.change_disc_total)
        self.disc_total_button.setMinimumWidth(50)
        self.disc_total_button.setMaximumWidth(80)
        disc_layout.addWidget(self.disc_total_button)

        self.editor_layout.addRow(self.disc, disc_layout)

    def setup_track_layout(self):
        track_layout = QHBoxLayout()
        track_layout.setSpacing(20)
        track_layout.setContentsMargins(0, 0, 0, 0)

        self.track = QLabel("Track ")
        self.track.setMinimumWidth(100)
        self.track.setStyleSheet("font-size: 18px;")

        self.track_number_input = QLineEdit()
        self.track_number_input.setMinimumWidth(100)
        self.track_number_input.setMaximumWidth(200)
        self.track_number_input.setPlaceholderText("Edit track number:")
        track_layout.addWidget(self.track_number_input)

        self.track_number_button = QPushButton("Update")
        self.track_number_button.clicked.connect(self.change_track_number)
        self.track_number_button.setMinimumWidth(50)
        self.track_number_button.setMaximumWidth(80)
        track_layout.addWidget(self.track_number_button)

        self.track_total_input = QLineEdit()
        self.track_total_input.setMinimumWidth(100)
        self.track_total_input.setMaximumWidth(200)
        self.track_total_input.setPlaceholderText("Edit track total:")
        track_layout.addWidget(self.track_total_input)

        self.track_total_button = QPushButton("Update")
        self.track_total_button.clicked.connect(self.change_track_total)
        self.track_total_button.setMinimumWidth(50)
        self.track_total_button.setMaximumWidth(80)
        track_layout.addWidget(self.track_total_button)

        self.editor_layout.addRow(self.track, track_layout)

    def setup_file_buttons(self):
        self.current_file = QLabel("Choose a file to proceed.")
        self.current_file.setStyleSheet("font-size: 18px;")
        self.current_file.setMaximumWidth(700)
        self.editor_layout.addRow(self.current_file)

        self.choose_button = QPushButton("Choose file")
        self.choose_button.clicked.connect(self.choose_audio_file)
        self.choose_button.setMaximumWidth(700)
        self.editor_layout.addRow("Choose audio file:", self.choose_button)

    def choose_audio_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "Choose audio file:",
            "",
            "Audio Files (*.flac *.mp3 *.ogg *.m4a *.wav);;All Files (*)"
        )

        if file_path:
            self.current_file.setText(f"File: {file_path}")

            # Get file metadata
            self.audio = mutagen.File(file_path, easy = True)
            self.audio_title = self.audio.get("title", ["Unknown Title"])
            self.minutes, self.seconds = divmod(self.audio.info.length, 60)
            self.audio_artist = self.audio.get("artist", ["Unknown Artist"])
            self.audio_album = self.audio.get("album", ["Unknown Album"])
            self.audio_year = self.audio.get("date", ["Unknown Year"])
            self.audio_track_number = self.audio.get("tracknumber", ["Unknown"])
            self.audio_track_total = self.audio.get("tracktotal", ["Unknown"])
            self.audio_disc_number = self.audio.get("discnumber", ["Unknown"])
            self.audio_disc_total = self.audio.get("disctotal", ["Unknown"])

            # Update labels
            if self.minutes < 10:
                self.title_length.setText(f"Title: {self.audio_title[0]} (0{int(self.minutes)}:{round(self.seconds, 2)})")
            else:
                self.title_length.setText(f"Title: {self.audio_title[0]} ({int(self.minutes)}:{round(self.seconds, 2)})")

            self.artist.setText(f"Artist: {self.audio_artist[0]}")

            if self.audio_year[0] == "Unknown Year":
                self.album_year.setText(f"Album: {self.audio_album[0]} ({self.audio_year[0]})")
            else:
                self.album_year.setText(f"Album: {self.audio_album[0]} ({self.audio_year[0][:4]})")

            if self.audio_disc_number == "Unknown" or self.audio_disc_total == "Unknown":
                pass
            else:
                disc_info = f"Disc {self.audio_disc_number[0]} / {self.audio_disc_total[0]}"
                self.disc.setText(disc_info)

            if self.audio_track_number == "Unknown" or self.audio_track_total == "Unknown":
                pass
            else:
                track_info = f"Track {self.audio_track_number[0]} / {self.audio_track_total[0]}"
                self.track.setText(track_info)

    def choose_thumbnail(self):
        thumbnail_path, _ = QFileDialog.getOpenFileName(
            None,
            "Choose thumbnail",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
            )
        if thumbnail_path and self.current_file.text() != "Choose a file to proceed.":
            temp_pixmap = QPixmap(thumbnail_path)
            self.thumbnail_label.setPixmap(temp_pixmap)

    def previous_thumbnail(self):
        if self.current_file.text() != "Choose a file to proceed.":
            self.thumbnail_label.setPixmap(self.thumbnail_pixmap)

    def change_title(self):
        if (self.title_input.text() != "" and self.title_input.text() != "Edit title:" and self.audio is not None):
            self.audio["title"] = self.title_input.text()
            self.audio.save()

            self.audio_title = self.audio["title"]
            if self.minutes < 10:
                self.title_length.setText(f"Title: {self.audio_title[0]} (0{int(self.minutes)}:{round(self.seconds, 2)})")
            else:
                self.title_length.setText(f"Title: {self.audio_title[0]} ({int(self.minutes)}:{round(self.seconds, 2)})")

    def change_artist(self):
        if (self.artist_input.text() != "" and self.artist_input.text() != "Edit artist:" and self.audio is not None):
            self.audio["artist"] = self.artist_input.text()
            self.audio.save()

            self.audio_artist = self.audio["artist"]
            self.artist.setText(f"Artist: {self.audio_artist[0]}")

    def change_album(self):
        if (self.album_input.text() != "" and self.album_input.text() != "Edit album:" and self.audio is not None):
            self.audio["album"] = self.album_input.text()
            self.audio.save()

            self.audio_album = self.audio["album"]
            self.album_year.setText(f"Album: {self.audio_album[0]} ({self.audio_year[0]})")

    def change_year(self):
        if (self.year_input.text() != "" and self.year_input.text() != "Edit year:" and self.audio is not None):
            self.audio["date"] = self.year_input.text()
            self.audio.save()

            self.audio_year = self.audio["date"]
            self.album_year.setText(f"Album: {self.audio_album[0]} ({self.audio_year[0][:4]})")

    def change_disc_number(self):
        if (self.disc_number_input.text() != "" and self.disc_number_input.text() != "Edit disc number:" and self.audio is not None and self.audio_disc_total != "Unknown"):
            self.audio["discnumber"] = self.disc_number_input.text()
            self.audio.save()

            self.audio_disc_number = self.audio["discnumber"]
            self.disc.setText(f"Disc {self.audio_disc_number[0]} / {self.audio_disc_total[0]}")

    def change_disc_total(self):
        if (self.disc_total_input.text() != "" and self.disc_total_input.text() != "Edit disc total:" and self.audio is not None and self.audio_disc_number != "Unknown"):
            self.audio["disctotal"] = self.disc_total_input.text()
            self.audio.save()

            self.audio_disc_total = self.audio["disctotal"]
            self.disc.setText(f"Disc {self.audio_disc_number[0]} / {self.audio_disc_total[0]}")

    def change_track_number(self):
        if (self.track_number_input.text() != "" and self.track_number_input.text() != "Edit track number:" and self.audio is not None and self.audio_track_total != "Unknown"):
            self.audio["tracknumber"] = self.track_number_input.text()
            self.audio.save()

            self.audio_track_number = self.audio["tracknumber"]
            self.track.setText(f"Track {self.audio_track_number[0]} / {self.audio_track_total[0]}")

    def change_track_total(self):
        if (self.track_total_input.text != "" and self.track_total_input.text() != "Edit track total:" and self.audio is not None and self.audio_track_number != "Unknown"):
            self.audio["tracktotal"] = self.track_total_input.text()
            self.audio.save()

            self.audio_track_total = self.audio["tracktotal"]
            self.track.setText(f"Track {self.audio_track_number[0]} / {self.audio_track_total[0]}")

# Holds event loop
app = QApplication([])

window = MainWindow()
window.show()

# Starts event loop
app.exec()