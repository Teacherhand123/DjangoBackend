import json
import smtplib
import random
from os import path
from os import makedirs
from email.header import Header
from email.mime.text import MIMEText

current_directory = path.dirname(path.abspath(__file__))
registerJsonPath = current_directory + '/userJsonData/email.json'

sender = 'testdjango2024@163.com'
passWrd = 'ZNVOHWZOJGMTJSTK'

smtpServer = 'smtp.136.com'

head = 'From Chat Web Register'


def sendingBy163(toSended):
    # check if registered
    emailJson = []
    notRegister = True

    if not path.exists(registerJsonPath):
        f = open(registerJsonPath, 'w')
        f.close()
    else:
        f = open(registerJsonPath, 'r')
        tempStr = f.read()
        f.close()
        emailJson = json.loads(tempStr)

    for item in emailJson:
        if item["email"] == toSended:
            notRegister = False
            break

    if not notRegister:
        return {"error": "true", "description": "has Register"}

    # email has not register
    code = ""
    for i in range(6):
        num = random.randint(0, 9)
        code += str(num)
    text = "your code is " + code

    # email message
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['From'] = Header('ChatTeam' + '<' + sender + '>')
    msg['To'] = Header(toSended)
    msg['Subject'] = Header(head)

    try:
        print('coming to login stmplib!')
        server = smtplib.SMTP_SSL('smtp.163.com', 465)

        server.login(sender, passWrd)
        server.sendmail(sender, toSended, msg.as_string())

        # write to register json
        emailJson.append({
            "email": toSended,
            "code": code
        })

        tempStr = json.dumps(emailJson)

        newTempStr = list(tempStr)

        for index in range(len(newTempStr)):
            if newTempStr[index] == ',':
                newTempStr[index] = ',\n'

        f = open(registerJsonPath, 'w')
        tempStr = ''.join(newTempStr)
        f.write(tempStr)
        f.close()

        print("has write json file")

        return {"error": "false", "description": "email register success"}
    except:
        return {"error": "true", "description": "register error"}
