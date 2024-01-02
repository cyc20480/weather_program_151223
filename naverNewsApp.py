import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

from naverApi import *

import webbrowser

form_class = uic.loadUiType("ui/naverNewsSearchAppUi.ui")[0]

class NaverAppWin(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("네이버뉴스 검색 앱")
        self.setWindowIcon(QIcon("img/newspaper.png"))
        self.statusBar().showMessage("Naver News Application v1.0")

        self.searchBtn.clicked.connect(self.searchBtnclicked)

    def searchBtnclicked(self):
        searchKeyword = self.input_keyword.text() # 입력 Keyword 가져옴

        naverApi = NaverApi() # Naver Api class 생성
        searchResult = naverApi.naverSearch("news", searchKeyword, 1, 50)
        # print(searchResult)

        #QTableWidget ( result_table ) 에 결과 Display (items만)
        items = searchResult['items']
        self.outputResult(items)

    def outputResult(self,items):
        self.result_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.result_table.setColumnCount(2) # 출력 Table 의 열 갯수
        self.result_table.setRowCount(len(items))# 출력 Table 의 행 갯수 (Items갯수)
        self.result_table.setHorizontalHeaderLabels(['기사 제목','기사 링크'])
        self.result_table.setColumnWidth(0,400) # 첫 열의 넙이
        self.result_table.setColumnWidth(1, 221) # 두번째 열의 넙이

        for i, news in enumerate(items):    # item 과index를 같이 뺀다
            newsTitle = self.clearTitle(news['title'])
            newsLink = news['originallink']

            self.result_table.setItem(i, 0, QTableWidgetItem(newsTitle))
            self.result_table.setItem(i, 1, QTableWidgetItem(newsLink))
    def clearTitle(self,title): #불필요한 HTML Tag들 삭제
        resultStr = title.replace('&quot', '').replace('<b>', '').replace('</b>', '').replace(';', '')
        return resultStr


app = QApplication(sys.argv)
win = NaverAppWin()
win.show()
app.exec_()