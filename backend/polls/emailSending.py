import smtplib
import random
from email.header import Header
from email.mime.text import MIMEText

sender = 'testdjango2024@163.com'
passWrd = 'ZNVOHWZOJGMTJSTK'

smtpServer = 'smtp.136.com'

head = 'From Chat Web Register'


def sendingBy163(toSended):
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

    server = smtplib.SMTP_SSL('smtp.163.com', 465)

    server.login(sender, passWrd)
    server.sendmail(sender, toSended, msg.as_string())

