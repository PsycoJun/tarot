from django.urls import path
from . import views
from .geminiapi import process_result

urlpatterns = [
    path('', views.index, name='index'),
    path('send_result/', process_result, name='process_result'),
    
]
