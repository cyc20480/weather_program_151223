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