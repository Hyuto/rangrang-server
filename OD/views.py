from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from .apps import OdConfig

import os
from random import sample
from string import digits, ascii_uppercase, ascii_lowercase
from datetime import datetime

def rand_name():
    chars = ascii_lowercase + ascii_uppercase + digits
    return ''.join(sample(chars, 8))

class ObjectDetectionVideo(APIView):
    permission_classes = []
    parser_classes = (MultiPartParser, )

    def get_file_name(self, path):
        while True:
            name = f"{datetime.now().strftime('%m-%d-%Y')}_{rand_name()}.mp4"
            if not os.path.exists(os.path.join(path, name)):
                return os.path.join(path, name)

    def post(self, request, format='mp4'):
        name = self.get_file_name('files')
        with open(name, 'wb+') as w:
            for part in request.FILES['file'].chunks():
                w.write(part)
        res = OdConfig.model.detect_vid(name)
        os.remove(name)
        return JsonResponse({'object' : res})

class ObjectDetectionPic(APIView):
    permission_classes = []
    parser_classes = (MultiPartParser, )

    def get_file_name(self, path):
        while True:
            name = f"{datetime.now().strftime('%m-%d-%Y')}_{rand_name()}.png"
            if not os.path.exists(os.path.join(path, name)):
                return os.path.join(path, name)

    def post(self, request, format='png'):
        name = self.get_file_name('files')
        with open(name, 'wb+') as w:
            for part in request.FILES['file'].chunks():
                w.write(part)
        res = OdConfig.model.detect_pic(name)
        os.remove(name)
        return JsonResponse({'object' : res})