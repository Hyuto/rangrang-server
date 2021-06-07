from django.apps import AppConfig
from tf_model import DetectionModel

class CdConfig(AppConfig):
    name = 'CD'
    model = DetectionModel('color_detection_model/pipeline.config', 'color_detection_model/ckpt-16', 
                           'color_detection_model/label_map.pbtxt')