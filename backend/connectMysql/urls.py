from django.urls import path

from . import views

urlpatterns = [
    path("checkusers", views.checkUser, name="checkAllUsers"),
    path("register", views.createNewUser, name="registerNewUsers"),
]
