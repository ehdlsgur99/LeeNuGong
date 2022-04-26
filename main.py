import requests
import sys
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from bs4 import BeautifulSoup

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("이누공")
        self.setGeometry(300, 100, 800, 800)
        self.setWindowIcon(QIcon("icon.png"))

app = QApplication(sys.argv)

window = MyWindow()
window.show()

app.exec_()

url = "http://www.tukorea.ac.kr/front/boardlist.do?bbsConfigFK=1&siteGubun=14&menuGubun=1"
html = urllib.request.urlopen(url).read()
bsObject = BeautifulSoup(html, "html.parser")
for span in bsObject.find_all('span', {'class': 'text'}):
     print(span.text)

