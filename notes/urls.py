from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='notes_home'),
]