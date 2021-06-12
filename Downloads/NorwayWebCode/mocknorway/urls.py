from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('message/', views.message, name='message'),
    path('image/', views.image, name='image'),
    path('historical008/', views.historical008, name='historical008'),
    path('historical008/histview008/', views.histview008, name='histview008'),
    path('historical009/', views.historical009, name='historical009'),
    path('historical009/histview009/', views.histview009, name='histview009'),
    path('traveltime/', views.traveltime, name='traveltime'),
    path('traveltime/travelview/', views.travelview, name='travelview')
]

