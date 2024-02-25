from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json

from .models import userInformation


# Create your views here.


def checkUser(request):
    if request.method == "POST":
        postJson = json.loads(request.body.decode())
        try:
            data = json.loads(serializers.serialize("json", userInformation.objects.filter(username=postJson["username"])))
            # check if the same password
            if data[0]["fields"]["password"] == postJson["password"]:
                return HttpResponse("welcome")
        except:
            return HttpResponse(status=404)
    return HttpResponse("fail")


def createNewUser(request):
    userInformation.objects.create(username="ComeFromDjangoAgain", password="123123Again")
    return HttpResponse("Django insert data to mysql!")
