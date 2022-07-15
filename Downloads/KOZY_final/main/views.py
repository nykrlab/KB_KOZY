from django.shortcuts import render, redirect
from django.http import JsonResponse
import pyttsx3
from . models import Bookmark 
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import random
import warnings
warnings.filterwarnings('ignore')

def main(request):
    context = {
        'data':request.session['data'],
        'news':request.session['news']
    }
    return render(request, 'main.html', context)

def conversation(request):
    return render(request, 'chat.html')

def chat(request):
    input_val = request.GET.get('req')

    if '안녕' in input_val:
        context = {
            'ans': '안녕하세요',
        }
    elif '금융 상품 추천' in input_val or '금융상품 추천' in input_val:
        context = {
            'ans': '금융 상품을 추천받고 싶으시면 "30만 원, 6개월"과 같이 말씀해 주세요',
        }
    elif ('만 원' in input_val or '만원' in input_val) and '개월' in input_val:
        info =  re.findall(r'\d+', input_val)
        # 크롬 브라우저 드라이버 설정
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        # driver = webdriver.Chrome("C:\PD\chromedriver.exe", chrome_options=options)
        driver = webdriver.Chrome(
            "Users/nykr/Downloads/chromedriver", chrome_options=options)
        # url 접속
        url = "https://portal.kfb.or.kr/compare/receiving_neosearch.php"
        driver.get(url)
        time.sleep(1)
        # 페이지 정보 받아오기
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # 정보 선택 및 입력
        driver.find_element_by_id("Bankselect8").click()
        driver.find_element_by_id("SaveMoney").send_keys(info[0] + '0000')
        if int(info[1]) >= 6 and int(info[1]) < 12:
            driver.find_element_by_id("InterestMonth1").click()
        elif int(info[1]) >= 12 and int(info[1]) < 24:
            driver.find_element_by_id("InterestMonth2").click()
        elif int(info[1]) >= 24 and int(info[1]) < 36:
            driver.find_element_by_id("InterestMonth3").click()
        elif int(info[1]) >= 36:
            driver.find_element_by_id("InterestMonth4").click()
        driver.find_element_by_id("JOIN_LIMIT_CODE1").click()
        driver.find_element_by_id("InterestType1").click()
        driver.find_element_by_id("JOIN_METHOD1").click()
        # 검색 버튼 클릭
        x_path='//*[@id="Content"]/div[3]/div[1]/form/div[3]/span/a'
        cursor = driver.find_element_by_xpath(x_path)
        cursor.click()
        # 검색 결과 나온 테이블 정보 가져오기
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # 상품명 리스트로 저장
        date_selector = '#SearchResult > div:nth-child(4) > table > tbody > tr:nth-child(even) > td:nth-child(2) > a'
        dates = soup.select(date_selector)
        context = {
            'ans': '"' + dates[random.randrange(len(dates))].text + '" 을 추천할게요',
        }
    elif '메인' in input_val and '돌아가' in input_val:
        context = {
            'ans':'kozy_return',
        }
    elif '마이페이지' in input_val:
        context = {
            'ans': 'mypage_return',
        }
    elif '북마크' in input_val:
        context = {
            'ans': 'bookmark_return',
        }
    else:
        context = {
            'ans': '무슨 말인지 모르겠어요',
        }
         
    if 'return' not in context['ans']:
        obj = pyttsx3.init()
        obj.say(context['ans'])
        obj.runAndWait()
    return JsonResponse(context)

def register(request):
    content = request.GET.get('content')

    Bookmark.objects.create(content=content, user_id=request.session['user_id'])