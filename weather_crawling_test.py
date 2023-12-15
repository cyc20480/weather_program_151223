# beautifulsoup4 설치
# requests 설치

import requests

from bs4 import BeautifulSoup

weather_html = requests.get("https://search.naver.com/search.naver?query=한남동+날씨")
print(weather_html.text)

weather_soup = BeautifulSoup(weather_html.text, 'html.parser')

# 검색한 날씨 지역명
weather_area = weather_soup.find('h2',{'class':'title'}).text
print(weather_area)

# 현재온도
now_temperature = weather_soup.find('div',{'class':'temperature_text'}).text
now_temperature = now_temperature[6:].strip()  # 현재온도 5.2 에서 5.2도 값만 슬라이싱
print(now_temperature)

# 어제와의 날씨 비교
yesterday_temper = weather_soup.find('p',{'class':'summary'}).text
yesterday_temper = yesterday_temper[:14].strip()
print(yesterday_temper)

# 체감온도
sense_temper = weather_soup.find('dd',{'class':'desc'}).text
print(sense_temper)

# 미세먼지 정보
dust_info = weather_soup.select('ul.today_chart_list>li')
# print(dust_info)

dust1 = dust_info[0].find('span',{'class':'txt'}).text  # 보통미세먼지 정보
print(dust1)
dust2 = dust_info[1].find('span',{'class':'txt'}).text  # 초미세먼지 정보
print(dust2)
