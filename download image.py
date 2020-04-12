import urllib.request
import os


def store_raw_images():
    images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n03948459'
    image_urls = urllib.request.urlopen(images_link).read().decode()

    pic_num = 1

    if not os.path.exists('C:/Users/Cihat Mert Baykal/Desktop/images'):
        os.makedirs('C:/Users/Cihat Mert Baykal/Desktop/images')

    for i in image_urls.split('\n'):
        try:
            print(i)
            urllib.request.urlretrieve(i, 'C:/Users/Cihat Mert Baykal/Desktop/images/' + str(pic_num) + ".jpg")

            pic_num += 1

        except Exception as e:
            print(str(e))


store_raw_images()
