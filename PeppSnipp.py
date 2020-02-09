import sys

from PySide2.QtWidgets import QApplication
from gui.Form import Form


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
