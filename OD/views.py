from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

from .apps import OdConfig

import os, json, base64
from random import sample
from string import digits, ascii_uppercase, ascii_lowercase
from datetime import datetime

def rand_name():
    chars = ascii_lowercase + ascii_uppercase + digits
    return ''.join(sample(chars, 8))

class ObjectDetectionVideo(APIView):
    parser_classes = (FileUploadParser,)

    def get_file_name(self, path):
        while True:
            name = f"{datetime.now().strftime('%m-%d-%Y')}_{rand_name()}.mp4"
            if not os.path.exists(os.path.join(path, name)):
                return os.path.join(path, name)

    def post(self, request):
        if request.method == 'POST':
            data = json.loads(request.body)
            name = self.get_file_name('files')
            with open(name, 'wb+') as video:
                video.write(bytes(base64.b64decode(data['video'])))
            res = OdConfig.model.detect_vid(name)
            os.remove(name)
            return JsonResponse({'object' : res})
    
    def put(self, request, filename, format='mp4'):
        up_file = request.FILES['file']
        name = self.get_file_name('files')
        destination = open(name, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
        destination.close()
        res = OdConfig.model.detect_vid(name)
        return JsonResponse({'object' : res})