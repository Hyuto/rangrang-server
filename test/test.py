import os, time
import numpy as np

import tensorflow as tf
import cv2

from PIL import Image

from object_detection.utils import label_map_util
from object_detection.utils import config_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import ops as utils_ops

def get_model_detection_function(model):
    """Get a tf.function for detection."""
    @tf.function
    def detect_fn(image):
        """Detect objects in image."""
        image, shapes = model.preprocess(image)
        prediction_dict = model.predict(image, shapes)
        detections = model.postprocess(prediction_dict, shapes)
        return detections, prediction_dict, tf.reshape(shapes, [-1])
    return detect_fn

if __name__ == '__main__':
    start = time.time()
    pipeline_config = os.path.join('object_detection_model/pipeline.config')

    configs = config_util.get_configs_from_pipeline_file(pipeline_config)
    model_config = configs['model']
    detection_model = model_builder.build(
        model_config=model_config, is_training=False)

    # Restore checkpoint
    ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
    ckpt.restore('object_detection_model/ckpt-3').expect_partial()

    detect_fn = get_model_detection_function(detection_model)

    label_map = label_map_util.load_labelmap('object_detection_model/label_map.pbtxt')
    categories = label_map_util.convert_label_map_to_categories(label_map,
        max_num_classes=label_map_util.get_max_label_map_index(label_map),
        use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
    stop_1 = time.time() - start
    cap = cv2.VideoCapture('test/test.mp4')

    start = time.time()
    i = 1
    CLASSES = set()
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            input_tensor = tf.convert_to_tensor(np.expand_dims(frame, 0), dtype=tf.float32)
            detections, predictions_dict, shapes = detect_fn(input_tensor)
            
            treshold = 0.6
            scores = detections['detection_scores'].numpy()
            classes = set(detections['detection_classes'].numpy()[scores > treshold])
            CLASSES.update(classes)

            """ viz_utils.visualize_boxes_and_labels_on_image_array(
                frame,
                detections['detection_boxes'][0].numpy(),
                (detections['detection_classes'][0].numpy() + 1).astype(int),
                detections['detection_scores'][0].numpy(),
                category_index,
                use_normalized_coordinates=True,
                max_boxes_to_draw=200,
                min_score_thresh=.60,
                agnostic_mode=False)
            
            Image.fromarray(np.uint8(frame)).convert('RGB').save(f'{i}.png', format='png') """
            i += 1
        # Break the loop
        else:
            break
    cap.release()
    stop_2 = time.time() - start
    CLASSES = [category_index[x]['name'] for x in CLASSES]

    print(stop_1)
    print(stop_2)
    print(CLASSES)