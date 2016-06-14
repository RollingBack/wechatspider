# coding: utf-8
import requests
from wechat_db import *
from sqlalchemy.orm import Session
import json
from time import time

def update_comment_info(signature, timestamp, src, ver):
    comment_params = {
        'src': src,
        'ver': ver,
        'timestamp': timestamp,
        'signature': signature,
    }
    comment_url = 'http://mp.weixin.qq.com/mp/getcomment'
    r = requests.get(comment_url, comment_params)
    comment_info = json.loads(r.text)
    print r.url + chr(10)
    print comment_info
    try:
        info = comment_info['read_num'], comment_info['like_num']    
    except KeyError:
        return
    session = Session(engine)
    article = session.query(Article).filter(Article.signature == signature).first()
    article.readnum = info[0]
    article.likenum = info[1]
    session.commit()
    
if __name__ == '__main__':
    session = Session(engine)
    for each_article in session.query(Article).all():
        update_comment_info(each_article.signature, each_article.timestamp, each_article.src, each_article.ver)
    
    
    
    
