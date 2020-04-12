import os
import shutil

path = "C:/tensorflow1/models/research/object_detection/images/Tabanca Veri"
newpath = "C:/tensorflow1/models/research/object_detection/images/test"


def move_image():
    sayac = 1
    images = os.listdir(path)
    for x in images:
        image = x.strip().lower()
        filename = image.split(".")[0]
        extension = image.split(".")[1]
        if extension in "jpg":
            sayac = sayac + 1
            xml = filename + ".xml"
            if os.path.isfile(path + "/" + xml):
                shutil.move(path+"/"+filename + "." + extension,newpath)
                shutil.move(path + "/" + xml, newpath)
                print(filename + " image and label file is moved")
            else:
                print(filename + " image and label file is not moved")


move_image()
