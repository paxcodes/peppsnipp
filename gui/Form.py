from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QRadioButton
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QApplication
from PyQt5.QtCore import QMetaObject, Qt, Q_ARG
from PyQt5.QtCore import pyqtSlot

from peppcrawler import PepperplateCrawler
from gui.LoggingOutput import LoggingOutput
from gui.ProcessRunnable import ProcessRunnable
from utils import getRecipeLinks


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.AddWidgets()
        self.CreateLayout()
        self.resize(350, 600)
        self.setWindowTitle("Pepperplate Snipper")
        self.RegisterExportAction()

        self.crawler = PepperplateCrawler()
        self.crawler.SetForm(self)
        self.crawler.visitLoginPage()

    def AddWidgets(self):
        self.formatLabel = QLabel("Export Format")
        self.jsonRadioButton = QRadioButton("JSON")
        self.jsonRadioButton.value = self.exportFormat = "j"
        self.jsonRadioButton.setChecked(True)

        self.pngRadioButton = QRadioButton("PNG")
        self.pngRadioButton.value = "p"
        self.bothRadioButton = QRadioButton("Both")
        self.bothRadioButton.value = "b"
        self.__RegisterRadioButtonToggled()

        self.emailLabel = QLabel("Pepperplate Email")
        self.email = QLineEdit()
        self.passwordLabel = QLabel("Pepperplate Password")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.logs = LoggingOutput(self)
        self.button = QPushButton("Export")

    def CreateLayout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.formatLabel)

        rbLayout = QHBoxLayout()
        rbLayout.addWidget(self.jsonRadioButton)
        rbLayout.addWidget(self.pngRadioButton)
        rbLayout.addWidget(self.bothRadioButton)
        layout.addLayout(rbLayout)

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
        QMetaObject.invokeMethod(self, "EnableForm", Qt.QueuedConnection,
                                 Q_ARG(bool, False))
        self.process = ProcessRunnable(target=self.LoginToPepperplate,
                                       args=(self.email.text(), self.password.text()))
        self.process.start()

    def LoginToPepperplate(self, email, password):
        successful, message = self.crawler.loginToPepperplate(email, password)
        if successful:
            recipeLinks, message = getRecipeLinks(self.crawler)
            self.Log(message)
            self.crawler.ProcessRecipeLinks(recipeLinks, self.exportFormat)
        else:
            self.__EnableForm(True)
            self.Log(message)

    def Log(self, message):
        QMetaObject.invokeMethod(self.logs, "append", Qt.QueuedConnection,
                                 Q_ARG(str, message))

    def __RegisterRadioButtonToggled(self):
        self.jsonRadioButton.toggled.connect(self.SetFormat)
        self.pngRadioButton.toggled.connect(self.SetFormat)
        self.bothRadioButton.toggled.connect(self.SetFormat)

    def SetFormat(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.exportFormat = radioButton.value

    @pyqtSlot(bool)
    def EnableForm(self, enabled):
        self.button.setEnabled(enabled)
        self.email.setEnabled(enabled)
        self.password.setEnabled(enabled)
