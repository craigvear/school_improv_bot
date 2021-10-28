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

from GotAISignal import GotAISignal
from AIData import AIData
from processVisualImages import ProcessVisuals


class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # open a signal streamer
        ai_signal = GotAISignal()

        # and connect to emitting stream
        ai_signal.ai_str.connect(self.got_ai_signal)

        # start the ball rolling with all data generation and parsing
        _ai_data_engine = AIData(ai_signal)

        # FP & CV = instantiate the visual processing object
        self.process_AI_signal = ProcessVisuals()

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

        if len(self.process_AI_signal.queue):
            for i in self.process_AI_signal.queue:
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
                    image_to_display = QImage(self.process_AI_signal.external_images[i["image"]])
                    painter.setOpacity(i["image_transparency"])
                    painter.compositionMode = i["image_composition_mode"]
                    # todo - would be good to slice the original image here
                    #  rather than pre-slice into the library
                    # painter.scale(3, 3)
                    # painter.translate(-20, -50)
                    painter.drawImage(x, y, image_to_display)

        self.process_AI_signal.update_queue()

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
    def got_ai_signal(self, ai_msg):
        ai_msg = literal_eval(ai_msg)

        screen_resolution = self.geometry()
        height = screen_resolution.height()
        width = screen_resolution.width()

        ai_msg["width"] = width
        ai_msg["height"] = height

        # print("main {}".format(str(ai_msg)))

        self.process_AI_signal.add_to_queue(ai_msg)


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
