from PyQt5.QtWidgets import QDialog, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QMetaObject, Qt, Q_ARG

from peppcrawler import PepperplateCrawler
from gui.LoggingOutput import LoggingOutput
from gui.ProcessRunnable import ProcessRunnable
from utils import getRecipeLinks


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.AddWidgets()
        self.CreateLayout()
        self.resize(350, 250)
        self.setWindowTitle("Pepperplate Snipper")
        self.RegisterExportAction()

        self.crawler = PepperplateCrawler()
        self.crawler.SetForm(self)
        self.crawler.visitLoginPage()

    def AddWidgets(self):
        self.emailLabel = QLabel("Pepperplate Email")
        self.email = QLineEdit()
        self.passwordLabel = QLabel("Pepperplate Password")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.logs = LoggingOutput(self)
        self.button = QPushButton("Export")

    def CreateLayout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.emailLabel)
        layout.addWidget(self.email)
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.password)
        layout.addWidget(self.button)
        layout.addWidget(self.logs)
        self.setLayout(layout)

    def RegisterExportAction(self):
        self.button.clicked.connect(self.StartProcess)

    def StartProcess(self):
        self.process = ProcessRunnable(target=self.LoginToPepperplate,
                                       args=(self.email.text(), self.password.text()))
        self.process.start()

    def LoginToPepperplate(self, email, password):
        successful, message = self.crawler.loginToPepperplate(email, password)
        if successful:
            recipeLinks, message = getRecipeLinks(self.crawler)
            self.Log(message)
            self.crawler.ProcessRecipeLinks(recipeLinks, format)
        else:
            self.Log(message)

    def Log(self, message):
        QMetaObject.invokeMethod(self.logs, "append", Qt.QueuedConnection,
                                 Q_ARG(str, message))
