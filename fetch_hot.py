# coding: utf-8
from redis import Redis
from wechat_article import WechatArticle
from wechat_db import Article
from sqlalchemy.exc import DatabaseError
import sys
reload(sys)
sys.setdefaultencoding('utf8')

redis_client = Redis('localhost', 6379, 1)
all_hot_links = redis_client.zrange("hot_article", 0, -1)
wechat_article = WechatArticle()
for each_hot_link in all_hot_links:
    print each_hot_link + chr(10)
    article =  wechat_article.get_article(each_hot_link)
    try:
        wechat_article.save_article(article)
    except DatabaseError as err:
        print article
        wechat_article.roll_back()
        print err