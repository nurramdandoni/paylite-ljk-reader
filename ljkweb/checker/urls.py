from django.urls import path
from . import views

urlpatterns = [
    path('proses/', views.proses, name='proses'),
]