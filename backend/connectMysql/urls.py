from django.urls import path

from . import views

urlpatterns = [
    path("verifylogin", views.verifyLogin, name="checkAllUsers"),
    path("register", views.createNewUser, name="registerNewUsers"),
    path("verifylogintime", views.verifyLoginTime, name="verifyLoginTime"),
    path("emailverificode", views.emailVerifiCode, name="emailVerifiCode")
]
