from django.urls import path

from fate.views import index


urlpatterns = [
    path('', index),
]
