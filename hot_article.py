# coding: utf-8

from selenium import webdriver
from selenium.common.exceptions import *
from redis import Redis

driver = webdriver.PhantomJS()
redis_client = Redis('127.0.0.1', 6379, 1)
topics = range(0, 19)
for each_topic in topics:
    topic_key = 'pc_' + str(each_topic)
    driver.get("http://weixin.sogou.com/pcindex/pc/%s/%s.html" % (topic_key, topic_key))
    for each_link in driver.find_elements_by_css_selector(".wx-news-info2 h4 a"):
        redis_client.zadd('hot_article', each_link.get_attribute('href'), float(each_topic))
    for each_page in range(1, 15):
        driver.get("http://weixin.sogou.com/pcindex/pc/%s/%s.html" % (topic_key, each_page))
        for each_link in driver.find_elements_by_css_selector(".wx-news-info2 h4 a"):
                redis_client.zadd('hot_article', each_link.get_attribute('href'), float(each_topic))        
driver.quit()    
