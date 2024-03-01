import json
import hashlib
import os

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from .models import userInformation

current_directory = os.path.dirname(os.path.abspath(__file__))

# Create your views here.


def verifyLoginTime(request):
    if request.method == "POST":
        postJson = json.loads(request.body.decode())
        f = open(current_directory + "/userJsonData/userToken.json")
        tempStr = f.read()
        f.close()
        userTokens = json.loads(tempStr)

        userName = ''
        # check if username has existed
        for userData in userTokens:
            if userData["token"] == postJson["userLoginToken"]:
                userName = userData["username"]

        if userName == '':
            return JsonResponse({"error": "true"}, safe=False)

        return JsonResponse({"error": "false", "username": userName}, safe=False)

def verifyLogin(request):
    if request.method == "POST":
        postJson = json.loads(request.body.decode())
        try:
            data = json.loads(serializers.serialize("json", userInformation.objects.filter(username=postJson["username"])))
            # check if the same password
            if data[0]["fields"]["password"] == postJson["password"]:

                # dm5 encode to token
                dm5Encode = hashlib.md5(postJson["password"].encode()).hexdigest()

                f = open(current_directory + "/userJsonData/userToken.json")
                tempStr = f.read()
                f.close()
                userTokens = json.loads(tempStr)

                isNull = True
                # check if username has existed
                for userData in userTokens:
                    if userData["username"] == postJson["username"]:
                        print(userData)
                        isNull = False
                        userData["token"] = dm5Encode

                if isNull:
                    userTokens.append({"username": postJson["username"],
                                      "token": dm5Encode})

                # write into .json
                newTempStr = json.dumps(userTokens)
                f = open(current_directory + "/userJsonData/userToken.json", 'w')
                f.write(newTempStr)
                f.close()

                return JsonResponse({"error": "false", "userlogintoken": dm5Encode, "description": "None"}, safe=False)
        except:
            return JsonResponse({"error": "true", "description": "this user does not exist"}, safe=False)
    return JsonResponse({"error": "true", "description": "username or password error"}, safe=False)


def createNewUser(request):
    userInformation.objects.create(username="ComeFromDjangoAgain", password="123123Again")
    return HttpResponse("Django insert data to mysql!")
