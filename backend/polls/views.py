from django.shortcuts import render
from os import path
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
import json

from .handleFiles import handleUploadFile, writeChatJson, readChatJson

# Create your views here.
current_directory = path.dirname(path.abspath(__file__))


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def getCSRFToken(request):
    csrf_token = get_token(request)
    return JsonResponse({'token': csrf_token})


def chatDataProcessing(request):
    if request.method == "GET":
        chatJson = readChatJson()
        return JsonResponse(chatJson, safe=False)
    else:
        # request.body is bytes class
        # bytes to str
        postJson = json.loads(request.body.decode())
        print(postJson)
        # write the jsonFile
        writeChatJson(postJson[0])
        return HttpResponse("you use post method!")


def imgDataProcessing(request):
    if request.method == "POST":
        username = request.POST['username']
        imgType = '.' + request.POST['imgType']
        fileData = request.FILES[username + 'imgs']

        imgName = handleUploadFile(fileData, username, imgType)
        # will be change in server----------------------------------------------------
        textContent = 'http://localhost:3001/imgs/' + username + '/' + imgName

        data = {
            "username": username,
            "textContent": textContent,
            "textType": "img"
        }

        writeChatJson(data)

    return HttpResponse("hello")
