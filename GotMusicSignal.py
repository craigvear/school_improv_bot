from PySide2.QtCore import QObject, Signal

# set up signal based emitter for harmony telemetry
class GotMusicSignal(QObject):
    harmony_str = Signal(str)

    def __init__(self):
        super(GotMusicSignal, self).__init__()