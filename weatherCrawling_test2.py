# beautifulsoup4 설치
# requests 설치

# 외국도시 날씨 출력 기능 추가

import requests

from bs4 import BeautifulSoup

weather_html = requests.get("https://search.naver.com/search.naver?query=fdfasff+날씨")
print(weather_html.text)

weather_soup = BeautifulSoup(weather_html.text, 'html.parser')

try:
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
except:#외국도시 날씨 검색의 경우 미세먼지 정보에서 에러가 출력되므로 예외처리하여 외국날씨 크롤링 정보 출력
    try:
        weather_area = weather_soup.find('h2', {'class': 'title'}).text
        print(weather_area)

        now_temperature = weather_soup.find('div', {'class': 'temperature_text'}).text
        now_temperature = now_temperature[6:10].strip()
        print(now_temperature)

        # 외국도시의 경우 현재 날씨(ex 흐림, 맑음)
        today_weather_text = weather_soup.find('p', {'class': 'summary'}).text
        print(today_weather_text)
        today_weather = today_weather_text[:2]
        print(today_weather)

        # 체감온도
        sense_temper = today_weather_text[8:].strip()
        print(sense_temper)

        #외국도시는 미세먼지 정보 없음
        yesterday_temper = "정보없음"
        dust1 = "정보없음"
        dust2 = "정보없음"

    except:
        print("해당 지역의 날씨정보가 검색되지 않습니다.")