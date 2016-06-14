# coding: utf-8
import requests
from bs4 import BeautifulSoup
from time import time
import json
from wechat_db import *
from sqlalchemy.orm import Session

keyword = "理财"
base_url = 'http://weixin.sogou.com/weixin'
comment_url = 'http://mp.weixin.qq.com/mp/getcomment'
params = {
    'type': 2,
    'query': keyword,
    'ie': 'utf8',
    'page': 1,
}
comment_params = {
    'src': 3,
    'ver': 1,
    'timestamp': int(time())
}
r = requests.get(base_url, params)
soup = BeautifulSoup(r.text, "lxml")
session = Session(engine)
for each_search_result in soup.select("h4 a"):
    signature = each_search_result['href'].split('signature=')[1]
    comment_params['signature'] = signature
    article = requests.get(each_search_result['href'])
    article_soup = BeautifulSoup(article.text, "lxml")
    comment_info = json.loads(requests.get(comment_url, comment_params).text)
    print comment_info
    print article_soup.select("#post-date")[0].get_text().strip(' ')[0:10]
    wechat_article = Article(article_soup.select("#post-date")[0].get_text().strip(' ')[0:10],
                             article_soup.select("#post-user")[0].get_text(),
                             article_soup.title.text,
                             article_soup.select("#js_content")[0].get_text(),
                             comment_info['read_num'],
                             comment_info['like_num'],
                             keyword
                             )
    session.add(wechat_article)
session.commit()
    