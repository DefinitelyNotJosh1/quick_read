# QuickRead - Speed Reading Application

A cross-platform desktop application for speed reading using the **Rapid Serial Visual Presentation (RSVP)** technique. QuickRead displays text one word (or phrase) at a time with the Optimal Recognition Point (ORP) highlighted, enabling faster reading without eye movement.

## Features

- **RSVP Speed Reading**: Display words rapidly at the center of the screen
- **ORP Highlighting**: The optimal recognition point of each word is highlighted in red
- **Adjustable Speed**: 100-1000 WPM (words per minute)
- **Multi-word Display**: Show 1-5 words per flash
- **File Support**: Load text from `.txt` or `.pdf` files
- **Punctuation Pauses**: Automatic pauses at commas, periods, etc.
- **Progress Tracking**: Progress bar and time remaining estimate
- **Fullscreen Mode**: Immersive reading experience
- **Keyboard Shortcuts**: Space (play/pause), Left Arrow (rewind), F11 (fullscreen), Escape (exit)
- **Modern UI**: Clean, minimalistic design with the Fusion theme

## Installation

An executable of an older version is available in the /dist directory. Not recommended, as it is not as feature-rich.

If it doesn't happen to be working you can run it like any other python program

### Prerequisites

- Python 3.8 or higher

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install PyQt6 PyMuPDF
```

### Run the Application

```bash
python quickread.py
```

## Usage

1. **Input Text**: Either paste text directly into the text area or click "Load File" to open a `.txt` or `.pdf` file
2. **Configure Settings**:
   - **WPM**: Adjust reading speed (100-1000 words per minute)
   - **Words per Flash**: Choose how many words to display at once (1-5)
   - **Font Size**: Adjust display font size (24-96pt)
3. **Start Reading**: Click "Start Reading" to begin
4. **Controls**:
   - **Play/Pause**: Toggle reading (or press Space)
   - **Rewind**: Go back 10 words (or press Left Arrow)
   - **Stop**: Reset to beginning
   - **Fullscreen**: Toggle fullscreen mode (or press F11)

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Space | Play/Pause |
| Left Arrow | Rewind |
| F11 | Toggle Fullscreen |
| Escape | Exit Fullscreen / Stop |

## Building Standalone Executables

Use PyInstaller to create standalone executables for distribution.

### Install PyInstaller

```bash
pip install pyinstaller
```

### Windows

```bash
pyinstaller --onefile --windowed --name QuickRead quickread.py
```

The executable will be in the `dist/` folder: `QuickRead.exe`

### macOS

```bash
pyinstaller --onefile --windowed --name QuickRead quickread.py
```

The app bundle will be in the `dist/` folder: `QuickRead.app`

For a proper macOS app with icon:

```bash
pyinstaller --onefile --windowed --name QuickRead --osx-bundle-identifier com.quickread.app quickread.py
```

### Linux

```bash
pyinstaller --onefile --windowed --name QuickRead quickread.py
```

The executable will be in the `dist/` folder: `QuickRead`

### Additional PyInstaller Options

- `--icon=icon.ico` (Windows) or `--icon=icon.icns` (macOS): Add a custom icon
- `--add-data "data:data"`: Include additional data files
- `--clean`: Clean cache before building

## How RSVP Works

Rapid Serial Visual Presentation displays text one segment at a time at a fixed point, eliminating the need for eye movement (saccades) that typically slows down reading. By highlighting the Optimal Recognition Point (ORP) - the character your eye naturally focuses on first - the app helps you process words faster.

### ORP Calculation

The ORP is calculated based on word length:
- 1-2 letters: First letter
- 3-6 letters: Second letter
- 7+ letters: Approximately 1/3 into the word

## Technical Details

- **Language**: Python 3
- **GUI Framework**: PyQt6
- **PDF Parsing**: PyMuPDF (fitz)
- **Styling**: Qt Fusion theme with custom stylesheet
- **Cross-platform**: Windows, macOS, Linux

## Troubleshooting

### PDF Loading Issues

Make sure PyMuPDF is installed:

```bash
pip install PyMuPDF
```

### Font Issues

The app attempts to use Consolas or Courier New. If these aren't available, it falls back to the system monospace font.

### High DPI Displays

PyQt6 handles high DPI displays automatically. If text appears too small/large, adjust the Font Size setting.

## License

MIT License - Feel free to use, modify, and distribute.
