from PySide6.QtWidgets import QApplication

from windows import Windows

app = QApplication()

windows = Windows()
windows.show()

app.exec()
