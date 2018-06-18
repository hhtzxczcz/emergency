# -*- coding: cp949 -*-
import base64
import smtplib
import codecs
from xml.dom.minidom import *
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

def Base64_Encode(s):
    return base64.b64encode(s.encode('utf-8'))

def Base64_Decode(b):
    return base64.b64decode(b).decode('utf-8')

def SendEmail(data, ReviceMail):
    open('data.xml', 'rt', encoding='utf8')
    s = smtplib.SMTP("smtp.gmail.com",587)
    s.starttls()

    s.login( Base64_Decode("YW5reW9uZzk5QGdtYWlsLmNvbQ=="),Base64_Decode("YW5reW9uZzk="))
    contents = "기관 이름   : " + data.dutyname.string + chr(10)
    contents += "기관 주소  : " + data.dutyaddr.string + chr(10)
    contents += "기관 분류  : " + data.dutyemclsname.string + chr(10)
    contents += "분류 코드  : " + data.dutyemcls.string + chr(10)
    contents += "대표 전화  : " + data.dutytel1.string + chr(10)

    try:
        contents += "응급 전화  : " + data.dutytel3.string + chr(10)
    except:
        pass

    msg = MIMEText(contents, _charset='euc-kr')
    msg['Subject'] = data.dutyname.string
    msg['From'] = Base64_Decode("YW5reW9uZzk5QGdtYWlsLmNvbQ==")
    msg['To'] = ReviceMail
    s.sendmail( Base64_Decode("YW5reW9uZzk5QGdtYWlsLmNvbQ==") , ReviceMail, msg.as_string())