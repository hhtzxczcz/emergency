#!/usr/bin/python
# coding=utf-8

import time
import sqlite3
import telepot
from pprint import pprint
from datetime import date, datetime

import noti

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        noti.sendMessage(user, row)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('출력'):
        print('try to 출력')
        for location in data.find_all("item"):
            text = "이름 : " + location.dutyname.string + chr(10)
            text += "주소 : " + location.dutyaddr.string + chr(10)
            text += "분류 : " + location.dutyemclsname.string + chr(10)
            text += "대표전화 : " + location.dutytel1.string + chr(10)
            try:
                text += "응급전화 : " + location.dutytel3.string + chr(10)
            except:
                pass
            noti.sendMessage(chat_id, text)
            print(text)
            print("")
    elif text.startswith('주소')  and len(args)>1:
        print('try to 주소검색', args[1])
        for location in data.find_all("item"):
            if args[1] in location.dutyaddr.string:
                text = "이름 : " + location.dutyname.string + chr(10)
                text += "주소 : " + location.dutyaddr.string + chr(10)
                text += "분류 : " + location.dutyemclsname.string + chr(10)
                text += "대표전화 : " + location.dutytel1.string + chr(10)
                try:
                    text += "응급전화 : " + location.dutytel3.string + chr(10)
                except:
                    pass
                noti.sendMessage(chat_id, text)
                print(text)
                print("")
    elif text.startswith('이름') and len(args) > 1:
        print('try to 이름검색', args[1])
        for location in data.find_all("item"):
            if args[1] in location.dutyname.string:
                text = "이름 : " + location.dutyname.string + chr(10)
                text += "주소 : " + location.dutyaddr.string + chr(10)
                text += "분류 : " + location.dutyemclsname.string + chr(10)
                text += "대표전화 : " + location.dutytel1.string + chr(10)
                try:
                    text += "응급전화 : " + location.dutytel3.string + chr(10)
                except:
                    pass
                noti.sendMessage(chat_id, text)
                print(text)
                print("")
    elif text.startswith('확인'):
        print('try to 확인')
        check( chat_id )
    else:
        noti.sendMessage(chat_id, """모르는 명령어입니다.\n출력 \n이름 [기관이름] \n주소 [기관주소] \n확인 중 하나의 명령을 입력하세요.\n     이름 의료법인 or 주소 시흥시 등등 """)


today = date.today()
current_month = today.strftime('%Y%m')
data = noti.LoadXMLFromFile()
print( '[', today,']received token :', noti.TOKEN)

bot = telepot.Bot(noti.TOKEN)
pprint( bot.getMe() )

bot.message_loop(handle)

print('Listening...')

while 1:
  time.sleep(10)