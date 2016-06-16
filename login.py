# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import sys
reload(sys)
sys.setdefaultencoding('utf8')

driver = webdriver.Chrome()
keywords =  ["理财", "融资", "投资", "信托", "金融", "贷款", "财产", "理财产品", "财经", "基金", "收益", "租赁", "P2P", "私募", "担保", "收益率", "理财网", "债券", "黄金", "融券", "小额", "p2p", "小额贷款", "利率", "外汇", "信托公司", "金融界", "债权", "供应链", "风险投资", "信托投资", "银行贷款", "家庭理财", "投资者", "期货", "融资难", "融资券", "贵金属", "借款", "投资收益", "信托投资公司", "证券公司", "投资信托", "金融机构", "全透明", "风险管理", "理财专家", "保险公司", "金融市场", "基金业", "保险产品", "安全可靠", "高风险", "投资界", "金融公司", "股票投资", "金融资产", "金融业务", "银行信贷", "银行利率", "年利率", "短期投资", "融资额", "金融交易", "消费信贷", "长期投资", "贷款额", "资产负债", "贷款额度", "长期贷款", "银行借款", "金融风险", "抵押借款", "银行担保", "投资额", "2016p2p"]
driver.get("http://weixin.sogou.com")
#driver.find_element_by_id("loginBtn").click()
#sleep(20)
for each_keyword in keywords:
    print each_keyword
    driver.find_element_by_id("upquery").send_keys(each_keyword.decode('utf-8'))
    driver.find_element_by_css_selector(".swz").click()
    sleep(1)
    links = driver.find_elements_by_css_selector(".txt-box h4 a")
    for each_link in links:
        each_link.get_attribute('href')
    index = 2
    while True:
        id_ = "#sogou_page_"+str(index)
        #driver.find_element_by_css_selector(id_)
        driver.execute_script("$('"+id_+"').click();")
        sleep(1)
        links = driver.find_elements_by_css_selector(".txt-box h4 a")
        for each_link in links:
            each_link.get_attribute('href')
        index += 1
driver.quit()