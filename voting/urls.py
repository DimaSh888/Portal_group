from django.urls import path
from .views import poll_list


urlpatterns = [
    path('', poll_list, name='poll_list'),
]