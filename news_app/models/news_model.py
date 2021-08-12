from typing import Text
from news_app import db
import csv

import pandas as pd
import time

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re

from news_app.utils.main_funcs import SentenceTokenizer, GraphMatrix, Rank, TextRank

class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.String(64), primary_key=True)
    date = db.Column(db.String(64))
    text = db.Column(db.String)
    summary = db.Column(db.String)
    url = db.Column(db.String)

    # user_laptops = db.relationship('User_laptop', backref='laptop', cascade = "all,delete") #user.tweets를 통해 tweet_model을 참조할 수 있음.

    def __repr__(self):
        return f"News {self.id}"



def renew_news():
    news_data_check = News.query.all()

    # 크롤링
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=104'

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(r'C:\Users\tjddy\ipynb_files\ipynb_files\chromedriver\chromedriver.exe', options=options)
    driver.get(url)

    driver.find_element_by_xpath('//*[@id="main_content"]/div/div[2]/div[2]/div/a').click()

    #뉴스 기사 페이지 소스 받기
    soup_nums_date = BeautifulSoup(driver.page_source)
    
    #뉴스 id
    nums = soup_nums_date.find_all(class_="cluster_head_more_icon_num")
    
    #날짜저장
    date = soup_nums_date.find(class_="lnb_date").get_text()

    #뉴스 ulr
    urls_cluster = soup_nums_date.find_all('div', attrs = {"class" : "cluster_group"})

    articles = []
    
    #text 크롤링
    for page in range(1,13):
        try:
            url = urls_cluster[page-1].find('a', class_="cluster_text_headline nclicks(cls_wor.clsart)").get("href")
            num = nums[page-1].get_text()
            id = date+str(num)
            id = re.sub(r'[^0-9]', '', id)
            
            driver.find_element_by_xpath('//*[@id="main_content"]/div/div[2]/div[1]/div['+str(page)+']/div[2]/ul/li[1]/div[2]/a').click()
            
            time.sleep(3)
            
            soup = BeautifulSoup(driver.page_source)
            body = soup.find(id='articleBodyContents')

            article = body.get_text()

            #불필요문자 제거
            if "// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}" in article:
                article = article.replace("// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}", "")

            article = re.sub(r'\[[^)]*\]', '', article)
            article = re.sub(r'\<[^)]*\>', '', article)
            article = re.sub(r'\©[^)]*\=', '', article)

            articles.append([id, date, article, url])
            
            driver.back()
            time.sleep(3)
        except:
            print('pass')
    
    #크롤링 종료
    driver.quit()

    #크롤링 데이터 저장
    data = pd.DataFrame(articles, columns = ['id', 'date', 'text', 'url'])
    data.to_csv("news.csv")

    with open('news.csv', encoding = 'utf-8') as f:
        file = csv.DictReader(f)
        id_check = []

        for i, row in enumerate(file):
            id = row['id']
            date = row['date']
            text = row['text']
            
            textrank = TextRank(text)
            summary_list = textrank.summarize(3)
            summary = ' '.join(summary_list)

            url = row['url']

            row_data = News(id=id,
                            date=date, 
                            text=text, 
                            summary=summary,
                            url=url
                            )
            
            if News.query.filter(News.id == row_data.id).first() == None: #primary key 중복제거
                db.session.add(row_data)
            
        db.session.commit()


def get_news():

    return News.query.all()

if __name__ == 'main':
    breakpoint()