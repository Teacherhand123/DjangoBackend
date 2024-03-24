import json
import hashlib
import os

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from .models import userInformation, userChatInformation

from .emailSending import sendingBy163

current_directory = os.path.dirname(os.path.abspath(__file__))
userTokenJsonPath = current_directory + "/userJsonData/userToken.json"
registerJsonPath = current_directory + "/userJsonData/email.json"

# Create your views here.


def verifyLoginTime(request):
    if request.method == "POST":
        postJson = json.loads(request.body.decode())
        f = open(userTokenJsonPath)
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
            data = json.loads(serializers.serialize("json", userChatInformation.objects.filter(username=postJson["username"])))
            # check if the same password
            if data[0]["fields"]["password"] == postJson["password"]:

                # dm5 encode to token
                dm5Encode = hashlib.md5(postJson["password"].encode()).hexdigest()

                f = open(userTokenJsonPath)
                tempStr = f.read()
                f.close()
                userTokens = json.loads(tempStr)

                isNull = True
                # check if username has existed
                for userData in userTokens:
                    if userData["username"] == postJson["username"]:
                        isNull = False
                        userData["token"] = dm5Encode

                if isNull:
                    userTokens.append({"username": postJson["username"],
                                      "token": dm5Encode})

                # write into .json
                newTempStr = json.dumps(userTokens)

                listTempStr = list(newTempStr)

                for index in range(len(listTempStr)):
                    if listTempStr[index] == ',':
                        listTempStr[index] = ',\n'

                newTempStr = ''.join(listTempStr)

                f = open(userTokenJsonPath, 'w')
                f.write(newTempStr)
                f.close()

                return JsonResponse({"error": "false", "userlogintoken": dm5Encode, "description": "None"}, safe=False)
        except:
            return JsonResponse({"error": "true", "description": "this user does not exist"}, safe=False)
    return JsonResponse({"error": "true", "description": "username or password error"}, safe=False)


def createNewUser(request):
    if request.method == "POST":
        postJson = json.loads(request.body.decode())
        print(postJson)

        # read emailJson
        f = open(registerJsonPath)
        tempStr = f.read()
        f.close()
        emailJson = json.loads(tempStr)

        correctInformation = False

        cancelIndex = -1

        for index in range(len(emailJson)):
            if postJson["emailcode"] == emailJson[index]["code"] and emailJson[index]["code"] != "-1":
                cancelIndex = index
                correctInformation = True
                break

        if correctInformation:
            userChatInformation.objects.create(username=postJson["username"], password=postJson["password"], email=postJson["email"])

            emailJson[cancelIndex]["code"] = "-1"

            tempStr = json.dumps(emailJson)
            tempStrList = list(tempStr)

            for index in range(len(tempStrList)):
                if tempStrList[index] == '}':
                    tempStrList[index] = '}\n'

            f = open(registerJsonPath, 'w')
            f.write('')
            f.close()

            with open(registerJsonPath, 'a') as f:
                f.writelines(tempStrList)

            return JsonResponse({"error": "false", "description": "register success"}, safe=False)

        return JsonResponse({"error": "true", "description": "email code error"}, safe=False)

    return JsonResponse({"error": "true", "description": "none"}, safe=False)


def emailVerifiCode(request):
    if request.method == "POST":
        postJson = json.loads(request.body.decode())
        postEmail = postJson["email"]
        # wait for response
        resp = sendingBy163(postEmail)
        return JsonResponse(resp, safe=False)
    return HttpResponse.status_code(500)
