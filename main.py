import requests
from bs4 import BeautifulSoup


url = 'http://www.tukorea.ac.kr/contents/main/cor/noticehaksa.html'
response = requests.get(url)

print(response) # 응답 형식은 <Response [200]>
print(response.status_code) # 응답 코드는 200 (정상 응답)
print(response.text)    # 응답 내용 출력 (html, 엄청 긺)