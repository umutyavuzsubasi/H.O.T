import cv2
import urllib.request as net
import numpy as np

resp = net.urlopen("http://192.168.137.148:8080/shot.jpg")
image = np.asarray(bytearray(resp.read()), dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)
cv2.imshow('Video', image)
cv2.waitKey(0)

