import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QDialog, QVBoxLayout
from PySide2.QtWidgets import QLabel, QLineEdit, QPushButton

from peppcrawler import PepperplateCrawler
from utils import getRecipeLinks


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.AddWidgets()
        self.CreateLayout()
        self.RegisterExportAction()

        self.crawler = PepperplateCrawler()
        self.crawler.SetForm(self)
        self.crawler.visitLoginPage()

    def AddWidgets(self):
        self.email = QLineEdit("Pepperplate Email")
        self.password = QLineEdit("Pepperplate Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.processMessage = QLabel("")
        self.button = QPushButton("Export")

    def CreateLayout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.button)
        layout.addWidget(self.processMessage)
        self.setLayout(layout)

    def RegisterExportAction(self):
        self.button.clicked.connect(self.StartProcess)

    def StartProcess(self):
        successful, message = self.crawler.loginToPepperplate(
            self.email.text(), self.password.text())
        if successful:
            recipeLinks = getRecipeLinks(self.crawler)
            self.crawler.ProcessRecipeLinks(recipeLinks, format)
        else:
            self.Log(message)

    def Log(self, message):
        self.processMessage.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
