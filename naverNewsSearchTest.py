from naverApi import *  # 제작한 naverApi 모듈 불러오기

searchKeyword = input("뉴스 검색 키워드를 입력하세요 : ")

naverApi = NaverApi()  # import된 naverApi 모듈의 NaverApi 클래스로 객체 생성

node = "news"
display = 10  # 한번에 불러올 수 있는 검색결과의 수 (최대 100개)
start = 1  # 검색시작위치 1

result = naverApi.naverSearch(node, searchKeyword, start, display)

# print(result)

items = result['items']
# print(items)

def clearTitle(title):
    resultStr = title.replace('&quot','').replace('<b>','').replace('</b>','').replace(';','')
    return resultStr

for title in items:
    print(f"뉴스제목 : {clearTitle(title['title'])}")
    print(f"뉴스url : {title['originallink']}")
