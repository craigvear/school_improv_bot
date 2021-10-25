from PySide2.QtCore import QObject, Signal


class GotOscSignal(QObject):
    osc_str = Signal(str)

    def __init__(self):
        super(GotOscSignal, self).__init__()
