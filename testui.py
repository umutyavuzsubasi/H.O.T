import sys
from PyQt5.QtCore import pyqtSlot, Qt, QTimer, QSize
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage, QMovie, QKeyEvent
import cv2
import qtmodern.styles


class loading(QDialog):
    def __init__(self, parent=None):
        super(loading, self).__init__()
        loadUi('ui/loading.ui', self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start)
        self.timer.start(2000)
        movie = QMovie("ui/gif2.gif")
        self.LGif.setMovie(movie)
        movie.setScaledSize(QSize(100, 100))
        movie.start()
        self.LLabel.setText("Yükleniyor...")

    def start(self):
        loadwidget.close()
        widget.show()
        self.timer.stop()


class deneme(QDialog):
    def __init__(self):
        super(deneme, self).__init__()
        loadUi('ui/test.ui', self)
        self.setWindowTitle('Deneme 123')
        self.butonSave.clicked.connect(self.saveShot)
        # self.timer1 = QTimer(self)
        # self.timer2 = QTimer(self)
        # self.timer1.timeout.connect(self.loading)
        # self.timer1.start(5)

        # self.ZMLabel.setText("% 0")
        # self.imgView.setPixmap(QPixmap('ui/noframe.png').scaled(960, 720, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def loading(self):
        self.timer2.timeout.connect(self.update)
        self.timer2.start(5)

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            # here accept the event and do something
            if(event.key() == Qt.Key_W):
                print("W ya bastın")
            elif (event.key() == Qt.Key_A):
                print("A ya bastın")
            elif (event.key() == Qt.Key_S):
                print("S ya bastın")
            elif (event.key() == Qt.Key_D):
                print("D ya bastın")
            event.accept()
        else:
            event.ignore()

    def update(self):
        ret, frame = cap.read()
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        resizeImage = pixmap.scaled(960, 720, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        QApplication.processEvents()
        self.imgView.setPixmap(resizeImage)
        self.imgView.setScaledContents(1)

    def saveShot(self):
        shot = cv2.imread("")


app = QApplication(sys.argv)
qtmodern.styles.dark(app)
loadwidget = loading()
loadwidget.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
loadwidget.show()

widget = deneme()

# cap = cv2.VideoCapture("http://192.168.137.206:8080/video")
cap = cv2.VideoCapture(0)
ret = cap.set(3, 960)
ret = cap.set(4, 720)
sys.exit(app.exec_())
