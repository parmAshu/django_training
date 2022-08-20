from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path( '',  views.homePageHandler, name="homePageHandler" ),
    path( 'hello', views.helloPageHandler, name="helloPageHandler" )
]