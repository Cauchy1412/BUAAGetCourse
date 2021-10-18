from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json
import time
import requests
from datetime import datetime
import re
from selenium.webdriver.chrome.options import Options


def _get_hidden_items(text):
    ''' get hidden item of html text '''
    item_pattern = re.compile(r'<input type="hidden" name="(.*?)" value="(.*?)"')
    items = re.findall(item_pattern, text)
    return {item[0]: item[1] for item in items}


def _get_hidden_items2(text):
    ''' get hidden item of html text '''
    item_pattern = re.compile(r'<input type="hidden" id="(.*?)" name="(.*?)"\s+value="(.*?)"')
    items = re.findall(item_pattern, text)
    return {item[1]: item[2] for item in items}


def _get_default_header():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
    return header


def grabcoures():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(browser, 5)
    browser.get("http://jwxt.buaa.edu.cn:8080/ieas2.1")
    browser.find_element_by_xpath('//*[@id="notice"]/div[2]/div[1]/p[2]/input').click()
    wait.until(EC.frame_to_be_available_and_switch_to_it(browser.find_element_by_id('loginIframe')))
    USER_NAME = '' #填账号
    USER_PASSWORD = '' #填密码
    time.sleep(5)
    browser.find_element_by_id("unPassword").send_keys(USER_NAME)
    browser.find_element_by_id("pwPassword").send_keys(USER_PASSWORD)
    browser.find_element_by_xpath('//*[@id="content-con"]/div[1]/div[7]/input').click()
    cookies = {}
    for cookie in browser.get_cookies():
        cookies[cookie['name']] = cookie['value']
    browser.close()
    type = '一般专业' #填想选的课的类型
    var1 = ''
    var2 = ''
    var3 = ''
    if type == '一般专业':
        var1 = 'xslbxk'
        var2 = 'ZYL'
        var3 = 'xslbxk'
    elif type == '核心通识':
        var1 = 'xsxk'
        var2 = 'TSL'
        var3 = 'tsk'
    elif type == '一般通识':
        var1 = 'xsxk'
        var2 = 'TSL'
        var3 = 'qxrx'
    list_url = 'http://jwxt.buaa.edu.cn:8080/ieas2.1/xslbxk/queryXsxkList?pageXkmkdm=' + var2
    response = requests.get(list_url, cookies=cookies)
    text = response.text
    payload = _get_hidden_items2(text)
    course = '' #课程编号
    #course = 'B3J063890' #for example
    rwh = '' + course + '' #rwh
    #rwh = '2021-2022-1-' + course + '-001' #for example
    payload['pageXnxq'] = '' #pageXnxq
    #payload['pageXnxq'] = '2021-20221' #for example
    payload['pageKkxiaoqu'] = ''
    payload['pageKkyx'] = ''
    payload['pageKcmc'] = ''
    payload['pageXklb'] = var3
    payload['rwh'] = rwh
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    }
    response = requests.post('http://jwxt.buaa.edu.cn:8080/ieas2.1/' + var1 + '/saveXsxk', data=payload, cookies=cookies)
    if "选课成功" in response.text:
        print("选课成功")
        exit()
    elif "容量已满" in response.text:
        print("容量已满")
    elif "不在学生选课时间范围内" in response.text:
        print("不在学生选课时间范围内")
    else:
        print("意料之外")
    time.sleep(1)

for i in range(10000):
    grabcoures()
    time.sleep(5)


