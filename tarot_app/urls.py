from django.urls import path
from . import views
from .geminiapi import process_result


urlpatterns = [
    path('process/', views.process, name='process'),
    path('', views.index, name='index'),
    path('send_result/', views.send_result, name='send_result'),
    path('process_result/', process_result, name='process_result')
]
