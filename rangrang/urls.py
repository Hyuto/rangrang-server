"""rangrang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from OD.views import ObjectDetectionVideo, ObjectDetectionPic
from CD.views import ColorDetectionVideo, ColorDetectionPic

urlpatterns = [
    # OD
    path('od-api/video/', ObjectDetectionVideo.as_view()),
    path('od-api/picture/', ObjectDetectionPic.as_view()),
    # CD
    path('cd-api/video/', ColorDetectionVideo.as_view()),
    path('cd-api/picture/', ColorDetectionPic.as_view()),
]
