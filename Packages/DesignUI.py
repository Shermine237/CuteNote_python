#   Design Widget
from PySide6.QtWidgets import QWidget, QLabel, QListWidget, QTextEdit, QPushButton


class MainWindows(QWidget):
    def __init__(self, title, size_tuple=(600, 500)):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(size_tuple[0], size_tuple[1])


class PushButton(QPushButton):
    def __init__(self, title):
        super().__init__(title)
        self.setDisabled(True)


class Label(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)


class ListWidget(QListWidget):
    def __init__(self):
        super().__init__()


class TextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
