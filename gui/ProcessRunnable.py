from PySide2.QtCore import QRunnable
from PySide2.QtCore import QThreadPool

class ProcessRunnable(QRunnable):
    def __init__(self, target, args):
        QRunnable.__init__(self)
        self.t = target
        self.args = args
        
    def run(self):
        self.t(*self.args)
        
    def start(self):
        QThreadPool.globalInstance().start(self)
