import requests
import sys
import io
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import telegram
from selenium import webdriver
from  apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler


from telegram.ext import MessageHandler, Filters
# 메세지에 버튼 추가 클래스
from telegram import ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler

import re
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



# 요약 url (smodin)
smodinURL = "https://smodin.io/ko/%E1%84%90%E1%85%A6%E1%86%A8%E1%84%89%E1%85%B3%E1%84%90%E1%85%B3%E1%84%8B%E1%85%AD%E1%84%8B%E1%85%A3%E1%86%A8%E1%84%80%E1%85%B5"
xpath_text =  '//*[@id="__next"]/div/div[2]/div[1]/div/div/div[2]/textarea'
xpath_button =  '//*[@id="__next"]/div/div[2]/div[1]/div/div/div[5]/button[1]/span[1]'
smodinKeywoad = ""

# driver = webdriver.Chrome()
# driver.get(smodinURL)

# URL, BeautifulSoup
url = "http://www.tukorea.ac.kr/front/boardlist.do?bbsConfigFK=1&siteGubun=14&menuGubun=1"
# url = "http://www.tukorea.ac.kr/front/boardlist.do?bbsConfigFK=8&siteGubun=14&menuGubun=1"
html = urllib.request.urlopen(url).read()
bsObject = BeautifulSoup(html, "html.parser")

# 링크를 확인한다.
href_list = bsObject.select("a.subject")

notice_list = []
keyword_search_list = []



class Notice:
    def __init__(self, number, href, notice_text = 'None'):
        self.href = href
        self.notice_text = notice_text
        self.visible = True
    def show(self):
        if self.visible:
            print( self.notice_text, " " ,self.href)


def create_notice_list():
    html = urllib.request.urlopen(url).read()
    bsObject = BeautifulSoup(html, "html.parser")

    # 링크를 확인한다.
    href_list = bsObject.select("a.subject")
    notice_list.clear()
    for href in href_list:
        n = Notice(0, "www.tukorea.ac.kr" + str(href.attrs['href']).replace('\n', ""))
        notice_list.append(n)
    count = 0
    # 공지 제목 텍스트 넣기
    for span in bsObject.find_all('span', {'class': 'text'}):
        # print(span.text)
        text = str(span.text)
        text = text.replace('[','<')
        text = text.replace(']','>')
        notice_list[count].notice_text = text.strip()
        count += 1

    # for n in notice_list:
    #     n.show()
    #     print("\n")


# 키워드 관련 새로운 공지사항이 있는지 확인
def check_new_notice():
    if not isAlarm:
        return
    nowHtml = urllib.request.urlopen(url).read()
    bsObj = BeautifulSoup(nowHtml, "html.parser")
    h_list = bsObj.select("a.subject")
    new_notice_list = []
    # new_notice_list 에 일단 다 넣는다.

    new_notice = Notice(0,'')
    for href in h_list:
        n = Notice(0,"www.tukorea.ac.kr" + str(href.attrs['href']).replace('\n', ""))
        new_notice_list.append(n)
        # print("www.tukorea.ac.kr" + href.attrs['href'])
    count = 0
    for span in bsObj.find_all('span', {'class': 'text'}):
        # print(span.text)
        text = str(span.text)
        text = text.replace('[', '<')
        text = text.replace(']', '>')
        new_notice_list[count].notice_text = text.strip()
        if text.strip().find(nowKeyword) != -1 and new_notice.notice_text == 'None':
            print(new_notice.notice_text)
            new_notice = new_notice_list[count]
        count += 1
    # new_notice_list에 넣은 후에 원본이랑 비교 해보고 중복이면 삭제한다.
    print(new_notice.notice_text)
    for li in notice_list:
        if li.notice_text == new_notice.notice_text:
            new_notice.notice_text = 'None'

    if new_notice.notice_text != 'None':
        now = time.localtime()
        nowTime = "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        text = "설정된 키워드 \'" + nowKeyword + "\'에 대한 새로운 공지사항이 올라왔습니다. \n" + '[' + new_notice.notice_text + '](' + new_notice.href + ')' + '\n' + nowTime
        bot.send_message(
            chat_id=id,
            text=text,
            parse_mode = 'Markdown')
    create_notice_list()

# 공지사항 스크랩
def notice_scraping():
    # 일단 학사공지만 스크랩
    pass

# 키워드 검색 실행시에 사용한다.
def search_keyword():
    create_notice_list()
    for li in notice_list:
        if li.notice_text.find(nowKeyword) != -1:
            # print(li.notice_text, "--" , nowKeyword)
            keyword_search_list.append(li)

def show_search_result(id, update, context):
    for li in keyword_search_list:
        text = '[' + li.notice_text + '](' + li.href + ')'
        # text_compress(li.href)
        # print(text)
        context.bot.send_message(
            chat_id=id,
            text=text,
            parse_mode = 'Markdown')
    keyword_search_list.clear()

def text_compress(href):
    nowHtml = urllib.request.urlopen("https://" + href).read()
    bsObj = BeautifulSoup(nowHtml, "html.parser")
    text = ""
    for span in bsObj.find_all('p'):
        text += span.text
    # 텍스트 입력, 클릭
    # driver.find_element(xpath_text).send_keys(text)
    # driver.find_element(xpath_button).click()

def cmd_task_buttons(update, context):
    task_buttons = [[
        InlineKeyboardButton('1. 키워드 등록', callback_data=1),
        InlineKeyboardButton('2. 키워드 검색', callback_data=2),

    ],
    [
        InlineKeyboardButton('3. 키워드 초기화', callback_data=3),
        InlineKeyboardButton('4. 키워드 알림 on/off', callback_data=4)
    ]]

    reply_markup = InlineKeyboardMarkup(task_buttons)

    context.bot.send_message(
        chat_id=update.message.chat_id
        , text='안녕하세요! 이누공에서 수행할 작업을 선택해주세요.'
        , reply_markup = reply_markup
    )

def cb_button(update, context):
    global isKeyword
    global nowKeyword
    global isAlarm
    query = update.callback_query
    data = query.data

    context.bot.send_chat_action(
        chat_id = update.effective_user.id
        , action=ChatAction.TYPING
    )
    # 전체 출력코드
    # text=""
    # for span in bsObject.find_all('span', {'class': 'text'}):
    #     text += span.text + "\n"

    # 키워드 추가
    if data == '1':
        isKeyword = True
        context.bot.send_message(
            chat_id=query.message.chat_id
            , text='사용할 키워드를 등록하세요.' )
    #  키워드 검색 후
    elif data == '2':
        search_keyword()
        show_search_result(id, update, context)
    elif data == '3':
        isKeyword = False
        if nowKeyword !='None':
            context.bot.send_message(
                chat_id=query.message.chat_id,
                text= '현재등록된 \'' + nowKeyword + '\' 키워드를 초기화 합니다.')
        else:
            context.bot.send_message(
                chat_id = query.message.chat_id
                ,text='현재등록된 키워드가 없습니다.')
        nowKeyword = 'None'
    elif data == '4':
        if isAlarm:
            text = "키워드 알림 받기를 해제하였습니다."
        elif not isAlarm:
            text = "키워드 알림 받기를 설정하였습니다."
        isAlarm = not isAlarm
        context.bot.send_message(
            chat_id=query.message.chat_id
            , text=text)

    # else:
    #     context.bot.edit_message_text(
    #         text=text
    #         ,chat_id = query.message.chat_id
    #         ,message_id=query.message.message_id)

def get_message(update, context):
    global isKeyword
    global nowKeyword
    if isKeyword:
        nowKeyword = update.message.text
        update.message.reply_text('키워드 \'' + nowKeyword + '\' 을/를 등록합니다.')
        isKeyword = False

create_notice_list()
# 키워드 입력을 받는다.
isKeyword = False
nowKeyword = 'None'
keywordNumber = 0
isAlarm = False

# 스케줄러 생성
sched = BackgroundScheduler(timezone='Asia/Seoul')
sched.add_job(check_new_notice, 'interval', seconds=30)
sched.start()

token = '5317344801:AAFAj8o9n4kAgdfDB4FHmwLs9VsOljKQYwE'
id = '5392549181'
# id = '452569916'

bot = telegram.Bot(token = token)

updater = Updater(token = token, use_context=True)
dispatcher = updater.dispatcher

task_buttons_handler = CommandHandler('ask', cmd_task_buttons)
button_callback_handler = CallbackQueryHandler(cb_button)
message_handler = MessageHandler(Filters.text, get_message)

dispatcher.add_handler(task_buttons_handler)
dispatcher.add_handler(button_callback_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()
updater.idle()



