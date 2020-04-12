import os
import cv2
import numpy as np
import tensorflow as tf
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QListView, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage
import qtmodern.styles


class tsui(QDialog):
    def __init__(self):
        super(tsui, self).__init__()
        loadUi('ui/test.ui', self)
        self.setWindowTitle('H.O.T')
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.butonBasla.clicked.connect(self.start)
        self.butonDur.clicked.connect(self.stop)
        self.butonSave.clicked.connect(self.takeShot)
        self.butonRecord.clicked.connect(self.takeVideo)
        self.settings = settings()
        self.butonSettings.clicked.connect(self.openSettings)
        self.butonDur.setEnabled(0)
        self.layer.setPixmap(QPixmap('ui/noframe.png'))

    def start(self):
        self.butonBasla.setEnabled(0)
        self.butonDur.setEnabled(1)
        self.layer.setPixmap(QPixmap('ui/layer.png'))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(33)

    def update(self):
        global sayac, frame, videooutput, videobool
        sayac = sayac + 1
        ret, frame = video.read()
        if (sayac == 30):
            sayac = 1
            frame_expanded = np.expand_dims(frame, axis=0)
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: frame_expanded})
            # Draw the results of the detection (aka 'visulaize the results')
            vis_util.visualize_boxes_and_labels_on_image_array(
                frame,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=8,
                min_score_thresh=0.85)
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)

        pixmap = QPixmap('ui/deneme.png')
        resizeImage = pixmap.scaled(640, 480, Qt.KeepAspectRatio)
        QApplication.processEvents()
        self.imgView.setPixmap(resizeImage)
        self.imgView.setScaledContents(1)
        if videobool == 1:
            videooutput.write(frame)
        # if int(np.amax(scores)*100) > 70:
        #     self.isabetList.addItem("Tespit yapıldı. İsabet oranı : " + str(int(np.amax(scores)*100)))
        #     self.isabetList.scrollToBottom()

    def stop(self):
        self.timer.stop()
        self.butonDur.setEnabled(0)
        self.butonBasla.setEnabled(1)
        self.layer.setPixmap(QPixmap('ui/noframe.png'))
        self.imgView.setPixmap(QPixmap('ui/noframe.png'))

    def openSettings(self):
        self.settings.show()
        self.close()

    def takeShot(self):
        if shotlocation != "":
            if video.isOpened() == True:
                if frame != "":
                    cv2.imwrite(shotlocation + "\Shot - " + str((len(os.listdir(shotlocation)) + 1)) + ".jpg", frame)
                else:
                    print("Tespit açık değildir")
            else:
                print("Kayıt Alınamamaktadır")
        else:
            print("Lütfen Shot konumunu giriniz")

    def takeVideo(self):
        global videolocation, videobool, videooutput
        if videolocation != "":
            if video.isOpened() == True:
                if frame != "":
                    if videobool == 0:
                        print(videolocation + "\Video - " + str((len(os.listdir(videolocation)) + 1)) + ".avi")
                        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                        videooutput = cv2.VideoWriter(
                            videolocation + "\Video - " + str((len(os.listdir(videolocation)) + 1)) + ".avi", fourcc,
                            15,
                            (640, 480))
                        print("Kayıt Başladı")
                        videobool = 1
                    else:
                        videooutput.release()
                        print("Kayıt Durdurulmuştur")
                        videobool = 0
                else:
                    print("Tespit açık değildir")
            else:
                print("Kayıt Alınmamaktadır")
        else:
            print("Lütfen Video konumunu giriniz")


class settings(QDialog):
    def __init__(self):
        super(settings, self).__init__()
        loadUi('ui/settings.ui', self)
        self.setWindowTitle('H.O.T Settings')
        self.shotBrowse.clicked.connect(self.Browseshot)
        self.videoBrowse.clicked.connect(self.Browsevideo)

    def Browseshot(self):
        global shotlocation
        sname = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        shotlocation = sname.replace("/", "\\")
        self.shotLocation.setText(shotlocation)

    def Browsevideo(self):
        global videolocation, videooutput
        vname = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        videolocation = vname.replace("/", "\\")
        self.videoLocation.setText(videolocation)

    def closeEvent(self, event):
        widget.show()
        self.close()


# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

# Name of the directory containing the object detection module we're using
MODEL_NAME = 'deneme'

# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, 'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH, 'training', 'labelmap.pbtxt')

# Number of classes the object detector can identify
NUM_CLASSES = 1

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)

# Define input and output tensors (i.e. data) for the object detection classifier
# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')
sayac = 1
shotlocation = ""
videolocation = ""
videobool = 0
videooutput = ""
frame = ""
# Initialize webcam feed
video = cv2.VideoCapture(0)
ret = video.set(3, 640)
ret = video.set(4, 480)
app = QApplication(sys.argv)
widget = tsui()
qtmodern.styles.dark(app)
widget.show()
sys.exit(app.exec_())
