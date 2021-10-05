######설정
from flask import Flask, render_template, request, send_file, make_response, Response
from io import BytesIO
import flask
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
warnings.filterwarnings("ignore")
plt.rc('font', family='Malgun Gothic')

app = Flask(__name__)

######메인화면
@app.route('/')

def main():
    return render_template("index.html")

######결과화면
@app.route('/result', methods = ['POST'])

def result():
    if request.method == 'POST':
        filePath = 'static\image'
        for file in os.scandir(filePath):
            os.remove(file.path)

        #입력 값 받기
        keyword = request.form['input1']
        num = int(request.form['input2'])

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("headless")
        driver = webdriver.Chrome("chromedriver", options=options)
        print("-------------시작--------------")

        if num == 1 :
            url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=2&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:1m,a:all&start={}'
        elif num == 6 :
            url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=6&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:6m,a:all&start={}'
        elif num == 12:
            url ='https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=5&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:1y,a:all&start={}'
        else:
            url ='https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=13&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:3m,a:all&start={}'
        

        urlList = []
        i = 1
        while True:
            try:
                driver.get(url.format(keyword,i))
                i += 10 
                newsUrls = driver.find_elements_by_link_text('네이버뉴스')

                for newsUrl in newsUrls:
                    tmp = newsUrl.get_attribute('href')
                    urlList.append(tmp)
                driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/div/a[2]').click()
                time.sleep(1) #2초에서 1초로 수정
            
            except:
                break
        driver.quit()

        urlDf = pd.DataFrame({"url":urlList})

        dfList = []
        dfList1 = []

        for i in range(len(urlDf)):
            print(f"진행상황: {i+1} / {len(urlDf)}") #진행도 확인차
            driver = webdriver.Chrome("chromedriver", options=options)
            driver.get(urlDf["url"][i])
            # time.sleep(2)
            
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
                contents = driver.find_elements_by_css_selector('span.u_cbox_contents')
                for content in contents:
                    review.append(content.text)

                #문자열로 변환
                review = " ".join(review)
                
                #댓글시간 리스트형태로 담기
                times = []      
                reviewTimes = driver.find_elements_by_css_selector('span.u_cbox_date')
                for reviewTime in reviewTimes:
                    times.append(reviewTime.text)

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
                "댓글":review,
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
                    "댓글시간":times[x]
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

        #파일 저장
        newsData.to_csv(f"static/file/뉴스기사데이터수집.csv", index=False, encoding="utf-8-sig")
        reviewsData.to_csv(f"static/file/관련뉴스댓글데이터수집.csv", index=False, encoding="utf-8-sig")

        newsData = pd.read_csv(f"static/file/뉴스기사데이터수집.csv")
        reviewsData = pd.read_csv(f"static/file/관련뉴스댓글데이터수집.csv")

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
            labels = ["남자","여자"]
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
            return plt.savefig(f"static/image/{a}.png")     
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
            return plt.savefig(f"static/image/{b}.png")
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
            return plt.savefig(f"static/image/{c}.png") 
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
            return plt.savefig(f"static/image/{d}.png")
        reviewsDate()

        #기사 많이 달린 날짜 기사들 접근하기

        newsByDateSum = dateData['제목'].groupby(dateData["날짜"]).count()
        topDate = newsByDateSum.sort_values(ascending = False)
        topDate = pd.DataFrame(topDate)
        topDateTop1 =  topDate["제목"].keys()[0]

        topNewsList = []
        for i in range(len(dateData)):
            if dateData["날짜"][i] == topDateTop1 :
                topNews = pd.DataFrame({
                    "제목":dateData["제목"][i],
                    "댓글수":dateData["댓글 수"][i],
                    "언론사":dateData["언론사"][i],
                    "날짜":dateData["날짜"][i],
                    "링크":dateData["링크"][i]
                },index = [i])
                topNewsList.append(topNews)
                
        topNewsList = pd.concat(topNewsList)
        topNewsList = topNewsList.reset_index(drop=True)

        topNewsListTitle = topNewsList["제목"]
        topNewsListReviewCnt = topNewsList["댓글수"]
        topNewsListPress = topNewsList["언론사"]
        topNewsListLink = topNewsList["링크"]


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
        plt.savefig(f"static/image/{e}.png")


        #빈도수 순위 
        rank = sorted(result.items(),reverse=True,key=lambda item: item[1])

    return render_template("result.html",
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

                            image1=a,
                            image2=b,
                            image3=c,
                            image4=d,
                            image5=e,
                            rank = rank
                            )

#####파일 다운로드 
@app.route("/getCsV")
def getPlotCSV():
    with open(f"static/file/뉴스기사데이터수집.csv",'rt', encoding='UTF8') as fp:
        csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=rowdata.csv"})

#####파일 다운로드 
@app.route("/getCsV2")
def getPlotCSV2():
    with open(f"static/file/관련뉴스댓글데이터수집.csv",'rt', encoding='UTF8') as fp:
        csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=onlyReview.csv"})

if __name__ == '__main__':
    app.run()



















# from flask import Flask, Response
# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return '''
#         <html><body>
#         Hello. <a href="/getCsV">Click me.</a>
#         </body></html>
#         '''

# @app.route("/getCsV")
# def getPlotCSV():
#     with open(f"{keyword}_관련뉴스기사데이터수집.csv",'rt', encoding='UTF8') as fp:
#         csv = fp.read()
#     return Response(
#         csv,
#         mimetype="text/csv",
#         headers={"Content-disposition":
#                  "attachment; filename=myplot.csv"})


# app.run(debug=True)
















