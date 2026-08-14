# AudioGUI

**This project is in early development.** Core functionality is limited and the app may be unstable. Use at your own risk.

A minimalist desktop application built in Python (PyQt6) for reading and editing metadata tags of audio files.

## Features
- View and edit metadata tags (title, artist, album) of .flac and .wav files

## Roadmap
- Support for .mp3 and other formats (in progress)
- View and edit thumbnails / album covers (in progress)
- Implement built-in file system explorer
- Replace placeholder image
- Increase aesthetic value of app

## Tech Stack
- Python 3
- PyQt6 (for GUI)
- mutagen (for audio file processing)

# Running AudioGUI

1. Clone the repository:

```bash
git clone https://github.com/aolbrysz/audiogui.git
```

2. Create and activate a virtual environment (venv):

```bash
# Linux / MacOS: 

python3 -m venv .venv
source .venv/bin/activate
```

```powershell
# Windows (PowerShell):

python -m venv .venv
.\.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python main.py
```