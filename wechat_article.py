# coding: utf-8
import requests
from bs4 import BeautifulSoup
from time import time
import json
from wechat_db import *
from sqlalchemy.orm import Session
import urlparse

class WechatArticle():
    
    def __init__(self):
        self.session = Session(engine)

    def get_article_in_sougou(self, keyword):
        base_url = 'http://weixin.sogou.com/weixin'
        page = 1
        while True:
            params = {
                'type': 2,
                'query': keyword,
                'ie': 'utf8',
                'page': page,
            }
            r = requests.get(base_url, params)
            soup = BeautifulSoup(r.text, "lxml")
                
            if len(soup.select("h4 a")) == 0:
                return
            for each_search_result in soup.select("h4 a"):
                wechat_article = get_article(each_search_result['href'])
                save_article(wechat_article)
            page += 1
                
    def get_article(self, href, keyword=""):
        url = urlparse.urlparse(href)
        url_params = urlparse.parse_qs(url.query, True)
        signature = url_params['signature'][0]
        timestamp = url_params['timestamp'][0]
        src = url_params['src'][0]
        ver = url_params['ver'][0]
        article = requests.get(href)
        article.encoding = 'utf-8'
        article_soup = BeautifulSoup(article.text, "lxml")
        try:
            date =  article_soup.select("#post-date")[0].get_text().strip(' ')[0:10]
        except IndexError as err:
            date = ''
        try:
            user = article_soup.select("#post-user")[0].get_text().strip(' ')
        except IndexError as err:
            user = ''
        try:
            content =  article_soup.select("#js_content")[0].get_text().strip(' ')
        except IndexError as err:
            content = ''
        return Article(signature,
                    timestamp, 
                    src,
                    ver, 
                    date, 
                    user,
                    article_soup.title.text,
                    content,
                    keyword
                    )
        
    def save_article(self, article):
        self.session.merge(article)
        self.session.commit()
        
    def roll_back(self):
        self.session.rollback()
    
        
if __name__ == '__main__':
    get_article_in_sougou("理财")