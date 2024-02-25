from django.shortcuts import render
import os
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
import json
# Create your views here.
current_directory = os.path.dirname(os.path.abspath(__file__))


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def getCSRFToken(request):
    csrf_token = get_token(request)
    return JsonResponse({'token': csrf_token})


def chatDataProcessing(request):
    if request.method == "GET":
        f = open(current_directory + "/jsonData/chat.json")
        tempStr = f.read()
        f.close()
        chatJson = json.loads(tempStr)
        return JsonResponse(chatJson, safe=False)
    else:
        # request.body is bytes class
        # bytes to str
        postJson = json.loads(request.body.decode())
        print(postJson)

        # get chat json
        f = open(current_directory + "/jsonData/chat.json")
        tempStr = f.read()
        chatJson = json.loads(tempStr)
        f.close()

        # add new content
        chatJson.append(postJson[0])
        strChatData = json.dumps(chatJson)

        # write into file
        f = open(current_directory + "/jsonData/chat.json", 'w')
        f.write(strChatData)
        f.close()
        return HttpResponse("you use post method!")
