from django.urls import path
from . import handler

urlpatterns = [
    path('', handler.temp_home),
    path('api/test/', handler.json_test),
]