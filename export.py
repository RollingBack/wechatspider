# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from redis import Redis
redis_client = Redis('localhost', 6379, 9)
f = open('wechat_word_cut.csv', 'w', 1024)
for each_word_cut in redis_client.zrevrangebyscore('wechat_word_cut', '+inf', '20', withscores=True):
    if len(each_word_cut[0].encode().decode()) > 1:
        f.write(each_word_cut[0].encode('gbk') + ',' + str(int(each_word_cut[1])) + chr(10))
f.close()
