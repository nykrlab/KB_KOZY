# -*- encoding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

import requests
from bs4 import BeautifulSoup
import random
# from . forms import CustomUserChangeForm

# def login_view(request):
#     form = AuthenticationForm(request, request.POST)
#     msg = None
    
#     # 이미 로그인된 상태 > 메인으로
#     if request.user.is_authenticated:
#         return redirect('main:main')

#     # msg = None

#     if request.method == "POST":
#         if form.is_valid():
#             # auth_login(request, form.get_user())           
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password")
#             user = authenticate(username=username, password=password)
            
#             if user is not None:
#                 # login(request, user)
#                 auth_login(request, form.get_user())
#                 return redirect("main:main")
#             else:
#                 msg = 'Invalid credentials'
#         else:
#             msg = 'Error validating the form'

#     context = {
#         'form':form,
#     }
#     # return render(request, 'login.html', context)
#     return render(request, "login.html", {"form": form, "msg": msg})


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['user_id'] = user.username

                category=[
                '기획/아이디어',
                '광고/마케팅',
                '논문/리포트',
                '영상/UCC/사진',
                '디자인/캐릭터/웹툰',
                '웹/모바일/IT',
                '게임/소프트웨어',
                '과학/공학',
                '문학/글/시나리오',
                '건축/건설/인테리어',
                '네이밍/슬로건',
                '예체능/미술/음악',
                '대외활동/서포터즈',
                '봉사활동',
                '취업/창업',
                '해외',
                '기타'
                ]

                category2={
                1:'기획/아이디어',
                10:'영상/UCC/사진', 
                21:'게임/소프트웨어', 
                27:'대외활동/서포터즈', 
                89:'봉사활동', 
                88:'취업/창업'
                }

                #공모전
                url2="https://www.wevity.com/?c=find"
                response = requests.get(url2)
                if response.status_code==200:
                    html=response.text
                    soup=BeautifulSoup(html,'html.parser')
                    finds = soup.select('#container > div.content-area > div.content-wrap > div.content > div:nth-child(4) > div > ul > li')
                    finds2 = soup.select('#container > div.content-area > div.content-wrap > div.content > div:nth-child(4) > div > ul > li > div:nth-child(2)')
                    finds3 = soup.select('#container > div.content-area > div.content-wrap > div.content > div:nth-child(4) > div > ul > li > div:nth-child(3)')
                    title=[] #제목
                    subtitle=[] #부제목
                    organ=[] #주최기관
                    day=[] #남은 요일
                    for find in finds[1:]:
                        title.append(find.div.a.text)
                        subtitle.append(find.div.div.text)
                    for find2 in finds2[1:]:
                        organ.append(find2.text)
                    for find3 in finds3[1:]:
                        day.append(find3.text.replace('접수중','').strip())
                else:
                    print(response.status_code)

                # 공모전 각 분야별 1페이지 15개 중 랜덤으로 1개씩 추천
                dict={}
                for i in category2:
                    dict[category2[i]]=[]
                    url_default='https://www.wevity.com/?c=find&s=1&gub=1&cidx='
                    url=url_default+str(i)
                    response = requests.get(url)
                    if response.status_code==200:
                        html=response.text
                        soup=BeautifulSoup(html,'html.parser')
                        actives1 = soup.select('#container > div.content-area > div.content-wrap > div.content > div:nth-child(4) > div > ul>li')

                        for active1 in actives1[1:]:
                            dict[category2[i]].append(url_default+active1.a['href'])
                    else:
                        print(response.status_code)

                reco_list = []
                for i,j in dict.items():
                    reco_list.append(j[random.randrange(15)])

                request.session['data'] = reco_list

                headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
                url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101"
                res = requests.get(url, headers=headers)
                res.raise_for_status()

                soup = BeautifulSoup(res.text, "lxml")

                news_title = soup.find_all("a", attrs = {"class" : "cluster_text_headline nclicks(cls_eco.clsart)"})
                ran_num = random.randint(0,len(news_title)-1)
                before_num = -1

                news = {}
                for i in range(5) : 
                    while(ran_num == before_num):
                        ran_num = random.randint(1,len(news_title))
                    str1 = news_title[ran_num].get_text()
                    news[str1] = news_title[ran_num]['href']
                    before_num = ran_num
                
                request.session['news'] = news
    
                context = {
                    'data':reco_list,
                    'news':news
                }
                return render(request, 'main.html', context)
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
    else:
        return render(request, 'accounts/login.html')

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            return redirect("/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})



# def register_user(request):
#     msg = None
#     success = False

#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get("username")
#             raw_password = form.cleaned_data.get("password")
#             user = authenticate(username=username, password=raw_password)

#             msg = 'User created - please <a href="/login">login</a>.'
#             success = True

#             # return redirect("/login/")

#         else:
#             msg = 'Form is not valid'
#     else:
#         form = SignUpForm()

#     return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

def logout(request):
    return redirect('/')
