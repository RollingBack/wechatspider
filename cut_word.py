# coding: utf-8
from wechat_db import *
from sqlalchemy.orm import Session
from redis import Redis
import jieba


session = Session(engine)
redis_client = Redis('127.0.0.1', 6379, 9)
query = session.query(Article).all()
for each_artilce in query:
    title_words = jieba.cut(each_artilce.title)
    for each_word in title_words:
        redis_client.zincrby('wechat_word_cut', each_word)
    content_words = jieba.cut(each_artilce.content)
    for each_word in content_words:
        redis_client.zincrby('wechat_word_cut', each_word)
    