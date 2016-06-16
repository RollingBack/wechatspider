# coding: utf-8
import requests
from bs4 import BeautifulSoup
from time import time
import json
from wechat_db import *
from sqlalchemy.orm import Session
import urlparse

def get_article_in_sougou(keyword):
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
        session = Session(engine)
        if len(soup.select("h4 a")) == 0:
            return
        for each_search_result in soup.select("h4 a"):
            url = urlparse.urlparse(each_search_result['href'])
            url_params = urlparse.parse_qs(url.query, True)
            signature = url_params['signature'][0]
            timestamp = url_params['timestamp'][0]
            src = url_params['src'][0]
            ver = url_params['ver'][0]
            article = requests.get(each_search_result['href'])
            article_soup = BeautifulSoup(article.text, "lxml")
            wechat_article = Article(signature,
                                     timestamp, 
                                     src,
                                     ver, 
                                     article_soup.select("#post-date")[0].get_text().strip(' ')[0:10],
                                     article_soup.select("#post-user")[0].get_text(),
                                     article_soup.title.text,
                                     article_soup.select("#js_content")[0].get_text(),
                                     keyword
                                     )
            print wechat_article
            session.add(wechat_article)
        session.commit()
        page += 1
        
if __name__ == '__main__':
    get_article_in_sougou("理财")