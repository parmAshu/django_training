from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path( '', views.indexPageHandler ),
    path( 'upload', views.uploadPageHandler ),
    path( 'delete', views.deletePageHandler ),
    path( 'download', views.downloadFileHandler ),
    path( 'uploadFile', views.uploadFileHandler ),
    path( 'deleteFile', views.deleteFileHandler )
]
