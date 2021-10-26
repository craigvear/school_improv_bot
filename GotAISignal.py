from PySide2.QtCore import QObject, Signal


class GotAISignal(QObject):
    ai_str = Signal(str)

    def __init__(self):
        super(GotAISignal, self).__init__()