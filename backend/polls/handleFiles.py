from os import path
from os import makedirs

import json
import datetime

current_directory = path.dirname(path.abspath(__file__))


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


def handleUploadFile(file, dirName, imgType):
    dirPath = current_directory + '/imgs/' + dirName
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


def writeChatJson(data):
    today = datetime.date.today()
    jsonFileName = today.strftime('%y%m%d') + 'chatData' + '.json'
    jsonFilePath = current_directory + "/jsonData/" + jsonFileName

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


def readChatJson():
    today = datetime.date.today()
    jsonFileName = today.strftime('%y%m%d') + 'chatData' + '.json'
    jsonFilePath = current_directory + "/jsonData/" + jsonFileName
    f = open(jsonFilePath, 'r')
    tempStr = f.read()
    f.close()
    chatJson = json.loads(tempStr)
    return chatJson
