from os import path
from os import makedirs
from pathlib import Path

import json
import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_IMG_ROOT = path.join(BASE_DIR, 'static/imgs/')
STATIC_CHATJSON_ROOT = path.join(BASE_DIR, 'static/jsonChatData/')

# count the pic amount
def readpicAmount(countPath):
    f = open(countPath, 'r')
    tempStr = f.read()
    strList = tempStr.split('=')
    f.close()

    count = strList[1]

    f = open(countPath, 'w')
    f.write('count=' + str(int(count) + 1))
    f.close()
    return count

# handle up img
def handleUploadFile(file, dirName, imgType):
    existsDir = path.exists(STATIC_IMG_ROOT)
    if not existsDir:
        makedirs(STATIC_IMG_ROOT)

    dirPath = STATIC_IMG_ROOT + '/' + dirName
    existsDir = path.exists(dirPath)
    if not existsDir:
        makedirs(dirPath)

    imgsMount = dirPath + '/' + dirName + '.txt'
    existsFile = path.exists(imgsMount)

    if not existsFile:
        f = open(imgsMount, 'w')
        f.write('count=0')
        f.close()

    imgName = str(readpicAmount(imgsMount))

    imgPath = dirPath + '/' + imgName + imgType
    with open(imgPath, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return imgName + imgType

# accept text from client
def writeChatJson(data):
    today = datetime.date.today()
    jsonFileName = today.strftime('%y%m%d') + 'chatData' + '.json'
    jsonFilePath = STATIC_CHATJSON_ROOT + '/' + jsonFileName

    if not path.exists(jsonFilePath):
        f = open(jsonFilePath, 'w')
        f.write('[]')
        f.close()

    # get chat json
    f = open(jsonFilePath, 'r')
    tempStr = f.read()
    chatJson = json.loads(tempStr)
    f.close()

    # add new content
    chatJson.append(data)

    strChatData = json.dumps(chatJson)

    strDataList = list(strChatData)
    for index in range(len(strDataList)):
        if strDataList[index] == '}':
            strDataList[index] = '}\n'

    strChatData = ''.join(strDataList)

    # write into file
    f = open(jsonFilePath, 'w')
    f.write(strChatData)
    f.close()


# Get data from chat json file
def readChatJson():
    today = datetime.date.today()
    jsonFileName = today.strftime('%y%m%d') + 'chatData' + '.json'
    jsonFilePath = STATIC_CHATJSON_ROOT + '/' + jsonFileName

    if not path.exists(STATIC_CHATJSON_ROOT):
        makedirs(STATIC_CHATJSON_ROOT)

    if not path.exists(jsonFilePath):
        f = open(jsonFilePath, 'w')
        f.write('[]')
        f.close()
        return []

    f = open(jsonFilePath, 'r')
    tempStr = f.read()
    f.close()
    chatJson = json.loads(tempStr)
    return chatJson
