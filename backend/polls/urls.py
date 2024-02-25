from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("chatDataProcessing", views.chatDataProcessing, name="chatDataProcessing"),
    path("getCSRFToken", views.getCSRFToken, name="getCSRFToken"),
]
