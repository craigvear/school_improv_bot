# from PySide2 import QtCore, QtGui, QtWidgets
#
# # from PIL import Image, ImageQt, ImageEnhance
#
# # from gui import Ui_MainWindow
#
#
# class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setupUi(self)
#         self.ShowIButton.clicked.connect(self.do_test)
#
#         self.scene = QtWidgets.QGraphicsScene(self)
#         self.graphicsView.setScene(self.scene)
#
#         self.pixmap_item = self.scene.addPixmap(QtGui.QPixmap())
#
#         self.level = 1
#         self.enhancer = None
#         self.timer = QtCore.QTimer(interval=500, timeout=self.on_timeout)
#
#     @QtCore.Slot()
#     def do_test(self):
#         input_img = Image.open("image1.png")
#         self.enhancer = ImageEnhance.Brightness(input_img)
#         self.timer.start()
#         self.ShowIButton.setDisabled(True)
#
#     @QtCore.Slot()
#     def on_timeout(self):
#         if self.enhancer is not None:
#             result_img = self.enhancer.enhance(self.level)
#             qimage = ImageQt.ImageQt(result_img)
#             self.pixmap_item.setPixmap(QtGui.QPixmap.fromImage(qimage))
#         if self.level > 7:
#             self.timer.stop()
#             self.enhancer = None
#             self.level = 0
#             self.ShowIButton.setDisabled(False)
#         self.level += 1
#
#
# if __name__ == "__main__":
#     import sys
#
#     app = QtWidgets.QApplication(sys.argv)
#     w = MainWindow()
#     w.show()
#     sys.exit(app.exec_())

import sys
from PySide2.QtGui import QPixmap, QPainter
from PySide2.QtWidgets import QMainWindow, QApplication, QLabel

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.title = "Image Viewer"
        self.setWindowTitle(self.title)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        label = QLabel(self)
        pixmap = QPixmap('images/2-5-1_guitar_lick_1.png')
        pixmap_scaled = pixmap.scaled(200, 100)


        label.setPixmap(pixmap_scaled)
        # self.setCentralWidget(label)
        self.resize(pixmap.width() /2 , pixmap.height() /2)



app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())

# import sys
# from PySide2 import QtCore, QtGui, QtWidgets
#
# app = QtWidgets.QApplication(sys.argv)
#
# # get image and load as pixmap
# pixmap = QtGui.QPixmap('images/2-5-1_guitar_lick_1.png')
#
# # what is size of image
#
# # rescale/ zoom in pixels or % of own geometry
# pixmap_scaled = pixmap.scaled(500, 300)
#
# # transform into painter object
# qp = QtGui.QPainter(pixmap_scaled)
#
# # make a label
# label = QtWidgets.QLabel()
# label.setFixedSize(300, 200)
#
# # put scaled image into label
# label.setPixmap(pixmap_scaled)
#
# # show
# label.show()
#
# app.exec_()

# import sys
# from PySide2.QtWidgets import *
# from PySide2.QtGui import *
# from PySide2.QtCore import *
#
# class Example(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setGeometry(30, 30, 500, 300)
#         self._photo = QGraphicsPixmapItem()
#         self._scene = QGraphicsScene(self)
#         self.graphicsView.setScene(self._scene)
#
#         self.pixmap_item = self.scene.addPixmap(QPixmap())
#
#     def paintEvent(self, event):
#         painter = QPainter(self)
#
#         self.pixure = QPixmap("images/2-5-1_guitar_lick_1.png")
#         self.pixmap_item.setPixmap(QtGui.QPixmap.fromImage(self.pixure))
#         # pixmap_scaled = pixmap.scaled(64, 64)
#         self.fitInView()
#
#         # painter.drawPixmap(self.rect(), self.pixure)
#         # pen = QPen(Qt.red, 3)
#         # painter.setPen(pen)
#         # painter.drawLine(10, 10, self.rect().width() -10 , 10)
#
#     def fitInView(self, scale=True):
#         factor = 8
#         self._zoom = 5
#         rect = QRectF(self._photo.pixmap().rect())
#         if True:
#             self.setSceneRect(rect)
#             if True:
#                 unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
#                 self.scale(1 / unity.width(), 1 / unity.height())
#                 viewrect = self.viewport().rect()
#                 scenerect = self.transform().mapRect(rect)
#                 factor = min(viewrect.width() / scenerect.width(),
#                              viewrect.height() / scenerect.height())
#                 self.scale(factor, factor)
#             # self._zoom = 0
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Example()
#     ex.show()
#     sys.exit(app.exec_())


#
#
# from PySide2 import QtCore
# from PySide2.QtCore import Slot
# from PySide2.QtGui import QPainter, Qt, QPen, QColor, QImage, QGuiApplication
# from PySide2.QtWidgets import (QApplication, QWidget)
# import sys
# from PySide2 import QtCore
# from PySide2.QtCore import Slot
# from PySide2.QtGui import QPainter, Qt, QPen, QColor, QImage
# from PySide2.QtWidgets import (QApplication, QWidget)
#
#
# class MyWidget(QWidget):
#     def __init__(self):
#         QWidget.__init__(self)
#         painter = QPainter()
#         # painter.setRenderHint(QPainter.Antialiasing, True)
#
#         image_path = "images/2-5-1_guitar_lick_1.png"
#
#         image_to_display = QImage(image_path)
#         painter.setOpacity(0.2)
#         painter.compositionMode = QPainter.CompositionMode_HardLight
#                             # todo - would be good to slice the original image here
#         #  rather than pre-slice into the library
#         # painter.scale(3, 3)
#         # painter.translate(-20, -50)
#         painter.drawImage(0, 0, image_to_display)
#
#
# if __name__=="__main__":
#     app = QApplication(sys.argv)
#
#     widget = MyWidget()
#     widget.resize(800, 600)
#     # widget.showFullScreen()
#     # widget.setWindowTitle("visual robotic score")
#     widget.setStyleSheet("background-color:white;")
#
#     widget.setCursor(Qt.BlankCursor)
#
#     widget.show()
#
#     sys.exit(app.exec_())