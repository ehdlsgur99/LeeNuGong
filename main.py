import requests
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from bs4 import BeautifulSoup

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("이누공")
        self.setGeometry(300, 300, 400, 400)
        self.setWindowIcon(QIcon("icon.png"))

app = QApplication(sys.argv)

window = MyWindow()
window.show()

app.exec_()

url = 'http://www.tukorea.ac.kr/gopage/main/gonomalnotice.jsp?siteGubun=1&bbsConfigFK=357&pkid=195753&menuGubun=1'
response = requests.get(url)

print(response) # 응답 형식은 <Response [200]>
print(response.status_code) # 응답 코드는 200 (정상 응답)
print(response.text)    # 응답 내용 출력 (html, 엄청 긺)