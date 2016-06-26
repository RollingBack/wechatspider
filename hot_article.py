# coding: utf-8

from selenium import webdriver
from selenium.common.exceptions import *
import jieba
import requests
from bs4 import BeautifulSoup
from time import time
import datetime
from urllib.parse import urlparse
from urllib.parse import parse_qs
from cyordereddict import OrderedDict
from requests.exceptions import ConnectionError
from pickle import dumps
import json

def get_article(href):
    url = urlparse(href)
    url_querys = parse_qs(url.query)
    signature = url_querys['signature']
    timestamp = url_querys['timestamp']
    src = url_querys['src']
    ver = url_querys['ver']
    try:
        article = requests.get(href)
    except Exception:
        print(href)
        return
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
    return (article_soup.title.text, content)

def wechat_links(driver):
    topics = range(0, 19)
    for each_topic in topics:
        topic_key = 'pc_' + str(each_topic)
        try:
            driver.get("http://weixin.sogou.com/pcindex/pc/%s/%s.html" % (topic_key, topic_key))
        except TimeoutException as e:
            print(topic_key)
            pass
        try:
            for each_link in driver.find_elements_by_css_selector(".wx-news-info2 h4 a"):
                yield each_link.get_attribute('href')
        except InvalidSelectorException:
            pass
                
        for each_page in range(1, 15):
            try:
                driver.get("http://weixin.sogou.com/pcindex/pc/%s/%s.html" % (topic_key, each_page))
            except TimeoutException as e:
                print(topic_key, each_page)
                pass
            try:
                for each_link in driver.find_elements_by_css_selector(".wx-news-info2 h4 a"):
                        yield each_link.get_attribute('href')
            except InvalidSelectorException as e:
                pass
            
def word_cuts(article):
    for each_word_cut in jieba.cut(article[0]):
        yield each_word_cut
    for each_word_cut in jieba.cut(article[1]):
        yield each_word_cut
        
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
    try:
        info = comment_info['read_num'], comment_info['like_num']
        return info
    except KeyError:
        return

driver = webdriver.PhantomJS()
jieba.set_dictionary('dict.txt.big.txt')
jieba.enable_parallel(4)

big_dict = OrderedDict()        
for each_link in wechat_links(driver):
    print(each_link)
    article = get_article(each_link)
    if article is not None:
        for each_word_cut in word_cuts(article):
            if len(each_word_cut) > 1:
                if big_dict.get(each_word_cut) is None:
                    big_dict[each_word_cut] = 1
                else:
                    big_dict[each_word_cut] += 1
                    
driver.quit()
big_dict = sorted(big_dict.items(), key=lambda d: d[1], reverse=True)

now = datetime.datetime.now()
today = now.strftime('%Y%m%d%H%M%S')
pfile = open("wechat_word_cut"+today+".pkl", "wb", buffering=1024)
pfile.write(dumps(big_dict))
pfile.close()
f = open("wechat_word_cut"+today+".csv", "wb", buffering=1024)
for each_word_cut, word_count in big_dict:
    line = each_word_cut + "," + str(word_count) + chr(10)
    f.write(line.encode('utf-8'))
f.close()



