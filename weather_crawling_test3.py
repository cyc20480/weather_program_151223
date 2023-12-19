# 네이버 날씨 크롤링 앱 v1.0

import sys
import requests
from bs4 import BeautifulSoup

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import Qt

import time
import threading

form_class = uic.loadUiType("ui/weatherUi.ui")[0]  # UI 불러오기

class WeatherWindow(QMainWindow, form_class):
    def __init__(self):  # 생성자
        super().__init__()  # 부모클래스의 생성자 호출
        self.setupUi(self)  # ui 호출

        self.setWindowTitle("오늘의 날씨")  # 프로그램 윈도우 제목
        self.setWindowIcon(QIcon("img/weather_icon.png"))  # 프로그램 아이콘 불러오기
        self.statusBar().showMessage("WEATHER APPLICATION V1.0")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)  # 윈도우를 항상 위로 유지

        self.weather_btn.clicked.connect(self.request_weather)  # 날씨조회 버튼 클릭->함수 연결
        self.weather_btn.clicked.connect(self.reflashTimer)  # 날씨조회 버튼 클릭->함수 연결

    def request_weather(self):
        weather_area = self.input_area.text()  # 프로그램 내 날씨입력창에서 입력된 지역이름 가져오기
        weather_html = requests.get(f"https://search.naver.com/search.naver?query={weather_area}+날씨")
        #print(weather_html.text)

        weather_soup = BeautifulSoup(weather_html.text, 'html.parser')

        try:
            # 검색한 날씨 지역명
            weather_area = weather_soup.find('h2', {'class': 'title'}).text
            #print(weather_area)

            # 오늘 날씨 텍스트(흐림, 맑음 등)
            today_weather = weather_soup.find('span', {'class': 'weather before_slash'}).text

            # 현재온도
            now_temperature = weather_soup.find('div', {'class': 'temperature_text'}).text
            now_temperature = now_temperature[6:].strip()  # 현재온도 5.2 에서 5.2도 값만 슬라이싱
            #print(now_temperature)

            # 어제와의 날씨 비교
            yesterday_temper = weather_soup.find('p', {'class': 'summary'}).text
            yesterday_temper = yesterday_temper[:14].strip()
            #print(yesterday_temper)

            # 체감온도
            sense_temper = weather_soup.find('dd', {'class': 'desc'}).text
            #print(sense_temper)

            # 미세먼지 정보
            dust_info = weather_soup.select('ul.today_chart_list>li')
            # print(dust_info)

            dust1 = dust_info[0].find('span', {'class': 'txt'}).text  # 보통미세먼지 정보
            #print(dust1)
            dust2 = dust_info[1].find('span', {'class': 'txt'}).text  # 초미세먼지 정보
            #print(dust2)

            self.area_label.setText(weather_area)  # 날씨 조회 지역 출력
            # self.weather_image.setText(today_weather)  # 오늘 날씨 텍스트 출력
            self.setWeatherImage(today_weather)  # 날씨 이미지 출력 함수 호출
            self.temper_label.setText(now_temperature)  # 현재온도 출력
            self.yesterday_label.setText(yesterday_temper)  # 어제와의 날씨 비교 텍스트 출력
            self.sensetemper_label.setText(sense_temper)  # 체감온도 출력
            self.dust01_info.setText(dust1)  # 미세먼지 정보 출력
            self.dust02_info.setText(dust2)  # 초미세먼지 정보 출력

        except:  # 외국도시 날씨 검색의 경우 미세먼지 정보에서 에러가 출력되므로 예외처리하여 외국날씨 크롤링 정보 출력
            try:
                weather_area = weather_soup.find('h2', {'class': 'title'}).text
                #print(weather_area)

                now_temperature = weather_soup.find('div', {'class': 'temperature_text'}).text
                now_temperature = now_temperature[6:8].strip()
                #print(now_temperature)

                # 외국도시의 경우 현재 날씨(ex 흐림, 맑음)
                today_weather_text = weather_soup.find('p', {'class': 'summary'}).text
                #print(today_weather_text)
                today_weather = today_weather_text[:2].strip()
                #print(today_weather)

                # 체감온도
                sense_temper = today_weather_text[8:].strip()
                #print(sense_temper)

                # 외국도시는 미세먼지 정보 없음
                yesterday_temper = ""
                dust1 = "-"
                dust2 = "-"

                self.area_label.setText(weather_area)  # 날씨 조회 지역 출력
                # self.weather_image.setText(today_weather)  # 오늘 날씨 텍스트 출력
                self.setWeatherImage(today_weather)  # 날씨 이미지 출력 함수 호출
                self.temper_label.setText(now_temperature)  # 현재온도 출력
                self.yesterday_label.setText(yesterday_temper)  # 어제와의 날씨 비교 텍스트 출력
                self.sensetemper_label.setText(sense_temper)  # 체감온도 출력
                self.dust01_info.setText(dust1)  # 미세먼지 정보 출력
                self.dust02_info.setText(dust2)  # 초미세먼지 정보 출력


            except:
                weather_area = "지역명 오류"
                # print("해당 지역의 날씨정보가 검색되지 않습니다.")
                self.area_label.setText(weather_area)  # 날씨 조회 지역 출력
                self.weather_image.setText("")  # 오늘 날씨 텍스트 출력
                self.temper_label.setText("")  # 현재온도 출력
                self.yesterday_label.setText("지역명을 다시 입력하세요.")  # 어제와의 날씨 비교 텍스트 출력
                self.sensetemper_label.setText("")  # 체감온도 출력
                self.dust01_info.setText("")  # 미세먼지 정보 출력
                self.dust02_info.setText("")  # 초미세먼지 정보 출력

    def setWeatherImage(self, weatherText):
        if weatherText == "맑음":
            weatherImg = QPixmap("img/sun.png")  # 맑음 이미지 불러오기
            self.weather_image.setPixmap(QPixmap(weatherImg))  # 해당 레이블 자리에 이미지가 출력
        elif weatherText == "흐림":
            weatherImg = QPixmap("img/cloud.png")  # 맑음 이미지 불러오기
            self.weather_image.setPixmap(QPixmap(weatherImg))  # 해당 레이블 자리에 이미지가 출력
        elif weatherText == "눈":
            weatherImg = QPixmap("img/snow.png")  # 맑음 이미지 불러오기
            self.weather_image.setPixmap(QPixmap(weatherImg))  # 해당 레이블 자리에 이미지가 출력
        elif weatherText == "비":
            weatherImg = QPixmap("img/rain.png")  # 맑음 이미지 불러오기
            self.weather_image.setPixmap(QPixmap(weatherImg))  # 해당 레이블 자리에 이미지가 출력
        elif weatherText == "소낙":
            weatherImg = QPixmap("img/rain.png")  # 맑음 이미지 불러오기
            self.weather_image.setPixmap(QPixmap(weatherImg))  # 해당 레이블 자리에 이미지가 출력
        elif weatherText == "구름많음":
            weatherImg = QPixmap("img/cloud.png")  # 맑음 이미지 불러오기
            self.weather_image.setPixmap(QPixmap(weatherImg))  # 해당 레이블 자리에 이미지가 출력
        else:
            self.weather_image.setText(weatherText)

    def reflashTimer(self):
        self.request_weather()  # 날씨 조회 함수 호출
        threading.Timer(30, self.reflashTimer).start()
        print("타이머 호출 확인")



app = QApplication(sys.argv)
win = WeatherWindow()
win.show()
app.exec_()
