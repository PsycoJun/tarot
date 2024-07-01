from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('send_result/', views.send_result, name='send_result'),
]
