from django.apps import AppConfig

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import numpy as np
import tensorflow as tf

import cv2
from PIL import Image

from object_detection.utils import label_map_util
from object_detection.utils import config_util
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

class ObjectDetection:
    def __init__(self, pipeline, checkpoint, labelmap):
        model_config = config_util.get_configs_from_pipeline_file(pipeline)['model']
        self.detection_model = model_builder.build(model_config=model_config, is_training=False)

        ckpt = tf.compat.v2.train.Checkpoint(model=self.detection_model)
        ckpt.restore(checkpoint).expect_partial()

        self.detect_fn = get_model_detection_function(self.detection_model)

        label_map = label_map_util.load_labelmap(labelmap)
        categories = label_map_util.convert_label_map_to_categories(label_map,
                    max_num_classes=label_map_util.get_max_label_map_index(label_map),
                    use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)

    def detect_vid(self, vid_path):
        cap = cv2.VideoCapture(vid_path)
        CLASSES = set()
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                input_tensor = tf.convert_to_tensor(np.expand_dims(frame, 0), dtype=tf.float32)
                detections, predictions_dict, shapes = self.detect_fn(input_tensor)

                treshold = 0.6
                scores = detections['detection_scores'].numpy()
                classes = set(detections['detection_classes'].numpy()[scores > treshold])
                CLASSES.update(classes)
            else:
                break
        cap.release()
        return [self.category_index[x]['name'] for x in CLASSES]
    
    def detect_pic(self, pic_path):
        image = np.asarray(Image.open('pic_path').convert('RGB'))
        input_tensor = tf.convert_to_tensor(np.expand_dims(image, 0), dtype=tf.float32)
        detections, predictions_dict, shapes = self.detect_fn(input_tensor)

class OdConfig(AppConfig):
    name = 'OD'
    model = ObjectDetection('object_detection_model/pipeline.config', 'object_detection_model/ckpt-16', 
                            'object_detection_model/label_map.pbtxt')
