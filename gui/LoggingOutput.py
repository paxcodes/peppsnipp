from PySide2.QtWidgets import QTextEdit
from PySide2.QtCore import Slot
from PySide2.QtGui import QTextCursor


class LoggingOutput(QTextEdit):
    def __init__(self, parent=None):
        super(LoggingOutput, self).__init__(parent)
        self.setReadOnly(True)
        self.setLineWrapMode(self.NoWrap)
        self.insertPlainText("")

    @Slot(str)
    def append(self, text):
        self.moveCursor(QTextCursor.End)
        current = self.toPlainText()

        if current == "":
            self.insertPlainText(text)
        else:
            self.insertPlainText("\n" + text)

        sb = self.verticalScrollBar()
        sb.setValue(sb.maximum())
