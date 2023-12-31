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
        self.input_keyword.returnPressed.connect(self.searchBtnclicked) # Enter 쳐도 Button Click 과 동일하게 작동
        self.result_table.doubleClicked.connect(self.resultDoubleClicked)

    def searchBtnclicked(self):
        searchKeyword = self.input_keyword.text() # 입력 Keyword 가져옴
        if searchKeyword == '' : #검색어를 입력하디 않았을때
            QMessageBox.warning(self,'경고!!!','검색어를 입력해 주세요!!!')
        else :

            naverApi = NaverApi() # Naver Api class 생성
            searchResult = naverApi.naverSearch("news", searchKeyword, 1, 50)
            # print(searchResult)

            #QTableWidget ( result_table ) 에 결과 Display (items만)
            items = searchResult['items']
            self.outputResult(items)

    def resultDoubleClicked(self): # Table내 검색 걀과 Double Click시 호출
        selectRowNum = self.result_table.currentRow() # 현재 선택된 행 번호 반횐
        newsUrl = self.result_table.item(selectRowNum,1).text() #기사중 Link 만 추출
        # print(newsUrl)
        webbrowser.open(newsUrl)

    def outputResult(self,items):
        self.result_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.result_table.setColumnCount(2) # 출력 Table 의 열 갯수
        self.result_table.setRowCount(len(items))# 출력 Table 의 행 갯수 (Items갯수)
        self.result_table.setHorizontalHeaderLabels(['기사 제목','기사 링크'])
        self.result_table.setColumnWidth(0,400) # 첫 열의 넙이
        self.result_table.setColumnWidth(1, 221) # 두번째 열의 넙이
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers) # Table 내용수정금지

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