import sys

from PyQt5.QtWidgets import QApplication

from utils import createDirectories
from gui.Form import Form


if __name__ == "__main__":
    createDirectories()
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
