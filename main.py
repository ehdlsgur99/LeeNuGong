import requests
import sys
import io
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import telegram
from selenium import webdriver
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
# 스케줄
import schedule
import time
import datetime
import pytz

from bs4 import BeautifulSoup

#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("이누공")
#         self.setGeometry(300, 100, 800, 800)
#         self.setWindowIcon(QIcon("icon.png"))
#
# app = QApplication(sys.argv)
#
# window = MyWindow()
# window.show()
#
# app.exec_()
#
# url = "http://www.tukorea.ac.kr/front/boardlist.do?bbsConfigFK=1&siteGubun=14&menuGubun=1"
# html = urllib.request.urlopen(url).read()
# bsObject = BeautifulSoup(html, "html.parser")
# for span in bsObject.find_all('span', {'class': 'text'}):
#      print(span.text)

token = '5317344801:AAFAj8o9n4kAgdfDB4FHmwLs9VsOljKQYwE'
id = '5392549181'

count = 1

def job():
    global count
    count += 1
    now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    if now.hour >= 23 or now.hour <= 6:
        return


    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')

    token = '5317344801:AAFAj8o9n4kAgdfDB4FHmwLs9VsOljKQYwE'
    bot = telegram.Bot(token = token)
    BASE_URL = "http://www.tukorea.ac.kr/front/boardlist.do?bbsConfigFK=1&siteGubun=14&menuGubun=1"
    chat_id = '5392549181'

    with requests.Session() as s:
        res = s.get(BASE_URL)
        if res.status_code == requests.codes.ok:
            soup = BeautifulSoup(res.text, 'html.parser')
            article = soup.select_one('div.btn_choice_box.btn_restock_box > button')
            cartExist = soup.select_one('#cartBtn')
            wishBtn = soup.select_one('#wishBtn')

            if article == None or cartExist or wishBtn:
                bot.sendMessage(chat_id=chat_id, text="구매 가능")
            else:
                if count % 6 == 0:
                    bot.sendMessage(chat_id=chat_id, text="품절 상태")
                else:
                    print("60분에 1번만 알림 가도록 설정")

# 10분 마다 실행
schedule.every(10).minutes.do(job)

print("Start App")

# 파이선 스케줄러
while True:
    schedule.run_pending()
    time.sleep(1)
