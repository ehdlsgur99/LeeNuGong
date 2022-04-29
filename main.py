import requests
import sys
import io
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import telegram
from selenium import webdriver

from telegram.ext import MessageHandler, Filters
# 메세지에 버튼 추가 클래스
from telegram import ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler


# 스케줄
import schedule
import time
import datetime
import pytz

from bs4 import BeautifulSoup


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

url = "http://www.tukorea.ac.kr/front/boardlist.do?bbsConfigFK=1&siteGubun=14&menuGubun=1"
html = urllib.request.urlopen(url).read()
bsObject = BeautifulSoup(html, "html.parser")

# href_list = bsObject.find_all("div", class_="bbs list mt15 bt1")
href_list = bsObject.select("a.subject")

class Notice:
    def __init__(self, href, notice_text = 'None'):
        self.href = href
        self.notice_text = notice_text
    def show(self):
        print(self.notice_text, "\n" ,self.href)

notice_list = []

for href in href_list:
    n = Notice("www.tukorea.ac.kr" + href.attrs['href'])
    notice_list.append(n)
    # print("www.tukorea.ac.kr" + href.attrs['href'])

count = 0
for span in bsObject.find_all('span', {'class': 'text'}):
    # print(span.text)
    notice_list[count].notice_text = span.text
    count += 1
    # text += span.text + "\n"

for n in notice_list:
    n.show()
    print("\n\n")

#      ---------------------------------------------------------

token = '5317344801:AAFAj8o9n4kAgdfDB4FHmwLs9VsOljKQYwE'
id = '5392549181'

updater = Updater(token = token, use_context=True)
dispatcher = updater.dispatcher

# 공지사항 스크랩
def notice_scraping():
    # 일단 학사공지만 스크랩
    pass

def cmd_task_buttons(update, context):
    task_buttons = [[
        InlineKeyboardButton('1. 키워드 추가', callback_data=1),
        InlineKeyboardButton('2. 키워드 검색', callback_data=2),

    ],
    [
        InlineKeyboardButton('3. 키워드 초기화', callback_data=3),
        InlineKeyboardButton('4. 키워드 알림 on/off', callback_data=4)
    ],
    [
       InlineKeyboardButton('5. 취소', callback_data=5)
    ]]
    reply_markup = InlineKeyboardMarkup(task_buttons)

    context.bot.send_message(
        chat_id=update.message.chat_id
        , text='안녕하세요! 이누공에서 수행할 작업을 선택해주세요.'
        , reply_markup = reply_markup
    )

def cb_button(update, context):
    query = update.callback_query
    data = query.data

    context.bot.send_chat_action(
        chat_id = update.effective_user.id
        , action=ChatAction.TYPING
    )
    text=""
    for span in bsObject.find_all('span', {'class': 'text'}):
        text += span.text + "\n"

    context.bot.edit_message_text(
        text=text
        ,chat_id = query.message.chat_id
        ,message_id=query.message.message_id)


task_buttons_handler = CommandHandler('ask', cmd_task_buttons)
button_callback_handler = CallbackQueryHandler(cb_button)

dispatcher.add_handler(task_buttons_handler)
dispatcher.add_handler(button_callback_handler)

updater.start_polling()
updater.idle()

# def job():
#     global count
#     count += 1
#     now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
#     if now.hour >= 23 or now.hour <= 6:
#         return
#
#     sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
#     sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
#
#     token = '5317344801:AAFAj8o9n4kAgdfDB4FHmwLs9VsOljKQYwE'
#     bot = telegram.Bot(token = token)
#     BASE_URL = "http://www.tukorea.ac.kr/front/boardlist.do?bbsConfigFK=1&siteGubun=14&menuGubun=1"
#     chat_id = '5392549181'
#
#     with requests.Session() as s:
#         res = s.get(BASE_URL)
#         if res.status_code == requests.codes.ok:
#             soup = BeautifulSoup(res.text, 'html.parser')
#             article = soup.select_one('div.btn_choice_box.btn_restock_box > button')
#             cartExist = soup.select_one('#cartBtn')
#             wishBtn = soup.select_one('#wishBtn')
#
#             if article == None or cartExist or wishBtn:
#                 bot.sendMessage(chat_id=chat_id, text="구매 가능")
#             else:
#                 if count % 6 == 0:
#                     bot.sendMessage(chat_id=chat_id, text="품절 상태")
#                 else:
#                     print("60분에 1번만 알림 가도록 설정")
#
# # 10분 마다 실행
# schedule.every(10).minutes.do(job)
#
# print("Start App")
#
# # 파이선 스케줄러
# while True:
#     schedule.run_pending()
#     time.sleep(1)
