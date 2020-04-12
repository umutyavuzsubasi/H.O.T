# region Library Imports
import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import qtmodern.styles
import time
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage, QMovie, QKeyEvent
from selenium import webdriver
from utils import label_map_util
from utils import visualization_utils as vis_util
from datetime import datetime

# endregion

# region TensorFlow Assignments

MODEL_NAME = 'deneme'
CWD_PATH = os.getcwd()
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, 'frozen_inference_graph.pb')
PATH_TO_LABELS = os.path.join(CWD_PATH, 'training', 'labelmap.pbtxt')
NUM_CLASSES = 1
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
num_detections = detection_graph.get_tensor_by_name('num_detections:0')


# endregion

# region Tensorflow Starter Function

def tfstart():
    global sess, widget, tensorflowbool
    tensorflowbool = 1
    tf.device("/device:GPU:0")
    sess = tf.Session(graph=detection_graph)

    # ret, frame = video.read()
    # image_expanded = np.expand_dims(frame, axis=0)
    # (boxes, scores, classes, num) = sess.run(
    #     [detection_boxes, detection_scores, detection_classes, num_detections],
    #     feed_dict={image_tensor: image_expanded})
    # vis_util.visualize_boxes_and_labels_on_image_array(frame, np.squeeze(boxes), np.squeeze(classes).astype(np.int32),
    #                                                    np.squeeze(scores), category_index,
    #                                                    use_normalized_coordinates=True, line_thickness=8,
    #                                                    min_score_thresh=0.80)
    # vis_util.visualize_boxes_and_labels_on_image_array(
    #     frame,
    #     np.squeeze(boxes),
    #     np.squeeze(classes).astype(np.int32),
    #     np.squeeze(scores),
    #     category_index,
    #     use_normalized_coordinates=True,
    #     line_thickness=5,
    #     min_score_thresh=0.90)
    widget.tftimer.stop()
    widget.stop()
    widget.ConsoleList.addItem(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": TensorFlow Başlatıldı")
    widget.ConsoleList.scrollToBottom()

# endregion

# region Control Functions
# Pan-Tilt Control Function

def moveservos(cors):
    xfark = (cors[3] * 960) - (cors[1] * 960)
    xcenter = (cors[1] * 960) + xfark
    yfark = (cors[2] * 720) - (cors[0] * 720)
    ycenter = (cors[0] * 720) - yfark
    perx = 105 - int(((xcenter / 960) * 61))
    pery = 145 - int(((ycenter / 720) * 35))
    hot.execute_script("document.getElementById('servoSlider1').value = " + str(perx))  # ALT SERVO
    hot.execute_script("document.getElementById('servoSlider2').value = " + str(pery))  # UST SERVO
    button = hot.find_element_by_id("moveservos")
    button.click()


# Motor Control Function

def runMotors(key):
    if (key == "w"):
        hot.execute_script("document.getElementById('solmotorslider').value = 1200")
        hot.execute_script("document.getElementById('sagmotorslider').value = 1300")
        button = hot.find_element_by_id("moveservos")
        button.click()
    elif (key == "a"):
        hot.execute_script("document.getElementById('solmotorslider').value = 1000")
        hot.execute_script("document.getElementById('sagmotorslider').value = 1700")
        button = hot.find_element_by_id("moveservos")
        button.click()
    elif (key == "s"):
        hot.execute_script("document.getElementById('solmotorslider').value = 1000")
        hot.execute_script("document.getElementById('sagmotorslider').value = 1000")
        button = hot.find_element_by_id("moveservos")
        button.click()
    elif (key == "d"):
        hot.execute_script("document.getElementById('solmotorslider').value = 1700")
        hot.execute_script("document.getElementById('sagmotorslider').value = 1000")
        button = hot.find_element_by_id("moveservos")
        button.click()


# endregion

# region User Interfaces
# Loading UI

class loading(QDialog):

    def __init__(self):
        super(loading, self).__init__()
        loadUi('ui/loading.ui', self)
        movie = QMovie("ui/gif2.gif")
        self.LGif.setMovie(movie)
        movie.setScaledSize(QSize(100, 100))
        movie.start()
        self.LLabel.setText("Yükleniyor...")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start)
        self.timer.start(1500)

    def start(self):
        loadwidget.close()
        widget.show()
        self.timer.stop()

# Settings UI

class settings(QDialog):

    def __init__(self):
        super(settings, self).__init__()
        loadUi('ui/settings.ui', self)
        self.setWindowTitle('H.O.T Ayarlar')
        self.shotBrowse.clicked.connect(self.Browseshot)
        self.videoBrowse.clicked.connect(self.Browsevideo)

    def Browseshot(self):
        global shotlocation
        sname = str(QFileDialog.getExistingDirectory(self, "Ekran Alıntısı Konum Diyaloğu"))
        shotlocation = sname.replace("/", "\\")
        self.shotLocation.setText(shotlocation)

    def Browsevideo(self):
        global videolocation
        vname = str(QFileDialog.getExistingDirectory(self, "Video Konum Diyaloğu"))
        videolocation = vname.replace("/", "\\")
        self.videoLocation.setText(videolocation)

    def closeEvent(self, event):
        widget.show()
        self.close()

# Main UI

class hotui(QDialog):

    def __init__(self):
        super(hotui, self).__init__()
        loadUi('ui/test.ui', self)
        self.setWindowTitle('H.O.T')
        self.settings = settings()
        self.butonBasla.clicked.connect(self.start)
        self.butonDur.clicked.connect(self.stop)
        self.butonLed.clicked.connect(self.ledToggle)
        self.butonZin.clicked.connect(self.zoomIn)
        self.butonZout.clicked.connect(self.zoomOut)
        self.butonSave.clicked.connect(self.saveShot)
        self.butonRecord.clicked.connect(self.saveVideo)
        self.butonSettings.clicked.connect(self.openSettings)
        self.ZMLabel.setText("% 0")
        self.timer = QTimer(self)
        self.tftimer = QTimer(self)
        self.layer.setPixmap(QPixmap('ui/noframe.png'))
        self.start()



    def keyPressEvent(self, event : QKeyEvent):
        if type(event) == QKeyEvent:

            # here accept the event and do something
            if (event.key() == Qt.Key_W):
                print("w")
                runMotors("w")
            elif (event.key() == Qt.Key_A):
                runMotors("a")
                print("a")
            elif (event.key() == Qt.Key_S):
                runMotors("s")
                print("s")
            elif (event.key() == Qt.Key_D):
                runMotors("d")
                print("d")
            event.accept()
        else:
            event.ignore()

    # def keyReleaseEvent(self, event):
    #     if type(event) == QKeyEvent:
    #         # here accept the event and do something
    #         if (event.key() == Qt.Key_W):
    #             time.sleep(0.5)
    #             runMotors("s")



    def start(self):
        global video, tensorflowbool
        video = cv2.VideoCapture(cameraip + "video")
        # video = cv2.VideoCapture(0)
        ret = video.set(3, 960)
        ret = video.set(4, 720)
        video.set(38, 1)
        if tensorflowbool == 0:
            self.ConsoleList.addItem(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": TensorFlow Başlatılıyor")
            self.ConsoleList.scrollToBottom()
            self.tftimer.timeout.connect(tfstart)
            self.tftimer.start(500)
        else:
            self.butonBasla.setEnabled(0)
            self.butonDur.setEnabled(1)
            self.layer.setPixmap(QPixmap('ui/layer.png'))
            self.timer.timeout.connect(self.update)
            self.timer.start(33)
            self.ConsoleList.addItem(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Tespit Başlatılmıştır")
            self.ConsoleList.scrollToBottom()

    def update(self):
        global video, sayac, frame, videooutput, videobool
        if not self.timer.isActive():
            self.butonDur.setEnabled(0)
            self.butonBasla.setEnabled(1)
            self.layer.setPixmap(QPixmap('ui/noframe.png'))
            self.imgView.setPixmap(QPixmap('ui/noframe.png'))
        else:
            sayac = sayac + 1
            ret, frame = video.read()
            if (sayac % 6 == 0):
                if (sayac == 30):
                    sayac = 1
                frame_expanded = np.expand_dims(frame, axis=0)

                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: frame_expanded})

                vis_util.visualize_boxes_and_labels_on_image_array(
                    frame,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=5,
                    min_score_thresh=0.90)

                if int(np.amax(scores) * 100) > 90:
                    coordinates = boxes[0][np.argmax(scores[0])]
                    moveservos(coordinates)
                    self.DetectionList.addItem("Tespit yapıldı. İsabet oranı : " + str(int(np.amax(scores) * 100)))
                    self.DetectionList.scrollToBottom()
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                               QImage.Format_RGB888)
                    convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
                    pixmap = QPixmap(convertToQtFormat)
                    resizeImage = pixmap.scaled(960, 720, Qt.KeepAspectRatio)
                    QApplication.processEvents()
                    self.layer.setPixmap(resizeImage)
                    self.layer.setScaledContents(1)
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
            pixmap = QPixmap(convertToQtFormat)
            resizeImage = pixmap.scaled(960, 720, Qt.KeepAspectRatio)
            QApplication.processEvents()
            self.imgView.setPixmap(resizeImage)
            self.imgView.setScaledContents(1)
            self.layer.setPixmap(QPixmap('ui/layer.png'))
            if videobool == 1:
                videooutput.write(frame)

    def stop(self):
        video.release()
        self.timer.stop()
        self.butonDur.setEnabled(0)
        self.butonBasla.setEnabled(1)
        self.layer.setPixmap(QPixmap('ui/noframe.png'))
        self.imgView.setPixmap(QPixmap('ui/noframe.png'))
        if tensorflowbool == 1:
            self.ConsoleList.addItem(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Tespit Durdurulmuştur")
            self.ConsoleList.scrollToBottom()

    def ledToggle(self):
        button = driver.find_element_by_id('flashbtn')
        button.click()
        if button.get_attribute("class") == "btn btn-sm btn-default":
            self.butonLed.setStyleSheet("background-image: url('ui/buttons/led.png')")
            self.ConsoleList.addItem(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": LED Devre Dışı Bırakılmıştır")
            self.ConsoleList.scrollToBottom()
        else:
            self.butonLed.setStyleSheet("background-image: url('ui/buttons/led-hover.png')")
            self.ConsoleList.addItem(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": LED Etkinleştirilmiştir")
            self.ConsoleList.scrollToBottom()

    def zoomIn(self):
        global zoomcount
        if int(zoomcount) != 100:
            zoomcount += 5
            zdriver.get(cameraip + "ptz?zoom=" + str(zoomcount))
            self.ZMLabel.setText("% " + str(zoomcount))
            self.ConsoleList.addItem(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": %5 Yakınlaştırma Yapılmıştır")
            self.ConsoleList.scrollToBottom()

    def zoomOut(self):
        global zoomcount
        if int(zoomcount) != 0:
            zoomcount -= 5
            zdriver.get(cameraip + "ptz?zoom=" + str(zoomcount))
            self.ZMLabel.setText("% " + str(zoomcount))
            self.ConsoleList.addItem(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": %5 Uzaklaştırma Yapılmıştır")
            self.ConsoleList.scrollToBottom()

    def saveShot(self):
        if shotlocation != "":
            if (video.isOpened() == True):
                if (frame != ""):
                    cv2.imwrite(shotlocation + "\Shot - " + str((len(os.listdir(shotlocation)) + 1)) + ".jpg", frame)
                    self.ConsoleList.addItem(
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Ekran Görüntüsü Alınmıştır")
                    self.ConsoleList.scrollToBottom()
                else:
                    self.ConsoleList.addItem(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Tespit Açık Değildir")
                    self.ConsoleList.scrollToBottom()
            else:
                self.ConsoleList.addItem(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Kayıt Alınmamaktadır")
                self.ConsoleList.scrollToBottom()
        else:
            self.ConsoleList.addItem(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Konum Bilgilerini Giriniz")
            self.ConsoleList.scrollToBottom()

    def saveVideo(self):
        global videolocation, videobool, videooutput
        if videolocation != "":
            if video.isOpened() == True:
                if frame != "":
                    if videobool == 0:
                        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                        videooutput = cv2.VideoWriter(
                            videolocation + "\Video - " + str((len(os.listdir(videolocation)) + 1)) + ".avi", fourcc,
                            15,
                            (960, 720))
                        self.ConsoleList.addItem(
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Kayıt Başlatılmıştır")
                        self.ConsoleList.scrollToBottom()
                        videobool = 1
                    else:
                        videooutput.release()
                        self.ConsoleList.addItem(
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Kayıt Durdurulmuştur")
                        self.ConsoleList.scrollToBottom()
                        videobool = 0
                else:
                    self.ConsoleList.addItem(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Tespit Açık Değildir")
                    self.ConsoleList.scrollToBottom()

            else:
                self.ConsoleList.addItem(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Kayıt Alınmamaktadır")
                self.ConsoleList.scrollToBottom()
        else:
            self.ConsoleList.addItem(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": Konum Bilgilerini Doldurunuz")
            self.ConsoleList.scrollToBottom()

    def openSettings(self):
        self.settings.show()
        self.close()

# endregion

# region Initialize Webcam UI and Motors UI
veri = os.popen("arp -a").read()
veri = veri.split("\n")
cameraip = ""
camerashot = ""
hotip = ""
for x in veri:
    if x.find("8c-f5-a3-70-54-01") == 24:
        a = x[2: 2 + 15]
        a = a.replace(" ", "")
        camerashot = "http://" + a + ":8080/shot.jpg"
        cameraip = "http://" + a + ":8080/"
        break
for x in veri:
    if x.find("3c-71-bf-2a-a1-da") == 24:
        a = x[2: 2 + 15]
        a = a.replace(" ", "")
        hotip = "http://" + a + "/"
        break
# endregion

# region Initialize Global Variables
sayac = 1
video = ""
sess = ""
tensorflowbool = 0
shotlocation = ""
videolocation = ""
videobool = 0
videooutput = ""
frame = ""
# endregion

# region Initialize Camera Options with WebDriver
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(chrome_options=options)
driver.get(cameraip + "settings_window.html")
zoomcount = 0
zdriver = webdriver.Chrome(chrome_options=options)
# endregion

# region Initialize Motors positions
hot = webdriver.Chrome(chrome_options=options)
hot.get(hotip)
hot.execute_script("document.getElementById('servoSlider1').value = 70")
hot.execute_script("document.getElementById('servoSlider2').value = 110")
hot.execute_script("document.getElementById('solmotorslider').value = 1000")
hot.execute_script("document.getElementById('sagmotorslider').value = 1000")
button = hot.find_element_by_id("moveservos")
button.click()
# endregion

# region Initialize UI Dialogs

app = QApplication(sys.argv)
qtmodern.styles.dark(app)
loadwidget = loading()
loadwidget.setWindowFlags(Qt.FramelessWindowHint)
widget = hotui()
loadwidget.show()

# endregion

sys.exit(app.exec_())
