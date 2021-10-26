import sys
import threading
import platform

from ast import literal_eval
from operator import itemgetter

PLATFORM = platform.machine()

if PLATFORM == "x86_64":
    from PySide2 import QtCore
    from PySide2.QtCore import Slot
    from PySide2.QtGui import QPainter, Qt, QPen, QColor, QImage
    from PySide2.QtWidgets import (QApplication, QWidget)
else:
    from PySide2 import QtCore
    from PySide2.QtCore import Slot
    from PySide2.QtGui import QPainter, QPen, QColor, QImage
    from PySide2.QtWidgets import (QApplication, QWidget)

from GotOscSignal import GotOscSignal
from OscData import OscData
from ProcessOscSignal import ProcessOscSignal


class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # FP = open a signal streamer
        osc_signal = GotOscSignal()
        # CV = get a stream of data from the AI engine

        # FP = and connect
        osc_signal.osc_str.connect(self.got_osc_signal)
        # CV = nothing to do

        # FP = pass t  o OSC dispatcher for robot control and dict filling
        _osc_data = OscData(osc_signal)
        # CV = fill the dict (using old names for now), no robot control

        # FP & CV = instantiate the visual processing object
        self.process_osc_signal = ProcessOscSignal()

        # FP & CV = start the thread
        self.gui_thread = None
        self.update_gui()

    def update_gui(self):
        # print("-------- updating gui")
        self.update()
        self.gui_thread = threading.Timer(0.1, self.update_gui)
        self.gui_thread.start()

    def paintEvent(self, paint_event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        if len(self.process_osc_signal.queue):
            for i in self.process_osc_signal.queue:
                # print("i {}".format(i))
                element_type, pen_size, size, original_color, position = itemgetter("type",
                                                                                    "pen",
                                                                                    "size",
                                                                                    "color",
                                                                                    "position")(i)
                x, y = itemgetter("x", "y")(position)
                r, g, b, a = itemgetter("r", "g", "b", "a")(original_color)

                color = QColor(r, g, b, a)

                if element_type == "line":
                    painter.setPen(QPen(color, pen_size))
                    painter.drawLine(x, y, x + size, y)
                elif element_type == "ellipse":
                    painter.setPen(QPen(color, 1))
                    painter.setBrush(color)
                    painter.drawEllipse(x, y, size, size)
                elif element_type == "rect":
                    painter.setPen(QPen(color, 1))
                    painter.setBrush(color)
                    painter.drawRect(x, y, x + size, y + size)
                elif element_type == "image":
                    image_to_display = QImage(self.process_osc_signal.external_images[i["image"]])
                    painter.setOpacity(i["image_transparency"])
                    painter.compositionMode = i["image_composition_mode"]
                    painter.drawImage(x, y, image_to_display)

        self.process_osc_signal.update_queue()

        painter.end()

        # print("UPDATED")

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

        if event.key() == QtCore.Qt.Key_Escape:
            self.gui_thread.cancel()
            app.quit()

    @Slot(str)
    def got_osc_signal(self, osc_msg):
        osc_msg = literal_eval(osc_msg)

        screen_resolution = self.geometry()
        height = screen_resolution.height()
        width = screen_resolution.width()

        osc_msg["width"] = width
        osc_msg["height"] = height

        # print("main {}".format(str(osc_msg)))

        self.process_osc_signal.add_to_queue(osc_msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.showFullScreen()
    widget.setWindowTitle("visual robotic score")
    widget.setStyleSheet("background-color:white;")

    if PLATFORM == "x86_64":
        widget.setCursor(Qt.BlankCursor)

    widget.show()

    sys.exit(app.exec_())
