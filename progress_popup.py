from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QPushButton, QDialog, QProgressBar, QTextEdit, QVBoxLayout, QLabel, QStyle, QProxyStyle
from math import floor

# TODO: Figure out how to properly handle threading so this stuff works... pain.

class CenteredProgressBarStyle(QProxyStyle):
    def drawControl(self, element, option, painter, widget=None):
        if element == QStyle.CE_ProgressBarLabel:
            # Do not draw default progress bar label
            return

        super().drawControl(element, option, painter, widget)

        if element == QStyle.CE_ProgressBarContents:
            # Draw custom progress label in the middle of the progress bar
            progress = option.rect.width() * (widget.value() / widget.maximum())
            label_width = 40
            label_height = 25
            label_x = option.rect.x() + (option.rect.width() / 2) - (label_width / 2)
            label_y = option.rect.y() + (option.rect.height() / 2) - (label_height / 2)

            # Check if a progress label already exists, and remove it if it does
            for child_widget in widget.children():
                if isinstance(child_widget, QLabel) and child_widget.objectName() == "progress_label":
                    child_widget.deleteLater()

            # Create new progress label and set its properties
            progress_label = QLabel("{}%".format(widget.value()), widget)
            progress_label.setObjectName("progress_label")
            progress_label.setGeometry(int(label_x), int(label_y), int(label_width), int(label_height))
            progress_label.setAlignment(Qt.AlignCenter)

            # Use custom palette colors for progress label and progress bar
            palette = widget.palette()
            progress_color = QColor(138, 43, 226)
            text_color = QColor(189, 195, 199)
            palette.setColor(QPalette.Highlight, progress_color)
            palette.setColor(QPalette.HighlightedText, text_color)
            progress_label.setPalette(palette)
            widget.setPalette(palette)

            # Draw filled progress bar
            painter.fillRect(option.rect.x(), option.rect.y(), int(progress), option.rect.height(), progress_color)

            # Draw empty progress bar
            painter.fillRect(option.rect.x() + int(progress), option.rect.y(), option.rect.width() - int(progress), option.rect.height(), palette.color(QPalette.Window))

            # Show the progress label
            progress_label.show()

class ProgressPopup(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Processing...")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(600, 400)

        # Create progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(0, 50, self.width(), 25)
        self.progress_bar.setStyle(CenteredProgressBarStyle())
        self.progress_bar.setTextVisible(False)

        # Create console log
        self.console_log = QTextEdit(self)
        self.console_log.setGeometry(0, 0, self.width(), self.height())
        self.console_log.setReadOnly(True)

        # Create close button (initially hidden)
        self.close_button = QPushButton("Close", self)
        self.close_button.setGeometry(100, 150, 100, 30)
        self.close_button.setVisible(False)
        self.close_button.clicked.connect(self.accept)

        # Create layout for progress dialog
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.console_log)
        self.layout.addWidget(self.close_button)


    def update_progress(self, progress):
        # Map float progress value to integer value for the progress bar
        int_progress = floor(progress)
        self.progress_bar.setValue(int_progress)

        # Scroll to the bottom of the console log widget
        scrollbar = self.console_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

        # Show close button once progress is complete
        if int_progress == 100:
            self.close_button.setVisible(True)


class ConsoleStream:
    def __init__(self, console_log):
        self.buffer = ""
        self.console_log = console_log

    def write(self, text):
        # Append new text to buffer
        self.buffer += text

        # If buffer contains newline, flush it to the console log
        if "\n" in self.buffer:
            lines = self.buffer.split("\n")
            for line in lines[:-1]:
                self.emit_new_log(line)
            self.buffer = lines[-1]

    def emit_new_log(self, log):
        # Append new log to the console log widget
        self.console_log.append(log)

    def flush(self):
        pass  # Do nothing (required by sys.stdout)