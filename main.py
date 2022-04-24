import requests
import sys
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup

app = QApplication(sys.argv)

window = QWidget()
window.show()

app.exec_()

url = 'http://www.tukorea.ac.kr/gopage/main/gonomalnotice.jsp?siteGubun=1&bbsConfigFK=357&pkid=195753&menuGubun=1'
response = requests.get(url)

print(response) # 응답 형식은 <Response [200]>
print(response.status_code) # 응답 코드는 200 (정상 응답)
print(response.text)    # 응답 내용 출력 (html, 엄청 긺)