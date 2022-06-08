from PyQt5.QtCore import QObject, pyqtSignal

"""set up PyQT signal based emitter for 
AI data emissions from Nebula
"""

class GotAISignal(QObject):
    ai_str = pyqtSignal(str)

    def __init__(self):
        super(GotAISignal, self).__init__()
