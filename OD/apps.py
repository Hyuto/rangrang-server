from django.apps import AppConfig
from tf_model import DetectionModel

class OdConfig(AppConfig):
    name = 'OD'
    model = DetectionModel('object_detection_model/pipeline.config', 'object_detection_model/ckpt-16', 
                           'object_detection_model/label_map.pbtxt')
