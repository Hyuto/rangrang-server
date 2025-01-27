from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from .apps import CdConfig

import os
from random import sample
from string import digits, ascii_uppercase, ascii_lowercase
from datetime import datetime

def rand_name(length = 8):
    """ Random string """
    chars = ascii_lowercase + ascii_uppercase + digits
    return ''.join(sample(chars, length))

class ColorDetectionVideo(APIView):
    permission_classes = []
    parser_classes = (MultiPartParser, )

    def get_file_name(self, path):
        """ Get file name for uploaded video """
        while True:
            name = f"{datetime.now().strftime('%m-%d-%Y')}_{rand_name()}.mp4"
            if not os.path.exists(os.path.join(path, name)):
                return os.path.join(path, name)

    def post(self, request, format='mp4'):
        """ Receive post video file and run detection """
        name = self.get_file_name('files')
        with open(name, 'wb+') as w:
            for part in request.FILES['file'].chunks():
                w.write(part)
        res = CdConfig.model.detect_vid(name)
        os.remove(name)
        return JsonResponse({'color' : res})

class ColorDetectionPic(APIView):
    permission_classes = []
    parser_classes = (MultiPartParser, )

    def get_file_name(self, path):
        """ Get file name for uploaded image """
        while True:
            name = f"{datetime.now().strftime('%m-%d-%Y')}_{rand_name()}.jpg"
            if not os.path.exists(os.path.join(path, name)):
                return os.path.join(path, name)

    def post(self, request, format='jpg'):
        """ Receive post image file and run detection """
        name = self.get_file_name('files')
        with open(name, 'wb+') as w:
            for part in request.FILES['file'].chunks():
                w.write(part)
        res = CdConfig.model.detect_pic(name)
        os.remove(name)
        return JsonResponse({'color' : res})