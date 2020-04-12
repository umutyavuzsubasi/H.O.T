import os
import cv2 as cv


path = "C:/tensorflow1/models/research/object_detection/images/train"


def resize_image():
    images = os.listdir(path)
    for x in images:
        image = cv.imread(path+ "/" +x);
        height, width = image.shape[:2]
        if width > 640:
         resize_ratio = 640/width
         resized_height = int(height*resize_ratio)
         resized_width = 640
         resized_image = cv.resize(image,(resized_width,resized_height))
         cv.imwrite(path + "/" + x,resized_image)
         print(x + " resized")

resize_image()

