from flask import Flask, render_template, request, send_file, make_response, Response
from io import BytesIO
import flask
from flask.helpers import flash
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from selenium.webdriver import Chrome
from selenium import webdriver
import time
import json
import numpy as np
import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.common import exceptions
from datetime import date
from collections import Counter
import warnings
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from datetime import date
from soynlp.word import WordExtractor
from wordcloud import WordCloud
from soynlp.tokenizer import LTokenizer
from soynlp.word import WordExtractor
from soynlp.utils import DoublespaceLineCorpus
import plotly
import plotly.express as px
import random
import datetime
from jinja2 import Environment, FileSystemLoader
from flask import url_for
import socket
warnings.filterwarnings("ignore")
plt.rc('font', family='Malgun Gothic')

app = Flask(__name__)
app.config["SECRET_KEY"] = "EBS"
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

host = socket.gethostname()
ip_addr = socket.gethostbyname(host)

######메인화면
@app.route('/')

#초기화면
def main():
    return render_template("index.html")

######결과화면
@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        #입력 값 받기
        keyword = request.form['input1']
        num = int(request.form['input2'])

        create_html("", keyword, num)

    return render_template('index.html')


def create_html(pstr, pkeyword, pnum):
    
    with app.app_context(), app.test_request_context():
        jsurl1 = url_for('static', filename='css/index.css')
        jsurl2 = url_for('static', filename='icon.png')

    try:
        start = time.time()  
        if 'POST' == 'POST':
            # filePath = 'static\image'
            # for file in os.scandir(filePath):
            #     os.remove(file.path)

            #입력 값 받기
            # keyword = request.form['input1']
            # num = int(request.form['input2'])
            keyword = pkeyword
            num = pnum

            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("headless")
            driver = webdriver.Chrome("chromedriver", options=options)
            print("-------------시작--------------")

            # if num == 1 :
            #     url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=4&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:1d,a:all&start={}'
            #     num = '1일'
            if num == 1 :
                url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=2&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:1m,a:all&start={}'
                num = '1개월'
            elif num == 6 :
                url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=6&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:6m,a:all&start={}'
                num = '6개월'
            elif num == 7 :
                url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=1&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:1w,a:all&start={}'
                num = '7일'
            elif num == 12:
                url ='https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=5&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:1y,a:all&start={}'
                num = '1년'
            else:
                url ='https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=13&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:3m,a:all&start={}'
                num = "3개월"

            urlList = []
            i = 1
            x = 1

            #url 
            while True:
                try:
                    print(f"{x} Page 수집중..")
                    with open("./static/html/{0}/log.txt".format(pstr), "w", encoding='utf-8') as f:
                        f.write(f"\n{x} Page 수집중..")
                    driver.get(url.format(keyword,i))
                    i += 10 
                    x += 1
                    newsUrls = driver.find_elements_by_link_text('네이버뉴스')

                    for newsUrl in newsUrls:
                        tmp = newsUrl.get_attribute('href')
                        urlList.append(tmp)
                    driver.find_element_by_css_selector('a.btn_next')
                    time.sleep(1) #2초에서 1초로 수정
                except:
                    break
            driver.quit()

            print("==========url수집 완료==========")

            urlDf = pd.DataFrame({"url":urlList})

            dfList = []
            dfList1 = []

            for i in range(len(urlDf)):
                print(f"진행상황: {i+1} / {len(urlDf)}") #진행도 확인차
                with open("./static/html/{0}/log.txt".format(pstr), "w", encoding='utf-8') as f:
                    f.write(f"\n진행상황: {i+1} / {len(urlDf)}")
                driver = webdriver.Chrome("chromedriver", options=options)
                driver.get(urlDf["url"][i])
                time.sleep(0.5)
                
                #제목담기
                try:
                    title = driver.find_element_by_xpath('//*[@id="articleTitle"]').text #정치및 사회 기사
                except:
                    try:
                        title = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/h2').text #연애기사
                    except:
                        driver.quit()
                        continue #스포츠기사는 제외
                
                #본문담기
                try:
                    text = driver.find_element_by_xpath('//*[@id="articleBodyContents"]').text
                except:
                    try:
                        text = driver.find_element_by_xpath('//*[@id="articeBody"]').text
                    except:
                        continue 

                #언론사 정보 담기
                try:
                    press = driver.find_element_by_xpath('//*[@id="wrap"]/table/tbody/tr/td[2]/div/div[1]/h4/em').text
                except:
                    pass

                #댓글없으면 continue
                try:
                    driver.find_element_by_xpath('//*[@id="cbox_module"]/div[2]/div[9]/a').click()
                    time.sleep(2)
                except:
                    driver.quit()
                    continue

                while True:
                    try:
                        btn_more = driver.find_element_by_css_selector('a.u_cbox_btn_more')
                        btn_more.click()
                    except:
                        break
                
                #댓글담기
                try: 
                    review = []
                    x = 1
                    while True:
                        try:
                            review.append(driver.find_element_by_xpath(f'//*[@id="cbox_module_wai_u_cbox_content_wrap_tabpanel"]/ul/li[{x}]/div[1]/div/div[2]/span[1]').text)
                            x += 1
                        except:
                            break

                    #문자열로 변환
                    reviews = " ".join(review)
                    
                    #댓글시간 리스트형태로 담기
                    times = []      
                    reviewTimes = driver.find_elements_by_css_selector('span.u_cbox_date')
                    for reviewTime in reviewTimes:
                        times.append(reviewTime.text)

                    #댓글 좋아요 싫어요 
                    likes = [] 
                    hates = [] 
                    for x in range(1,len(review)+1):
                        try:
                            likes.append(driver.find_element_by_xpath(f'//*[@id="cbox_module_wai_u_cbox_content_wrap_tabpanel"]/ul/li[{x}]/div[1]/div/div[4]/div/a[1]/em').text)
                            hates.append(driver.find_element_by_xpath(f'//*[@id="cbox_module_wai_u_cbox_content_wrap_tabpanel"]/ul/li[{x}]/div[1]/div/div[4]/div/a[2]/em').text)
                        except:
                            likes.append("0")
                            hates.append("0")

                    #댓글수
                    reviewCnt = driver.find_element_by_xpath('//*[@id="cbox_module"]/div[2]/div[2]/ul/li[1]/span').text

                    #댓글 성비, 10대, 20대, 30대, 40대, 50대, 60대 이상
                    try:
                        per = driver.find_elements_by_css_selector('span.u_cbox_chart_per')
                        man = per[0].text
                        girl = per[1].text
                        age10= per[2].text
                        age20 = per[3].text
                        age30 = per[4].text
                        age40 = per[5].text
                        age50 = per[6].text
                        age60 = per[7].text
                    except: #성비가 안나타있는 댓글에는 그냥 공백처리
                        man = " "
                        girl = " "
                        age10= " "
                        age20 = " "
                        age30 = " "
                        age40 = " "
                        age50 = " "
                        age60 = " "
                except:
                        pass
                
                #날짜
                dates =  driver.find_elements_by_css_selector('span.t11')
                for date in dates:
                    tmpDate = [] 
                    tmpDate.append(date.text)
                
                #url 링크
                urlLink = urlDf["url"][i]
                
                df = pd.DataFrame({
                    "제목":title,
                    "본문":text,
                    "댓글":reviews,
                    "댓글 수":reviewCnt,
                    "언론사":press,
                    "남자":man,
                    "여자":girl,
                    "10대":age10,
                    "20대":age20,
                    "30대":age30,
                    "40대":age40,
                    "50대":age50,
                    "60대 이상":age60,
                    "날짜":tmpDate,
                    "링크":urlLink
                    },  )

                for x in range(len(times)):
                    timeDf = pd.DataFrame({
                        "제목":title,
                        "댓글":review[x],
                        "좋아요":likes[x],
                        "싫어요":hates[x],
                        "댓글시간":times[x],
                        "링크":urlLink
                    },index = [i])
                    dfList1.append(timeDf)
                x = 0

                dfList.append(df)
                driver.quit()

            driver.quit()
            articleCnt = len(dfList)
            
            #파일명 저장
            a = (str(datetime.datetime.now()) + str(random.random())).replace(":","")
            b = (str(datetime.datetime.now()) + str(random.random())).replace(":","")
            c = (str(datetime.datetime.now()) + str(random.random())).replace(":","")
            d = (str(datetime.datetime.now()) + str(random.random())).replace(":","")
            e = (str(datetime.datetime.now()) + str(random.random())).replace(":","")

            newsData = pd.concat(dfList)
            reviewsData = pd.concat(dfList1)



            newsData.to_csv(f"./static/html/{pstr}/뉴스기사데이터수집.csv", index=False, encoding="utf-8-sig")
            reviewsData.to_csv(f"./static/html/{pstr}/관련뉴스댓글데이터수집.csv", index=False, encoding="utf-8-sig")            

            newsData = pd.read_csv(f"./static/html/{pstr}/뉴스기사데이터수집.csv")
            reviewsData = pd.read_csv(f"./static/html/{pstr}/관련뉴스댓글데이터수집.csv")
            

            #결측값 있으면 제거
            newsData = newsData.dropna()
            reviewsData = reviewsData.dropna()

            #인덱스 재설정
            newsData = newsData.reset_index(drop=True)
            reviewsData = reviewsData.reset_index(drop = True)

            #댓글이 가장 많이 나온 Top10 기사
            try:
                newsData["댓글 수"] = newsData["댓글 수"].str.replace(",","")
            except:
                pass
            newsData['댓글 수'] = newsData['댓글 수'].astype(int)
            
            #총 댓글수 
            reviewCnt = newsData['댓글 수'].sum()

            newsData = newsData.sort_values(by="댓글 수",ascending=False).reset_index(drop=True)
            newsTop10 = newsData[:10][['제목','링크','댓글 수','언론사']]
            newsTop10Title = newsTop10["제목"]
            newsTop10Link = newsTop10["링크"]
            newsTop10reviews = newsTop10['댓글 수']
            newsTop10press = newsTop10["언론사"]
            
            #성별 및 나이대 분석 공백을 null값으로 바꿔주기
            newsData["남자"] = newsData["남자"].str.replace("%","")
            newsData["남자"] = newsData["남자"].replace(" ",np.nan)
            newsData["남자"] = newsData["남자"].replace("",np.nan)

            newsData["여자"] = newsData["여자"].str.replace("%","")
            newsData["여자"] = newsData["여자"].replace(" ",np.nan)
            newsData["여자"] = newsData["여자"].replace("",np.nan)

            newsData["10대"] = newsData["10대"].str.replace("%","")
            newsData["10대"] = newsData["10대"].replace(" ",np.nan)
            newsData["10대"] = newsData["10대"].replace("",np.nan)

            newsData["20대"] = newsData["20대"].str.replace("%","")
            newsData["20대"] = newsData["20대"].replace(" ",np.nan)
            newsData["20대"] = newsData["20대"].replace("",np.nan)

            newsData["30대"] = newsData["30대"].str.replace("%","")
            newsData["30대"] = newsData["30대"].replace(" ",np.nan)
            newsData["30대"] = newsData["30대"].replace("",np.nan)

            newsData["40대"] = newsData["40대"].str.replace("%","")
            newsData["40대"] = newsData["40대"].replace(" ",np.nan)
            newsData["40대"] = newsData["40대"].replace("",np.nan)

            newsData["50대"] = newsData["50대"].str.replace("%","")
            newsData["50대"] = newsData["50대"].replace(" ",np.nan)
            newsData["50대"] = newsData["50대"].replace("",np.nan)

            newsData["60대 이상"] = newsData["60대 이상"].str.replace("%","")
            newsData["60대 이상"] = newsData["60대 이상"].replace(" ",np.nan)
            newsData["60대 이상"] = newsData["60대 이상"].replace("",np.nan)
            
            #새로운 데이터 세트 만들어주기
            newsDataPrivacy = newsData.dropna()
            newsDataPrivacy = newsDataPrivacy[["남자","여자","10대","20대","30대","40대","50대","60대 이상"]]

            #분석하기 용이하게 str -> int형으로 변환
            newsDataPrivacy["남자"] = newsDataPrivacy["남자"].astype(int)
            newsDataPrivacy["여자"] =newsDataPrivacy["여자"].astype(int)
            newsDataPrivacy["10대"] =newsDataPrivacy["10대"].astype(int)
            newsDataPrivacy["20대"] =newsDataPrivacy["20대"].astype(int)
            newsDataPrivacy["30대"] =newsDataPrivacy["30대"].astype(int)
            newsDataPrivacy["40대"] =newsDataPrivacy["40대"].astype(int)
            newsDataPrivacy["50대"] =newsDataPrivacy["50대"].astype(int)
            newsDataPrivacy["60대 이상"] =newsDataPrivacy["60대 이상"].astype(int)

            newsDataPrivacySum = newsDataPrivacy.sum() 
            
            def gender():
                labels = ["MEN","WOMEN"]
                fig = plt.figure(figsize=(5,5)) 
                fig.set_facecolor('white')
                explode = [0.01, 0.01]
                colors = ['#96e6a1','#fbc2eb']
                wedgeprops={'width': 0.8, 'edgecolor': 'w', 'linewidth': 5}
                plt.pie(newsDataPrivacySum[["남자","여자"]],
                        labels = labels,
                        startangle=90,
                        counterclock=False,
                        autopct='%.1f%%',
                        explode = explode,
                        colors=colors,
                        wedgeprops=wedgeprops)
                plt.legend()
                return plt.savefig(f"./static/html/{pstr}/a.png")
                # return plt.savefig(f"static/image/{a}.png")     
            gender()

            #나이대별 분석
            
            def age():
                labels = ["10's","20's","30's","40's","50's","over 60's"]
                fig = plt.figure(figsize=(10,10)) ## 캔버스 생성
                fig.set_facecolor('white') ## 캔버스 배경색을 하얀색으로 설정
                explode = [0.01, 0.01, 0.01, 0.01,0.01,0.01]
                colors = ['#8fd3f4','#ff9999','#96e6a1','#fda085','#fbc2eb','#ffc000']
                wedgeprops={'width': 0.8, 'edgecolor': 'w', 'linewidth': 5}
                plt.pie(newsDataPrivacySum[["10대","20대","30대","40대","50대","60대 이상"]],
                        labels = labels,
                        startangle=90,
                        autopct='%.1f%%',
                        counterclock=False,
                        explode = explode,colors=colors,wedgeprops=wedgeprops)
                plt.legend(fontsize=10, ncol= 2)
                return plt.savefig(f"./static/html/{pstr}/b.png")
                # return plt.savefig(f"static/image/{b}.png")
            age()

            #날짜별 기사올라온 수 분석 진행
            dateData = newsData[["제목","날짜","댓글 수","언론사","링크"]]

            dateData = dateData.dropna()
            
            for i in range(len(dateData)):
                dateData["날짜"][:][i] = dateData["날짜"][:][i][:10]
            
            dateData["날짜"] = pd.to_datetime(dateData["날짜"]) 
            dateData['날짜']  = dateData['날짜'].dt.date

            reviewsData["댓글시간"] = pd.to_datetime(reviewsData["댓글시간"])
            reviewsData['댓글시간']  = reviewsData['댓글시간'].dt.date

            # 날짜별 기사 업로드 수
            def newsdate():  
                newsByDateSum = dateData['제목'].groupby(dateData["날짜"]).count()
                plt.figure(figsize=(15,8))
                str_plt_style = 'seaborn'
                plt.style.use([str_plt_style])
                plt.ylabel("number of articles")
                plt.plot(newsByDateSum.index, newsByDateSum.values, marker='s',  linestyle='-', linewidth=3)
                plt.xticks(newsByDateSum.index, rotation = 90)
                plt.legend(["number of articles"])
                return plt.savefig(f"./static/html/{pstr}/c.png")
                # return plt.savefig(f"static/image/{c}.png") 
            newsdate()

            # 날짜별 댓글 업로드 수
            def reviewsDate():
                reviewByDateSum = reviewsData['제목'].groupby(reviewsData["댓글시간"]).count()
                plt.figure(figsize=(15,8))
                str_plt_style = 'seaborn'
                plt.style.use([str_plt_style])
                plt.ylabel("number of comments")
                plt.plot(reviewByDateSum.index, reviewByDateSum.values, marker='s',  linestyle='-', linewidth=3)
                plt.xticks(reviewByDateSum.index, rotation = 90)
                plt.legend(["number of comments"])
                return plt.savefig(f"./static/html/{pstr}/d.png")
                # return plt.savefig(f"static/image/{d}.png")
            reviewsDate()

            #기사 많이 달린 날짜 기사들 접근하기

            newsByDateSum = dateData['제목'].groupby(dateData["날짜"]).count()
            topDate = newsByDateSum.sort_values(ascending = False)
            topDate = pd.DataFrame(topDate)
            topDateTop1 = []
            topNewsList = []
            check = topDate["제목"][0]
            topDateTop1.append(topDate["제목"].keys()[0])

            tmp = 1
            while True:
                try:
                    if topDate["제목"][tmp] == check:
                        topDateTop1.append(topDate["제목"].keys()[tmp])
                        tmp += 1
                    else:
                        break
                except:
                    break

            for i in range(len(dateData)):
                if dateData["날짜"][i] in topDateTop1:
                    topNews = pd.DataFrame({
                        "제목":dateData["제목"][i],
                        "댓글수":dateData["댓글 수"][i],
                        "언론사":dateData["언론사"][i],
                        "날짜":dateData["날짜"][i],
                        "링크":dateData["링크"][i]
                    },index = [i])
                    topNewsList.append(topNews)
                    
            topNewsList = pd.concat(topNewsList)
            topNewsList = topNewsList.sort_values(by=['날짜'], axis=0)
            topNewsList = topNewsList.reset_index(drop=True)

            topNewsListTitle = topNewsList["제목"]
            topNewsListReviewCnt = topNewsList["댓글수"]
            topNewsListPress = topNewsList["언론사"]
            topNewsListLink = topNewsList["링크"]
            topNewsListDate = topNewsList["날짜"]

            #좋아요 싫어요 분석
            lhTable = reviewsData[["제목","댓글","좋아요","싫어요","링크"]]
            lhTable["합계"] = lhTable.sum(axis=1).astype(int)
            lhTable = lhTable.sort_values(by="합계",ascending=False).reset_index(drop=True)
            lhTableTotal = lhTable[:40] 
            lhTableTotalReview = lhTableTotal["댓글"]
            lhTableTotalLike = lhTableTotal["좋아요"]
            lhTableTotalHate = lhTableTotal["싫어요"]
            lhTableTotalRink = lhTableTotal["링크"]

            lhTable = lhTable.sort_values(by="좋아요",ascending=False).reset_index(drop=True)
            lhTableLike = lhTable[:40] 
            lhTableLikeReview = lhTableLike["댓글"]
            lhTableLikeLike = lhTableLike["좋아요"]
            lhTableLikeHate = lhTableLike["싫어요"]
            lhTableLikeRink = lhTableLike["링크"]

            lhTable = lhTable.sort_values(by="싫어요",ascending=False).reset_index(drop=True)
            lhTableHate = lhTable[:40]
            lhTableHateReview = lhTableHate["댓글"]
            lhTableHateLike = lhTableHate["좋아요"]
            lhTableHateHate = lhTableHate["싫어요"]
            lhTableHateRink = lhTableHate["링크"] 


            #댓글 워드클라우드 진행
            newsDataWord = newsData["댓글"] 
            newsDataWord = pd.DataFrame(newsDataWord)
            newsDataWord["댓글"] = newsDataWord["댓글"].apply(lambda x: re.sub("[^가-힣\s]","",str(x)))

            word_extractor = WordExtractor(min_frequency=100,
                min_cohesion_forward=0.05, 
                min_right_branching_entropy=0.0
            )
            word_extractor.train(newsDataWord["댓글"].values)
            words = word_extractor.extract()

            cohesion_score = {word:score.cohesion_forward for word, score in words.items()}
            tokenizer = LTokenizer(scores=cohesion_score)

            newsDataWord["tokenizer"] = newsDataWord["댓글"].apply(lambda x: tokenizer.tokenize(x, remove_r=True))

            words = []
            for i in newsDataWord["tokenizer"].values:
                for k in i:
                    words.append(k)
            
            #불용어 처리 

            fileName = open('stopWordTxt.txt','r',encoding="utf-8")

            stopWordList = []
            for line in fileName.readlines():
                stopWordList.append(line.rstrip())
            fileName.close()

            result = [] 
            for word in words: 
                if word not in stopWordList: 
                    result.append(word) 
            
            cnt = Counter(result)
            result = dict(cnt)
            
    
            wordcloud = WordCloud(font_path = 'C:/Windows/Fonts/malgun.ttf', background_color='white', width=500, height=500, colormap = "winter").generate_from_frequencies(result)
            plt.figure(figsize=(10,10))
            plt.axis("off")
            plt.imshow(wordcloud)
            plt.savefig(f"./static/html/{pstr}/e.png")
            # plt.savefig(f"static/image/{e}.png")


            #빈도수 순위 
            rank = sorted(result.items(),reverse=True,key=lambda item: item[1])
            print("time :", time.time() - start)

            #주차별 빈도수 비교
            onlyweek = pd.read_csv(f"./static/html/{pstr}/관련뉴스댓글데이터수집.csv")   
            onlyweek["댓글시간"] = pd.to_datetime(onlyweek["댓글시간"])
            onlyweek["주차"] = onlyweek.댓글시간.dt.week
            cancel = onlyweek["댓글"].isna().groupby(onlyweek['주차']).sum()
            cancel = pd.DataFrame(cancel)
            onlyweek = onlyweek.dropna()
            tmpTable = onlyweek["댓글"].groupby(onlyweek['주차']).sum()
            tmpTable = pd.DataFrame(tmpTable)
            tmpTable["삭제된댓글"] = cancel.values[:len(tmpTable)]

            tmpTable["댓글"] = tmpTable["댓글"].apply(lambda x: re.sub("[^가-힣\s]","",str(x)))

            word_extractor = WordExtractor(min_frequency=100,
                min_cohesion_forward=0.05, 
                min_right_branching_entropy=0.0
            )
            word_extractor.train(tmpTable["댓글"].values)
            words = word_extractor.extract()

            cohesion_score = {word:score.cohesion_forward for word, score in words.items()}
            tokenizer = LTokenizer(scores=cohesion_score)
                    
            tmpTable["tokenizer"] = tmpTable["댓글"].apply(lambda x: tokenizer.tokenize(x, remove_r=True))

            fileName = open('stopWordTxt.txt','r',encoding="utf-8")

            stopWordList = []
            for line in fileName.readlines():
                stopWordList.append(line.rstrip())
            fileName.close()

            i = 0
            for i in range(len(tmpTable)):
                word = []
                words = []
                for word in tmpTable["tokenizer"].values[i]: 
                    if word not in stopWordList: 
                        words.append(word) 
                tmpTable["tokenizer"].values[i] = words
                i += 1
                    
            i = 0
            ranks = []
            for i in range(len(tmpTable)):
                cnt = Counter(tmpTable["tokenizer"].values[i])
                result = dict(cnt)

                weekrank = sorted(result.items(),reverse=True,key=lambda item: item[1])
                weekrank = weekrank[:10]
                ranks.append(weekrank)

            tmpTable["빈도수"] = ranks
            week = tmpTable.index
            tmpTable = tmpTable.reset_index(drop=True)
            finalweek = tmpTable[["빈도수","삭제된댓글"]]
            finalweek["주차"] = week

            varWeek = finalweek["주차"]
            varCnt = finalweek["빈도수"]
            varDel = finalweek["삭제된댓글"]

            noData = ["댓글 없음"] #기사목록은 있어 리스트는 있는데 댓글이 없어서 에러나는것을 방지
            for i in range(len(varCnt)):
                if len(varCnt[i]) == 0:
                    varCnt[i].append(noData)

        print("댓글 포함 HTML 생성")

        env = Environment(extensions=['jinja2.ext.loopcontrols'], loader=FileSystemLoader('templates'))
        template = env.get_template("result.html")

        output_from_parsed_template = template.render(
                                    ip_addr= ip_addr,
                                    keyword = keyword,
                                    num = num,
                                    articleCnt = articleCnt,
                                    reviewCnt = reviewCnt,

                                    newsTop10Title = newsTop10Title, #댓글 많이 달린 뉴스기사 제목 + 링크
                                    newsTop10Link = newsTop10Link,
                                    newsTop10reviews= newsTop10reviews,
                                    newsTop10press = newsTop10press,

                                    topNewsListTitle = topNewsListTitle, #제목
                                    topNewsListLink = topNewsListLink, #링크
                                    topDateTop1 = topDateTop1, #날짜 
                                    topNewsListReviewCnt = topNewsListReviewCnt, #댓글수
                                    topNewsListPress = topNewsListPress, #언론사
                                    topNewsListDate = topNewsListDate, #기사 날짜

                                    image1=a,
                                    image2=b,
                                    image3=c,
                                    image4=d,
                                    image5=e,
                                    rank = rank,

                                    #주차별 변수
                                    finalweek = finalweek,
                                    varWeek = varWeek,
                                    varCnt = varCnt,
                                    varDel = varDel,

                                    #좋아요 싫어요
                                    lhTableTotalReview = lhTableTotalReview,
                                    lhTableTotalLike = lhTableTotalLike,
                                    lhTableTotalHate = lhTableTotalHate,
                                    lhTableTotalRink= lhTableTotalRink,

                                    lhTableLikeReview=lhTableLikeReview,
                                    lhTableLikeLike= lhTableLikeLike,
                                    lhTableLikeHate=lhTableLikeHate,
                                    lhTableLikeRink=lhTableLikeRink,

                                    lhTableHateReview=lhTableHateReview,
                                    lhTableHateLike=lhTableHateLike,
                                    lhTableHateHate=lhTableHateHate,
                                    lhTableHateRink=lhTableHateRink,

                                    jsurl1 = jsurl1,
                                    jsurl2 = jsurl2                                    
                                    )

            


        print(output_from_parsed_template)

        # to save the results
        with open("./static/html/{0}/result.html".format(pstr), "w", encoding='utf-8') as fh:
            fh.write(output_from_parsed_template)

    except:
        try:
            if 'POST' == 'POST':
                # filePath = 'static\image'
                # for file in os.scandir(filePath):
                #     os.remove(file.path)

                #입력 값 받기
                # keyword = request.form['input1']
                # num = int(request.form['input2'])
                keyword = pkeyword
                num = pnum                

                options = webdriver.ChromeOptions()
                options.add_argument("--start-maximized")
                options.add_argument("headless")
                driver = webdriver.Chrome("chromedriver", options=options)
                print("-------------시작--------------")

                # if num == 1 :
                #     url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=4&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:1d,a:all&start={}'
                #     num = '1일'
                if num == 1 :
                    url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=2&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:1m,a:all&start={}'
                    num = '1개월'
                elif num == 6 :
                    url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=6&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:6m,a:all&start={}'
                    num = '6개월'
                elif num == 7 :
                    url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=1&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:1w,a:all&start={}'
                    num = '7일'
                elif num == 12:
                    url ='https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=5&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:1y,a:all&start={}'
                    num = '1년'
                else:
                    url ='https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=13&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:3m,a:all&start={}'
                    num = "3개월"
                with open("./static/html/{0}/log.txt".format(pstr), "w", encoding='utf-8') as f:
                                    f.write(f"\n수집된 기사에 댓글이 없어 기사 목록만 수집 진행.")
                urlList = []
                i = 1
                x = 1
                while True:
                    try:
                        print(f"{x} Page 수집중..")
                        with open("./static/html/{0}/log.txt".format(pstr), "w", encoding='utf-8') as f:
                            f.write(f"\n{x} Page 수집중..")
                        driver.get(url.format(keyword,i))
                        i += 10 
                        x += 1
                        newsUrls = driver.find_elements_by_link_text('네이버뉴스')

                        for newsUrl in newsUrls:
                            tmp = newsUrl.get_attribute('href')
                            urlList.append(tmp)
                        driver.find_element_by_css_selector('a.btn_next')
                        time.sleep(1) #2초에서 1초로 수정
                    except:
                        break
                driver.quit()

                print("==========url수집 완료==========")

                urlDf = pd.DataFrame({"url":urlList})

                dfList = []
                dfList1 = []

                for i in range(len(urlDf)):
                    print(f"진행상황: {i+1} / {len(urlDf)}") #진행도 확인차
                    with open("./static/html/{0}/log.txt".format(pstr), "w", encoding='utf-8') as f:
                        f.write(f"\n진행상황: {i+1} / {len(urlDf)}")
                    driver = webdriver.Chrome("chromedriver", options=options)
                    driver.get(urlDf["url"][i])
                    time.sleep(0.5)

                    #제목담기
                    try:
                        title = driver.find_element_by_xpath('//*[@id="articleTitle"]').text #정치및 사회 기사
                    except:
                        try:
                            title = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/h2').text #연애기사
                        except:
                            try:
                                title = driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[1]/h4').text #스포츠기사
                            except:
                                driver.quit()
                                continue 

                    try:
                        press = driver.find_element_by_xpath('//*[@id="wrap"]/table/tbody/tr/td[2]/div/div[1]/h4/em').text
                    except:
                        press = "NaN"

                    #날짜

                    try:
                        try:
                            tmpDate = [driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/div[2]/span/em').text]
                        except:
                            tmpDate = [driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[1]/div/span[1]').text]

                    except:
                        dates =  driver.find_elements_by_css_selector('span.t11')
                        for date in dates:
                            tmpDate = [] 
                            tmpDate.append(date.text)
                    #url 링크
                    urlLink = urlDf["url"][i]
                    df = pd.DataFrame({
                        "제목":title,
                        "언론사":press,
                        "날짜":tmpDate,
                        "링크":urlLink
                        },)
                    dfList.append(df)
                    driver.quit()

                driver.quit()
                articleCnt = len(dfList)

                newsData = pd.concat(dfList)
                newsData = newsData.dropna()
                newsData = newsData.reset_index(drop=True)

                for i in range(len(newsData)):
                    newsData["날짜"][i] = newsData['날짜'][i].replace("기사입력","")
                    newsData["날짜"][i] = newsData["날짜"][i].strip()
                    newsData["날짜"][i] = newsData["날짜"][i][:10]

                newsDataTitle = newsData["제목"]
                newsDataPress = newsData["언론사"]
                newsDataDate = newsData["날짜"]
                newsDataLink = newsData["링크"]
                reviewCnt = "0"

                

            print("댓글 없는 HTML 생성")

            env = Environment(extensions=['jinja2.ext.loopcontrols'], loader=FileSystemLoader('templates'))
            template = env.get_template('pageError.html')
    
            output_from_parsed_template = template.render(
                                    ip_addr=ip_addr,
                                    keyword = keyword,
                                    num = num,
                                    articleCnt = articleCnt,
                                    reviewCnt = reviewCnt,
                                    newsDataTitle = newsDataTitle,
                                    newsDataPress = newsDataPress,
                                    newsDataDate = newsDataDate,
                                    newsDataLink = newsDataLink,
                                    jsurl1 = jsurl1,
                                    jsurl2 = jsurl2
                                    )

            print(output_from_parsed_template)

            # to save the results
            with open("./static/html/{0}/result.html".format(pstr), "w", encoding='utf-8') as fh:
                fh.write(output_from_parsed_template)                                    

        except:
            with open("./static/html/{0}/log.txt".format(pstr), "w", encoding='utf-8') as f:
                f.write("\npass")


@app.errorhandler(500)
def page_not_fount(error):
    flash("알수없는 오류가 발생했습니다 키워드 및 개월 수를 변경해주세요")
    return render_template('index.html',
                            ),500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)



#문제 
""" 
1. 크롬 버전에 맞춰 크롬드라이버 업데이트
2. 
"""
