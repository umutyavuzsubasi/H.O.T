import numpy as np
import os
import sys
import tensorflow as tf
import cv2


from utils import label_map_util  # Etiketleme Kütüphanesi
from utils import visualization_utils as vis_util  # Görüntüleme Kütüphanesi

cap = cv2.VideoCapture(0)  # Kamera Görüntü Alma

# Model Hazırlıkları

MODEL_NAME = 'ssd_deneme'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'  # Model Dosya Yolu

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

# Label Map Yükleme
PATH_TO_LABELS = os.path.join('ssd_deneme', 'labelmap.pbtxt')  # Label Map Dosya Yolu
NUM_CLASSES = 1  # Tespit Yapılcak Sınıf Sayısı
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# Tespit

def run_inference_for_single_image(image, graph):
    with graph.as_default():

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


        image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
        # Run inference
        output_dict = sess.run(tensor_dict,
                               feed_dict={image_tensor: np.expand_dims(image, 0)})
        # all outputs are float32 numpy arrays, so convert types as appropriate
        output_dict['num_detections'] = int(output_dict['num_detections'][0])
        output_dict['detection_classes'] = output_dict[
            'detection_classes'][0].astype(np.uint8)
        output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
        output_dict['detection_scores'] = output_dict['detection_scores'][0]

    return output_dict


# In[11]:

with tf.Session(graph=detection_graph) as sess:
    while True:
        ret, image_np = cap.read()
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        # Actual detection.
        output_dict = run_inference_for_single_image(image_np, detection_graph)
        # Visualization of the results of a detection.
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            output_dict['detection_boxes'],
            output_dict['detection_classes'],
            output_dict['detection_scores'],
            category_index,
            use_normalized_coordinates=True,
            line_thickness=5,
            skip_scores = False)

        cv2.imshow('Video', image_np)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        # tf.image.crop_to_bounding_box(cap.read(),output_dict['detection_boxes'])