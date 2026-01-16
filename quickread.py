#!/usr/bin/env python3
"""
QuickRead - Speed Reading Application using RSVP Technique
A cross-platform desktop application for speed reading using Rapid Serial Visual Presentation.
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple, Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QSlider, QSpinBox, QComboBox,
    QFileDialog, QProgressBar, QStackedWidget, QFrame, QMessageBox,
    QSizePolicy, QSpacerItem, QGraphicsDropShadowEffect, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import QFont, QFontDatabase, QKeySequence, QShortcut, QAction, QColor, QFontMetrics


# =============================================================================
# Constants
# =============================================================================

DEFAULT_WPM = 300
MIN_WPM = 100
MAX_WPM = 1000
WPM_STEP = 25
DEFAULT_WORDS_PER_FLASH = 1
MAX_WORDS_PER_FLASH = 5
DEFAULT_FONT_SIZE = 48
MIN_FONT_SIZE = 24
MAX_FONT_SIZE = 96
REWIND_WORDS = 10
FORWARD_WORDS = 10
COMMA_DELAY_MULTIPLIER = 1.5
PERIOD_DELAY_MULTIPLIER = 2.0
MULTI_WORD_DELAY_MULTIPLIER = 1.2


# =============================================================================
# Stylesheet
# =============================================================================

STYLESHEET = """
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
}

QWidget {
    font-family: 'Segoe UI', 'SF Pro Display', 'Ubuntu', sans-serif;
    font-size: 14px;
    color: #e8e8e8;
}

QLabel {
    color: #e8e8e8;
}

QLabel#titleLabel {
    font-size: 36px;
    font-weight: bold;
    color: #00d9ff;
    padding: 10px;
}

QLabel#subtitleLabel {
    font-size: 14px;
    color: #a0a0a0;
    padding-bottom: 20px;
}

QLabel#sectionTitle {
    font-size: 18px;
    font-weight: bold;
    color: #00d9ff;
    padding: 5px 0;
    border-bottom: 2px solid #00d9ff;
    margin-bottom: 10px;
}

QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #4a4a6a, stop:1 #3a3a5a);
    color: white;
    border: 1px solid #5a5a7a;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: bold;
    min-width: 100px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #5a5a7a, stop:1 #4a4a6a);
    border: 1px solid #00d9ff;
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #3a3a5a, stop:1 #2a2a4a);
}

QPushButton:disabled {
    background: #2a2a3a;
    color: #666;
    border: 1px solid #3a3a4a;
}

QPushButton#startButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #00d9ff, stop:1 #0099cc);
    color: #1a1a2e;
    border: none;
    font-size: 16px;
    padding: 15px 40px;
}

QPushButton#startButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #33e0ff, stop:1 #00b8e6);
}

QPushButton#playButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #00e676, stop:1 #00c853);
    color: #1a1a2e;
    border: none;
    font-size: 16px;
    min-width: 140px;
}

QPushButton#playButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #33eb91, stop:1 #00e676);
}

QPushButton#pauseButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #ffa726, stop:1 #fb8c00);
    color: #1a1a2e;
    border: none;
    font-size: 16px;
    min-width: 140px;
}

QPushButton#pauseButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #ffb74d, stop:1 #ffa726);
}

QPushButton#stopButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #ff5252, stop:1 #d32f2f);
    color: white;
    border: none;
}

QPushButton#stopButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #ff6b6b, stop:1 #ff5252);
}

QPushButton#fileButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #ab47bc, stop:1 #8e24aa);
    color: white;
    border: none;
}

QPushButton#fileButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #ba68c8, stop:1 #ab47bc);
}

QTextEdit {
    background-color: #1e1e30;
    border: 2px solid #3a3a5a;
    border-radius: 10px;
    padding: 15px;
    font-size: 14px;
    line-height: 1.6;
    color: #e8e8e8;
    selection-background-color: #00d9ff;
    selection-color: #1a1a2e;
}

QTextEdit:focus {
    border-color: #00d9ff;
}

QSlider::groove:horizontal {
    border: none;
    height: 8px;
    background: #2a2a4a;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #00d9ff, stop:1 #0099cc);
    border: none;
    width: 22px;
    height: 22px;
    margin: -7px 0;
    border-radius: 11px;
}

QSlider::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #33e0ff, stop:1 #00d9ff);
}

QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #00d9ff, stop:1 #0099cc);
    border-radius: 4px;
}

QSpinBox, QComboBox {
    background-color: #1e1e30;
    border: 2px solid #3a3a5a;
    border-radius: 8px;
    padding: 8px 15px;
    min-width: 90px;
    color: #e8e8e8;
}

QSpinBox:focus, QComboBox:focus {
    border-color: #00d9ff;
}

QSpinBox::up-button, QSpinBox::down-button {
    background: #3a3a5a;
    border: none;
    width: 20px;
}

QSpinBox::up-button:hover, QSpinBox::down-button:hover {
    background: #4a4a6a;
}

QComboBox::drop-down {
    border: none;
    width: 35px;
    background: #3a3a5a;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
}

QComboBox QAbstractItemView {
    background-color: #1e1e30;
    border: 2px solid #3a3a5a;
    selection-background-color: #00d9ff;
    selection-color: #1a1a2e;
}

QProgressBar {
    border: none;
    border-radius: 6px;
    background-color: #2a2a4a;
    height: 12px;
    text-align: center;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #00d9ff, stop:0.5 #00e676, stop:1 #00d9ff);
    border-radius: 6px;
}

QFrame#displayFrame {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #1e1e35, stop:1 #12122a);
    border: 2px solid #3a3a5a;
    border-radius: 16px;
}

QFrame#inputFrame {
    background: rgba(30, 30, 48, 0.8);
    border: 1px solid #3a3a5a;
    border-radius: 12px;
    padding: 20px;
}

QFrame#settingsFrame {
    background: rgba(30, 30, 48, 0.8);
    border: 1px solid #3a3a5a;
    border-radius: 12px;
    padding: 20px;
}

QLabel#wordDisplay {
    color: #ffffff;
    background-color: transparent;
}

QLabel#statusLabel {
    font-size: 13px;
    color: #a0a0a0;
}

QLabel#timeLabel {
    font-size: 15px;
    color: #00d9ff;
    font-weight: bold;
}

QLabel#wpmDisplayLabel {
    font-size: 24px;
    color: #00d9ff;
    font-weight: bold;
}

QLabel#guideLine {
    color: #ff4757;
    font-size: 40px;
    font-weight: bold;
}

QFrame#orpContainer {
    background: transparent;
}
"""


# =============================================================================
# Text Processing Functions
# =============================================================================

def extract_text_from_pdf(filepath: str) -> str:
    """Extract text content from a PDF file using PyMuPDF."""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except ImportError:
        raise ImportError("PyMuPDF is required for PDF support. Install with: pip install pymupdf")
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")


def extract_text_from_txt(filepath: str) -> str:
    """Extract text content from a plain text file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with different encoding
        with open(filepath, 'r', encoding='latin-1') as f:
            return f.read()


def tokenize_text(text: str) -> List[dict]:
    """
    Split text into words with metadata about punctuation.
    Returns list of dicts with 'word' and 'delay_multiplier' keys.
    """
    # Normalize whitespace and clean text
    text = re.sub(r'\s+', ' ', text.strip())
    
    if not text:
        return []
    
    # Split into words
    raw_words = text.split()
    tokens = []
    
    for word in raw_words:
        if not word:
            continue
        
        # Determine delay multiplier based on trailing punctuation
        delay_multiplier = 1.0
        
        # Check for sentence-ending punctuation
        if re.search(r'[.!?]$', word):
            delay_multiplier = PERIOD_DELAY_MULTIPLIER
        elif re.search(r'[,;:]$', word):
            delay_multiplier = COMMA_DELAY_MULTIPLIER
        
        # Clean the word for display (keep internal punctuation like hyphens)
        clean_word = word.strip()
        
        if clean_word:
            tokens.append({
                'word': clean_word,
                'delay_multiplier': delay_multiplier
            })
    
    return tokens


def calculate_orp_index(word: str) -> int:
    """
    Calculate the Optimal Recognition Point (ORP) index for a word.
    This is the character that should be highlighted and centered.
    
    Rules based on word length (letters only):
    - 1 letter: index 0
    - 2-5 letters: index 1 (second letter)
    - 6-9 letters: index 2 (third letter)  
    - 10-13 letters: index 3 (fourth letter)
    - 14+ letters: approximately 1/4 into the word
    """
    # Get the actual letters (excluding punctuation for calculation)
    letters_only = re.sub(r'[^\w]', '', word)
    length = len(letters_only)
    
    if length <= 1:
        return 0
    elif length <= 5:
        return 1
    elif length <= 9:
        return 2
    elif length <= 13:
        return 3
    else:
        return length // 4


def find_orp_in_word(word: str) -> int:
    """
    Find the actual index of ORP in the word string (including punctuation).
    """
    # Get ORP index based on letters only
    letters_only = re.sub(r'[^\w]', '', word)
    orp_letter_index = calculate_orp_index(word)
    
    # Map back to actual string index
    letter_count = 0
    for i, char in enumerate(word):
        if re.match(r'\w', char):
            if letter_count == orp_letter_index:
                return i
            letter_count += 1
    
    return 0  # Fallback


def get_monospace_font() -> QFont:
    """Get a suitable monospace font for the display."""
    preferred_fonts = ['Consolas', 'Courier New', 'Monaco', 'Liberation Mono', 'DejaVu Sans Mono', 'Fira Code']
    
    available = QFontDatabase.families()
    
    for font_name in preferred_fonts:
        if font_name in available:
            return QFont(font_name)
    
    # Fallback to system monospace
    font = QFont()
    font.setStyleHint(QFont.StyleHint.Monospace)
    return font


# =============================================================================
# Custom ORP Display Widget
# =============================================================================

class ORPDisplayWidget(QWidget):
    """
    Custom widget that displays words with the ORP character perfectly centered.
    Uses three labels: left part, ORP character, right part.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.font_size = DEFAULT_FONT_SIZE
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the three-part display."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Top guide line
        self.top_guide = QLabel("▼")
        self.top_guide.setObjectName("guideLine")
        self.top_guide.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.top_guide.setStyleSheet("color: #ff4757; font-size: 28px; font-weight: bold;")
        layout.addWidget(self.top_guide)
        
        # Word display container
        word_container = QWidget()
        word_layout = QHBoxLayout(word_container)
        word_layout.setContentsMargins(0, 5, 0, 5)
        word_layout.setSpacing(0)
        
        # Left part (before ORP) - right aligned
        self.left_label = QLabel("")
        self.left_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        word_layout.addWidget(self.left_label, 1)
        
        # ORP character - centered, highlighted
        self.orp_label = QLabel("")
        self.orp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.orp_label.setStyleSheet("color: #ff4757; font-weight: bold;")
        word_layout.addWidget(self.orp_label, 0)
        
        # Right part (after ORP) - left aligned
        self.right_label = QLabel("")
        self.right_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        word_layout.addWidget(self.right_label, 1)
        
        layout.addWidget(word_container)
        
        # Bottom guide line
        self.bottom_guide = QLabel("▲")
        self.bottom_guide.setObjectName("guideLine")
        self.bottom_guide.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bottom_guide.setStyleSheet("color: #ff4757; font-size: 28px; font-weight: bold;")
        layout.addWidget(self.bottom_guide)
        
        self.update_font()
    
    def update_font(self):
        """Update fonts for all labels."""
        font = get_monospace_font()
        font.setPointSize(self.font_size)
        font.setBold(True)
        
        self.left_label.setFont(font)
        self.orp_label.setFont(font)
        self.right_label.setFont(font)
        
        # Style
        base_style = f"color: #ffffff; font-size: {self.font_size}pt;"
        self.left_label.setStyleSheet(base_style)
        self.right_label.setStyleSheet(base_style)
        self.orp_label.setStyleSheet(f"color: #ff4757; font-size: {self.font_size}pt; font-weight: bold;")
    
    def set_font_size(self, size: int):
        """Set the font size."""
        self.font_size = size
        self.update_font()
    
    def display_word(self, word: str):
        """Display a single word with ORP highlighting."""
        if not word:
            self.clear()
            return
        
        orp_index = find_orp_in_word(word)
        
        left_part = word[:orp_index] if orp_index > 0 else ""
        orp_char = word[orp_index] if orp_index < len(word) else ""
        right_part = word[orp_index + 1:] if orp_index + 1 < len(word) else ""
        
        self.left_label.setText(left_part)
        self.orp_label.setText(orp_char)
        self.right_label.setText(right_part)
    
    def display_phrase(self, words: List[str]):
        """Display multiple words as a phrase."""
        if not words:
            self.clear()
            return
        
        if len(words) == 1:
            self.display_word(words[0])
            return
        
        # For multiple words, find the middle word and center on its ORP
        middle_idx = len(words) // 2
        middle_word = words[middle_idx]
        orp_index = find_orp_in_word(middle_word)
        
        # Build left side: all words before middle + left part of middle word
        left_words = words[:middle_idx]
        left_part_middle = middle_word[:orp_index] if orp_index > 0 else ""
        left_text = " ".join(left_words)
        if left_text and left_part_middle:
            left_text += " " + left_part_middle
        elif left_part_middle:
            left_text = left_part_middle
        
        # ORP character
        orp_char = middle_word[orp_index] if orp_index < len(middle_word) else ""
        
        # Build right side: right part of middle word + all words after middle
        right_part_middle = middle_word[orp_index + 1:] if orp_index + 1 < len(middle_word) else ""
        right_words = words[middle_idx + 1:]
        right_text = right_part_middle
        if right_text and right_words:
            right_text += " " + " ".join(right_words)
        elif right_words:
            right_text = " ".join(right_words)
        
        self.left_label.setText(left_text)
        self.orp_label.setText(orp_char)
        self.right_label.setText(right_text)
    
    def display_message(self, message: str):
        """Display a centered message (like 'Done!')."""
        self.left_label.setText("")
        self.orp_label.setText(message)
        self.right_label.setText("")
        # Temporarily change ORP color for messages
        self.orp_label.setStyleSheet(f"color: #00d9ff; font-size: {self.font_size}pt; font-weight: bold;")
    
    def clear(self):
        """Clear the display."""
        self.left_label.setText("")
        self.orp_label.setText("")
        self.right_label.setText("")
        # Reset ORP color
        self.orp_label.setStyleSheet(f"color: #ff4757; font-size: {self.font_size}pt; font-weight: bold;")


# =============================================================================
# Main Application Window
# =============================================================================

class QuickReadApp(QMainWindow):
    """Main application window for QuickRead speed reader."""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("QuickRead - Speed Reader")
        self.setMinimumSize(900, 650)
        self.resize(1100, 750)
        
        # Application state
        self.tokens: List[dict] = []
        self.current_index: int = 0
        self.is_playing: bool = False
        self.is_paused: bool = False
        self.wpm: int = DEFAULT_WPM
        self.words_per_flash: int = DEFAULT_WORDS_PER_FLASH
        self.font_size: int = DEFAULT_FONT_SIZE
        self.is_fullscreen: bool = False
        
        # Timer for word display
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_next_word)
        
        # Setup UI
        self.setup_ui()
        self.apply_styles()
        self.setup_shortcuts()
        
        # Show input view initially
        self.show_input_view()
    
    def setup_ui(self):
        """Setup the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)
        
        # Stacked widget to switch between input and reading views
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        # Create input view
        self.input_widget = self.create_input_view()
        self.stacked_widget.addWidget(self.input_widget)
        
        # Create reading view
        self.reading_widget = self.create_reading_view()
        self.stacked_widget.addWidget(self.reading_widget)
    
    def create_input_view(self) -> QWidget:
        """Create the input/setup view with side-by-side layout."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("⚡ QuickRead")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Speed Reading with RSVP Technology • Focus. Read. Accelerate.")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle)
        
        layout.addLayout(header_layout)
        
        # Main content: side by side layout
        content_layout = QHBoxLayout()
        content_layout.setSpacing(25)
        
        # LEFT SIDE - Text Input
        input_frame = QFrame()
        input_frame.setObjectName("inputFrame")
        input_layout = QVBoxLayout(input_frame)
        input_layout.setSpacing(15)
        
        input_title = QLabel("📄 Text Input")
        input_title.setObjectName("sectionTitle")
        input_layout.addWidget(input_title)
        
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText(
            "Paste your text here...\n\n"
            "Supports any text content including articles, books, documents, and more.\n\n"
            "Or use the 'Load File' button below to open a .txt or .pdf file."
        )
        self.text_input.setMinimumHeight(300)
        input_layout.addWidget(self.text_input)
        
        # File load button
        self.file_button = QPushButton("📁 Load File (.txt, .pdf)")
        self.file_button.setObjectName("fileButton")
        self.file_button.clicked.connect(self.load_file)
        input_layout.addWidget(self.file_button)
        
        # Word count label
        self.word_count_label = QLabel("Words: 0")
        self.word_count_label.setStyleSheet("color: #a0a0a0; font-size: 12px;")
        self.text_input.textChanged.connect(self.update_word_count)
        input_layout.addWidget(self.word_count_label)
        
        content_layout.addWidget(input_frame, 3)
        
        # RIGHT SIDE - Settings
        settings_frame = QFrame()
        settings_frame.setObjectName("settingsFrame")
        settings_layout = QVBoxLayout(settings_frame)
        settings_layout.setSpacing(20)
        
        settings_title = QLabel("⚙️ Settings")
        settings_title.setObjectName("sectionTitle")
        settings_layout.addWidget(settings_title)
        
        # WPM setting
        wpm_group = QVBoxLayout()
        wpm_header = QHBoxLayout()
        wpm_label = QLabel("Reading Speed")
        wpm_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        wpm_header.addWidget(wpm_label)
        wpm_header.addStretch()
        self.wpm_value_label = QLabel(f"{DEFAULT_WPM} WPM")
        self.wpm_value_label.setStyleSheet("color: #00d9ff; font-weight: bold; font-size: 14px;")
        wpm_header.addWidget(self.wpm_value_label)
        wpm_group.addLayout(wpm_header)
        
        self.wpm_slider = QSlider(Qt.Orientation.Horizontal)
        self.wpm_slider.setMinimum(MIN_WPM)
        self.wpm_slider.setMaximum(MAX_WPM)
        self.wpm_slider.setValue(DEFAULT_WPM)
        self.wpm_slider.setTickInterval(100)
        self.wpm_slider.valueChanged.connect(self.on_wpm_changed)
        wpm_group.addWidget(self.wpm_slider)
        
        wpm_range = QHBoxLayout()
        wpm_range.addWidget(QLabel(f"{MIN_WPM}"))
        wpm_range.addStretch()
        wpm_range.addWidget(QLabel(f"{MAX_WPM}"))
        wpm_group.addLayout(wpm_range)
        
        settings_layout.addLayout(wpm_group)
        
        # Words per flash setting
        wpf_group = QVBoxLayout()
        wpf_label = QLabel("Words per Flash")
        wpf_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        wpf_group.addWidget(wpf_label)
        
        wpf_layout = QHBoxLayout()
        self.wpf_combo = QComboBox()
        for i in range(1, MAX_WORDS_PER_FLASH + 1):
            self.wpf_combo.addItem(f"{i} word{'s' if i > 1 else ''}", i)
        self.wpf_combo.currentIndexChanged.connect(self.on_wpf_changed)
        wpf_layout.addWidget(self.wpf_combo)
        wpf_layout.addStretch()
        wpf_group.addLayout(wpf_layout)
        
        settings_layout.addLayout(wpf_group)
        
        # Font size setting
        font_group = QVBoxLayout()
        font_header = QHBoxLayout()
        font_label = QLabel("Display Font Size")
        font_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        font_header.addWidget(font_label)
        font_header.addStretch()
        self.font_value_label = QLabel(f"{DEFAULT_FONT_SIZE} pt")
        self.font_value_label.setStyleSheet("color: #00d9ff; font-weight: bold; font-size: 14px;")
        font_header.addWidget(self.font_value_label)
        font_group.addLayout(font_header)
        
        self.font_slider = QSlider(Qt.Orientation.Horizontal)
        self.font_slider.setMinimum(MIN_FONT_SIZE)
        self.font_slider.setMaximum(MAX_FONT_SIZE)
        self.font_slider.setValue(DEFAULT_FONT_SIZE)
        self.font_slider.valueChanged.connect(self.on_font_size_changed)
        font_group.addWidget(self.font_slider)
        
        settings_layout.addLayout(font_group)
        
        # Spacer
        settings_layout.addStretch()
        
        # Time estimate
        self.estimate_label = QLabel("Estimated time: --:--")
        self.estimate_label.setStyleSheet("color: #a0a0a0; font-size: 13px;")
        self.estimate_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_layout.addWidget(self.estimate_label)
        
        # Start button
        self.start_reading_button = QPushButton("▶ Start Reading")
        self.start_reading_button.setObjectName("startButton")
        self.start_reading_button.clicked.connect(self.start_reading)
        settings_layout.addWidget(self.start_reading_button)
        
        content_layout.addWidget(settings_frame, 2)
        
        layout.addLayout(content_layout)
        
        # Keyboard shortcuts hint
        shortcuts_label = QLabel("💡 Shortcuts: Space = Play/Pause • ← → = Navigate • ↑ ↓ = Speed • F11 = Fullscreen")
        shortcuts_label.setStyleSheet("color: #666; font-size: 11px;")
        shortcuts_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(shortcuts_label)
        
        return widget
    
    def create_reading_view(self) -> QWidget:
        """Create the reading/display view."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Top bar with back button and fullscreen toggle
        top_bar = QHBoxLayout()
        
        self.back_button = QPushButton("← Back")
        self.back_button.clicked.connect(self.show_input_view)
        top_bar.addWidget(self.back_button)
        
        top_bar.addStretch()
        
        # WPM display in reading mode
        self.wpm_display = QLabel(f"{self.wpm} WPM")
        self.wpm_display.setObjectName("wpmDisplayLabel")
        top_bar.addWidget(self.wpm_display)
        
        top_bar.addStretch()
        
        self.fullscreen_button = QPushButton("⛶ Fullscreen")
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        top_bar.addWidget(self.fullscreen_button)
        
        layout.addLayout(top_bar)
        
        # Main display area
        display_frame = QFrame()
        display_frame.setObjectName("displayFrame")
        display_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        display_layout = QVBoxLayout(display_frame)
        display_layout.setContentsMargins(50, 30, 50, 30)
        
        # Spacer above
        display_layout.addStretch(1)
        
        # ORP Display Widget (custom widget for perfect centering)
        self.orp_display = ORPDisplayWidget()
        self.orp_display.set_font_size(self.font_size)
        display_layout.addWidget(self.orp_display)
        
        # Spacer below
        display_layout.addStretch(1)
        
        layout.addWidget(display_frame, 1)
        
        # WPM slider in reading mode
        wpm_reading_layout = QHBoxLayout()
        wpm_reading_layout.setSpacing(15)
        
        slow_label = QLabel("🐢 Slower")
        slow_label.setStyleSheet("color: #a0a0a0; font-size: 12px;")
        wpm_reading_layout.addWidget(slow_label)
        
        self.reading_wpm_slider = QSlider(Qt.Orientation.Horizontal)
        self.reading_wpm_slider.setMinimum(MIN_WPM)
        self.reading_wpm_slider.setMaximum(MAX_WPM)
        self.reading_wpm_slider.setValue(self.wpm)
        self.reading_wpm_slider.valueChanged.connect(self.on_reading_wpm_changed)
        wpm_reading_layout.addWidget(self.reading_wpm_slider, 1)
        
        fast_label = QLabel("🐇 Faster")
        fast_label.setStyleSheet("color: #a0a0a0; font-size: 12px;")
        wpm_reading_layout.addWidget(fast_label)
        
        layout.addLayout(wpm_reading_layout)
        
        # Progress section
        progress_layout = QHBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        progress_layout.addWidget(self.progress_bar, 1)
        
        self.time_label = QLabel("Remaining: --:--")
        self.time_label.setObjectName("timeLabel")
        self.time_label.setMinimumWidth(150)
        progress_layout.addWidget(self.time_label)
        
        layout.addLayout(progress_layout)
        
        # Control buttons
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)
        
        controls_layout.addStretch()
        
        self.rewind_button = QPushButton("⏪ Rewind")
        self.rewind_button.clicked.connect(self.rewind)
        controls_layout.addWidget(self.rewind_button)
        
        self.play_pause_button = QPushButton("▶ Play")
        self.play_pause_button.setObjectName("playButton")
        self.play_pause_button.setMinimumWidth(140)
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        controls_layout.addWidget(self.play_pause_button)
        
        self.forward_button = QPushButton("Forward ⏩")
        self.forward_button.clicked.connect(self.forward)
        controls_layout.addWidget(self.forward_button)
        
        self.stop_button = QPushButton("⏹ Stop")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.clicked.connect(self.stop_reading)
        controls_layout.addWidget(self.stop_button)
        
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
        
        # Status label
        self.status_label = QLabel("Press Space or Play to start reading • ↑↓ adjust speed • ←→ navigate")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        return widget
    
    def apply_styles(self):
        """Apply the application stylesheet."""
        self.setStyleSheet(STYLESHEET)
        QApplication.setStyle("Fusion")
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts."""
        # Space to play/pause
        space_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Space), self)
        space_shortcut.activated.connect(self.toggle_play_pause)
        
        # Escape to exit fullscreen or stop
        escape_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        escape_shortcut.activated.connect(self.on_escape)
        
        # Left arrow to rewind
        left_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Left), self)
        left_shortcut.activated.connect(self.rewind)
        
        # Right arrow to forward
        right_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Right), self)
        right_shortcut.activated.connect(self.forward)
        
        # Up arrow to increase WPM
        up_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Up), self)
        up_shortcut.activated.connect(self.increase_wpm)
        
        # Down arrow to decrease WPM
        down_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Down), self)
        down_shortcut.activated.connect(self.decrease_wpm)
        
        # F11 for fullscreen
        f11_shortcut = QShortcut(QKeySequence(Qt.Key.Key_F11), self)
        f11_shortcut.activated.connect(self.toggle_fullscreen)
    
    def update_display_font(self):
        """Update the word display font."""
        self.orp_display.set_font_size(self.font_size)
    
    # =========================================================================
    # Event Handlers
    # =========================================================================
    
    def on_wpm_changed(self, value: int):
        """Handle WPM slider change in input view."""
        self.wpm = value
        self.wpm_value_label.setText(f"{value} WPM")
        self.reading_wpm_slider.blockSignals(True)
        self.reading_wpm_slider.setValue(value)
        self.reading_wpm_slider.blockSignals(False)
        self.update_wpm_display()
        self.update_estimate()
    
    def on_reading_wpm_changed(self, value: int):
        """Handle WPM slider change in reading view."""
        self.wpm = value
        self.wpm_slider.blockSignals(True)
        self.wpm_slider.setValue(value)
        self.wpm_slider.blockSignals(False)
        self.wpm_value_label.setText(f"{value} WPM")
        self.update_wpm_display()
        self.update_time_estimate()
    
    def increase_wpm(self):
        """Increase WPM by step amount."""
        new_wpm = min(self.wpm + WPM_STEP, MAX_WPM)
        self.wpm = new_wpm
        self.wpm_slider.setValue(new_wpm)
        self.reading_wpm_slider.setValue(new_wpm)
        self.update_wpm_display()
        self.status_label.setText(f"Speed: {new_wpm} WPM")
    
    def decrease_wpm(self):
        """Decrease WPM by step amount."""
        new_wpm = max(self.wpm - WPM_STEP, MIN_WPM)
        self.wpm = new_wpm
        self.wpm_slider.setValue(new_wpm)
        self.reading_wpm_slider.setValue(new_wpm)
        self.update_wpm_display()
        self.status_label.setText(f"Speed: {new_wpm} WPM")
    
    def update_wpm_display(self):
        """Update WPM display label."""
        self.wpm_display.setText(f"{self.wpm} WPM")
    
    def on_wpf_changed(self, index: int):
        """Handle words per flash change."""
        self.words_per_flash = self.wpf_combo.currentData()
        self.update_estimate()
    
    def on_font_size_changed(self, value: int):
        """Handle font size slider change."""
        self.font_size = value
        self.font_value_label.setText(f"{value} pt")
        self.update_display_font()
    
    def on_escape(self):
        """Handle escape key."""
        if self.is_fullscreen:
            self.toggle_fullscreen()
        elif self.is_playing:
            self.pause_reading()
    
    def update_word_count(self):
        """Update word count label."""
        text = self.text_input.toPlainText()
        words = len(text.split()) if text.strip() else 0
        self.word_count_label.setText(f"Words: {words:,}")
        self.update_estimate()
    
    def update_estimate(self):
        """Update estimated reading time in input view."""
        text = self.text_input.toPlainText()
        words = len(text.split()) if text.strip() else 0
        
        if words == 0:
            self.estimate_label.setText("Estimated time: --:--")
            return
        
        # Calculate time
        flashes = words / self.words_per_flash
        base_delay_ms = 60000 / self.wpm
        avg_delay = base_delay_ms * 1.2  # Account for punctuation pauses
        if self.words_per_flash > 1:
            avg_delay *= MULTI_WORD_DELAY_MULTIPLIER
        
        total_ms = flashes * avg_delay
        total_seconds = int(total_ms / 1000)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        
        self.estimate_label.setText(f"Estimated time: {minutes}:{seconds:02d}")
    
    # =========================================================================
    # File Operations
    # =========================================================================
    
    def load_file(self):
        """Open file dialog and load text from selected file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Text File",
            "",
            "Text Files (*.txt);;PDF Files (*.pdf);;All Files (*.*)"
        )
        
        if not file_path:
            return
        
        try:
            path = Path(file_path)
            
            if path.suffix.lower() == '.pdf':
                text = extract_text_from_pdf(file_path)
            else:
                text = extract_text_from_txt(file_path)
            
            self.text_input.setPlainText(text)
            
        except ImportError as e:
            QMessageBox.warning(
                self,
                "Missing Dependency",
                str(e)
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Loading File",
                f"Could not load file:\n{str(e)}"
            )
    
    # =========================================================================
    # View Navigation
    # =========================================================================
    
    def show_input_view(self):
        """Switch to the input view."""
        self.stop_reading()
        self.stacked_widget.setCurrentIndex(0)
        
        # Exit fullscreen if active
        if self.is_fullscreen:
            self.toggle_fullscreen()
    
    def show_reading_view(self):
        """Switch to the reading view."""
        self.stacked_widget.setCurrentIndex(1)
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        if self.is_fullscreen:
            self.showNormal()
            self.fullscreen_button.setText("⛶ Fullscreen")
            self.is_fullscreen = False
        else:
            self.showFullScreen()
            self.fullscreen_button.setText("⛶ Exit Fullscreen")
            self.is_fullscreen = True
    
    # =========================================================================
    # Reading Control
    # =========================================================================
    
    def start_reading(self):
        """Initialize and start reading session."""
        text = self.text_input.toPlainText().strip()
        
        if not text:
            QMessageBox.warning(
                self,
                "No Text",
                "Please enter or load some text to read."
            )
            return
        
        # Tokenize text
        self.tokens = tokenize_text(text)
        
        if not self.tokens:
            QMessageBox.warning(
                self,
                "No Words",
                "The text doesn't contain any readable words."
            )
            return
        
        # Reset state
        self.current_index = 0
        self.is_playing = False
        self.is_paused = False
        
        # Update UI
        self.progress_bar.setValue(0)
        self.orp_display.clear()
        self.reading_wpm_slider.setValue(self.wpm)
        self.update_wpm_display()
        self.update_time_estimate()
        self.update_play_button()
        
        # Switch to reading view
        self.show_reading_view()
        
        # Auto-start
        self.toggle_play_pause()
    
    def toggle_play_pause(self):
        """Toggle between play and pause states."""
        if not self.tokens:
            return
        
        if self.is_playing:
            self.pause_reading()
        else:
            self.resume_reading()
    
    def resume_reading(self):
        """Resume or start reading."""
        if self.current_index >= len(self.tokens):
            self.current_index = 0  # Restart if at end
        
        self.is_playing = True
        self.is_paused = False
        self.update_play_button()
        self.display_next_word()
    
    def pause_reading(self):
        """Pause reading."""
        self.timer.stop()
        self.is_playing = False
        self.is_paused = True
        self.update_play_button()
        self.status_label.setText("⏸ Paused • Press Space to resume • ↑↓ adjust speed")
    
    def stop_reading(self):
        """Stop reading and reset."""
        self.timer.stop()
        self.is_playing = False
        self.is_paused = False
        self.current_index = 0
        self.orp_display.clear()
        self.progress_bar.setValue(0)
        self.update_play_button()
        self.status_label.setText("⏹ Stopped • Press Space to start")
    
    def rewind(self):
        """Rewind by a number of words."""
        if not self.tokens:
            return
        
        # Calculate rewind amount
        rewind_amount = max(REWIND_WORDS, len(self.tokens) // 20)
        rewind_amount = rewind_amount * self.words_per_flash
        
        self.current_index = max(0, self.current_index - rewind_amount)
        self.update_progress()
        self.update_time_estimate()
        
        # Show the current word
        if self.is_playing:
            self.timer.stop()
            self.display_next_word()
        else:
            # Show current word without advancing
            self.show_current_word()
            self.status_label.setText(f"⏪ Rewound to word {self.current_index + 1}")
    
    def forward(self):
        """Forward by a number of words."""
        if not self.tokens:
            return
        
        # Calculate forward amount
        forward_amount = max(FORWARD_WORDS, len(self.tokens) // 20)
        forward_amount = forward_amount * self.words_per_flash
        
        self.current_index = min(len(self.tokens) - 1, self.current_index + forward_amount)
        self.update_progress()
        self.update_time_estimate()
        
        # Show the current word
        if self.is_playing:
            self.timer.stop()
            self.display_next_word()
        else:
            # Show current word without advancing
            self.show_current_word()
            self.status_label.setText(f"⏩ Skipped to word {self.current_index + 1}")
    
    def show_current_word(self):
        """Display the current word without advancing."""
        if self.current_index >= len(self.tokens):
            return
        
        end_index = min(self.current_index + self.words_per_flash, len(self.tokens))
        flash_tokens = self.tokens[self.current_index:end_index]
        words = [t['word'] for t in flash_tokens]
        
        if len(words) == 1:
            self.orp_display.display_word(words[0])
        else:
            self.orp_display.display_phrase(words)
    
    def display_next_word(self):
        """Display the next word or phrase."""
        if self.current_index >= len(self.tokens):
            # Finished reading
            self.timer.stop()
            self.is_playing = False
            self.orp_display.display_message("✓ Done!")
            self.progress_bar.setValue(100)
            self.status_label.setText("🎉 Finished! Press Space to restart")
            self.update_play_button()
            return
        
        # Get words for this flash
        end_index = min(self.current_index + self.words_per_flash, len(self.tokens))
        flash_tokens = self.tokens[self.current_index:end_index]
        
        # Get the words
        words = [t['word'] for t in flash_tokens]
        
        # Calculate max delay multiplier for this batch
        max_delay_multiplier = max(t['delay_multiplier'] for t in flash_tokens)
        
        # Display
        if len(words) == 1:
            self.orp_display.display_word(words[0])
        else:
            self.orp_display.display_phrase(words)
        
        # Update progress
        self.current_index = end_index
        self.update_progress()
        self.update_time_estimate()
        
        # Calculate delay for next word
        base_delay = 60000 / self.wpm  # milliseconds
        
        # Apply delay multiplier for punctuation
        delay = base_delay * max_delay_multiplier
        
        # Add slight extra delay for multi-word displays
        if self.words_per_flash > 1:
            delay *= MULTI_WORD_DELAY_MULTIPLIER
        
        # Schedule next word
        self.timer.start(int(delay))
    
    def update_play_button(self):
        """Update play/pause button appearance."""
        if self.is_playing:
            self.play_pause_button.setText("⏸ Pause")
            self.play_pause_button.setObjectName("pauseButton")
        else:
            self.play_pause_button.setText("▶ Play")
            self.play_pause_button.setObjectName("playButton")
        
        # Refresh style
        self.play_pause_button.setStyleSheet("")
        self.play_pause_button.style().unpolish(self.play_pause_button)
        self.play_pause_button.style().polish(self.play_pause_button)
    
    def update_progress(self):
        """Update progress bar."""
        if not self.tokens:
            return
        
        progress = (self.current_index / len(self.tokens)) * 100
        self.progress_bar.setValue(int(progress))
    
    def update_time_estimate(self):
        """Update estimated remaining time."""
        if not self.tokens:
            self.time_label.setText("Remaining: --:--")
            return
        
        remaining_words = len(self.tokens) - self.current_index
        remaining_flashes = remaining_words / self.words_per_flash
        
        # Base time calculation
        base_delay_ms = 60000 / self.wpm
        
        # Account for average delay multiplier
        avg_delay = base_delay_ms * 1.2
        
        # Multi-word adjustment
        if self.words_per_flash > 1:
            avg_delay *= MULTI_WORD_DELAY_MULTIPLIER
        
        remaining_ms = remaining_flashes * avg_delay
        remaining_seconds = int(remaining_ms / 1000)
        
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        
        self.time_label.setText(f"⏱ {minutes}:{seconds:02d}")
        
        if self.is_playing:
            word_num = min(self.current_index, len(self.tokens))
            self.status_label.setText(
                f"📖 Reading: {word_num:,} / {len(self.tokens):,} words • ↑↓ adjust speed"
            )


# =============================================================================
# Main Entry Point
# =============================================================================

def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("QuickRead")
    app.setOrganizationName("QuickRead")
    
    window = QuickReadApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
