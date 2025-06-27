from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QColor, QTextCursor, QFont
import sys

class JarvisUI(QWidget):
    send_message = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis - Voice & Chat Assistant")
        self.setMinimumSize(520, 540)
        self.setStyleSheet("background-color: #23272e;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        self.status_label = QLabel("Idle")
        self.status_label.setStyleSheet("color: #00bfff; font: 10pt 'Segoe UI'; margin-bottom: 4px;")
        layout.addWidget(self.status_label)

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("background: #181a20; color: #eee; border-radius: 8px; padding: 8px; font: 11pt 'Segoe UI';")
        self.chat_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.chat_area)

        entry_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your message...")
        self.input_box.setStyleSheet("background: #fff; color: #222; border-radius: 6px; padding: 8px; font: 11pt 'Segoe UI';")
        self.input_box.returnPressed.connect(self._on_send)
        entry_layout.addWidget(self.input_box)

        self.send_btn = QPushButton("Send")
        self.send_btn.setStyleSheet("background: #00bfff; color: #fff; border-radius: 6px; padding: 8px 18px; font: 10pt 'Segoe UI';")
        self.send_btn.clicked.connect(self._on_send)
        entry_layout.addWidget(self.send_btn)

        layout.addLayout(entry_layout)

        self.clear_btn = QPushButton("Clear Chat")
        self.clear_btn.setStyleSheet("background: #444; color: #fff; border-radius: 6px; padding: 6px 12px; font: 9pt 'Segoe UI';")
        self.clear_btn.clicked.connect(self.clear_chat)
        layout.addWidget(self.clear_btn, alignment=Qt.AlignRight)

    def _on_send(self):
        msg = self.input_box.text().strip()
        if msg:
            self.display_message("You", msg)
            self.input_box.clear()
            self.input_box.setFocus()
            self.send_message.emit(msg)

    def display_message(self, sender, message):
        if sender == "You":
            color = "#00bfff"
            align = "right"
        elif sender == "Jarvis":
            color = "#00ff90"
            align = "left"
        else:
            color = "#ff5555"
            align = "center"
        html = f'<div style="color:{color}; text-align:{align}; margin:4px 0; font-weight:bold;">{sender}: <span style="font-weight:normal; color:#eee;">{message}</span></div>'
        self.chat_area.moveCursor(QTextCursor.End)
        self.chat_area.insertHtml(html)
        self.chat_area.append("")
        self.chat_area.moveCursor(QTextCursor.End)

    def clear_chat(self):
        self.chat_area.clear()

    def set_status(self, status):
        self.status_label.setText(status)

    def run(self):
        self.show()
        self.input_box.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = JarvisUI()
    ui.run()
    sys.exit(app.exec_())
