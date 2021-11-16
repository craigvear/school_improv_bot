from PySide2.QtCore import QObject, Signal

# set up signal based emitter for AI data emissions
class GotAISignal(QObject):
    ai_str = Signal(str)

    def __init__(self):
        super(GotAISignal, self).__init__()
