import json
import datetime

from urllib.request import Request, urlopen
from urllib.parse import quote  # utf-8

class NaverApi:
    def getRequestUrl(self, url):
        requestUrl = Request(url)

        requestUrl.add_header('X-Naver-Client-ID','_Zgd7DjzVM9oRwOEi2Ro')
        requestUrl.add_header('X-Naver-Client-Secret', 'IV7LzYz4_i')

        try:
            result = urlopen(requestUrl)  # 요청 결과가 반환

            if result.getcode() == 200:  # 응답결과가 정상
                print(f"네이버 api 요청 응답 정상 진행-[{datetime.datetime.now()}]")
                return result.read().decode('utf-8')  # utf-8 디코딩해서 반환
            else:
                print(f"네이버 api 요청 응답 실패-[{datetime.datetime.now()}]")
                return None
        except Exception as e:
            print(f"에러 발생 : {e}")
            return None

    def naverSearch(self, node, searchKeyword, start, display):
        baseUrl = "https://openapi.naver.com/v1/search"  # 기본 url
        node = f"/{node}.json"
        params = f"?query={quote(searchKeyword)}&start={start}&display={display}"

        url = baseUrl+node+params  # 네이버에 요청할 전체 url

        resultData = self.getRequestUrl(url)
        # 만들어진 전체 url을 인수로 getRequestUrl함수를 호출하면 결과 도착

        if resultData != None:  # 조건이 참이면 정상 응답 받음
            return json.loads(resultData)  # json 형태로 변환하여 반환
        else:
            print("네이버 응답 실패!!")
            return None