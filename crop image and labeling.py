# region import
import os
import sys
import tensorflow as tf
import numpy as np
import cv2
import xml.etree.ElementTree as et
from matplotlib import pyplot as plt
from PIL import Image

sys.path.append("..")
from utils import ops as utils_ops
from utils import label_map_util
from utils import visualization_utils as vis_util



# endregion

# region Model İşlemleri
MODEL_NAME = 'deneme'
MODEL_FILE = MODEL_NAME + '.tar.gz'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = os.path.join('training', 'labelmap.pbtxt')
NUM_CLASSES = 90
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
# endregion

# region Label Ayarları
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# endregion

# region Resim Alma İşlemleri
def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)


PATH_TO_TEST_IMAGES_DIR = 'C:/Users/Cihat Mert Baykal/Desktop/test_image/images/'
TEST_IMAGE_PATHS = [os.path.join(PATH_TO_TEST_IMAGES_DIR, '{}.jpg'.format(i)) for i in range(1, 46)]
IMAGE_SIZE = (12, 8)


# endregion

# region XML ve Kırpma İşlemleri
def createXML(folder, filename, filepath, width, height, labelname, xmax, ymax, ):
    xmlfile = et.parse('C:/Users/Cihat Mert Baykal/Desktop/test_image/samples/sample.xml')
    xmlfile.find(".//folder").text = folder
    xmlfile.find(".//filename").text = filename
    xmlfile.find(".//path").text = filepath + filename
    xmlfile.find(".//width").text = width
    xmlfile.find(".//height").text = height
    xmlfile.find(".//name").text = labelname
    xmlfile.find(".//xmax").text = xmax
    xmlfile.find(".//ymax").text = ymax
    xmlfile.write(filepath + str.replace(filename, ".jpg", "") + ".xml")


def cropImages():
    with open('C:/Users/Cihat Mert Baykal/Desktop/test_image/Output.txt') as f:
        lines = f.readlines()
        for line in lines:
            content = line.split('-')
            img = cv2.imread("C:/Users/Cihat Mert Baykal/Desktop/test_image/images/" + content[0])
            height, width = img.shape[:2]
            print(str(height) + " - " + str(width))
            ymin = int(float(content[1]) * height)
            xmin = int(float(content[2]) * width)
            ymax = int(float(content[3]) * height)
            xmax = int(float(content[4]) * width)
            print(str(xmin) + "-" + str(xmax) + "-" + str(ymin) + "-" + str(ymax))
            img2 = img[ymin:ymax, xmin:xmax]
            cv2.imwrite("C:/Users/Cihat Mert Baykal/Desktop/test_image/output/" + content[0], img2)
            createXML("output", content[0], "C:/Users/Cihat Mert Baykal/Desktop/test_image/output/", str(xmax - xmin),
                      str(ymax - ymin), "tabanca", str(xmax - xmin), str(ymax - ymin))


# endregion

# region Tespit ve Etiketleme İşlemleri
def singleImageDetection(image, graph):
    with graph.as_default():
        with tf.Session() as sess:
            # Get handles to input and output tensors
            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            tensor_dict = {}
            for key in [
                'num_detections', 'detection_boxes', 'detection_scores',
                'detection_classes', 'detection_masks'
            ]:
                tensor_name = key + ':0'
                if tensor_name in all_tensor_names:
                    tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                        tensor_name)
            if 'detection_masks' in tensor_dict:
                detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                    detection_masks, detection_boxes, image.shape[0], image.shape[1])
                detection_masks_reframed = tf.cast(
                    tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                tensor_dict['detection_masks'] = tf.expand_dims(
                    detection_masks_reframed, 0)
            image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
            output_dict = sess.run(tensor_dict,
                                   feed_dict={image_tensor: np.expand_dims(image, 0)})
            output_dict['num_detections'] = int(output_dict['num_detections'][0])
            output_dict['detection_classes'] = output_dict[
                'detection_classes'][0].astype(np.uint8)
            output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
            output_dict['detection_scores'] = output_dict['detection_scores'][0]
            if 'detection_masks' in output_dict:
                output_dict['detection_masks'] = output_dict['detection_masks'][0]
    return output_dict


sayac = 1
for image_path in TEST_IMAGE_PATHS:

    image = Image.open(image_path)
    # the array based representation of the image will be used later in order to prepare the
    # result image with boxes and labels on it.
    image_np = load_image_into_numpy_array(image)
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    # Actual detection.
    output_dict = singleImageDetection(image_np, detection_graph)
    print(np.argmax(output_dict['detection_scores']))
    print(output_dict['detection_boxes'][np.argmax(output_dict['detection_scores'])])
    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        output_dict['detection_boxes'],
        output_dict['detection_classes'],
        output_dict['detection_scores'],
        category_index,
        instance_masks=output_dict.get('detection_masks'),
        use_normalized_coordinates=True,
        line_thickness=8)
    plt.figure(figsize=IMAGE_SIZE)
    coordinates = output_dict['detection_boxes'][np.argmax(output_dict['detection_scores'])]
    if sayac == 1:
        text_file = open("C:/Users/Cihat Mert Baykal/Desktop/test_image/Output.txt", "w")
        text_file.write(str(sayac) + ".jpg-" + str(coordinates[0]) + "-" + str(coordinates[1]) + "-" + str(
            coordinates[2]) + "-" + str(coordinates[3]) + "\n")
    else:
        text_file = open("C:/Users/Cihat Mert Baykal/Desktop/test_image/Output.txt", "a")
        text_file.write(str(sayac) + ".jpg-" + str(coordinates[0]) + "-" + str(coordinates[1]) + "-" + str(
            coordinates[2]) + "-" + str(coordinates[3]) + "\n")
    sayac = sayac + 1
text_file.close()
cropImages()
# endregion
