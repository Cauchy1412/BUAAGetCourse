import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import quote
import time
import re


page_xnxq = ''
username = ''  #fill in
password = ''  #fill in
type = '核心专业'
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
elif type == '核心专业':
    var1 = 'xslbxk'
    var2 = 'ZYL'
    var3 = 'xslbxk'

jiaowu_url = 'http://jwxt.buaa.edu.cn:8080/ieas2.1/'
login_url = 'https://sso.buaa.edu.cn/login?service=' \
            + quote(jiaowu_url, 'utf-8') + 'welcome'


def get_login_token(session):
    r = session.get(login_url)
    assert (r.status_code == 200)
    soup = BeautifulSoup(r.content, 'html.parser')
    lt = soup.find('input', {'name': 'execution'})['value']
    return lt


def login(username, password, session):
    formdata = {
        'username': username,
        'password': password,
        'execution': get_login_token(session),
        'type': 'username_password',
        '_eventId': 'submit',
        'submit': '登陆'
    }
    r2 = session.post(login_url, data=formdata, allow_redirects=True)
    soup = BeautifulSoup(r2.text, "html.parser")
    return not soup.find_all('div', class_='error_txt')


def _get_hidden_items(text):
    ''' get hidden item of html text '''
    item_pattern = re.compile(r'<input type="hidden" id="(.*?)" name="(.*?)"\s+value="(.*?)"')
    items = re.findall(item_pattern, text)
    return {item[1]: item[2] for item in items}


def chose():
    session = requests.Session()
    login(username, password, session)
    list_url = 'http://jwxt.buaa.edu.cn:8080/ieas2.1/xslbxk/queryXsxkList?pageXkmkdm=' + var2
    response = session.post(list_url,allow_redirects=True)
    payload=_get_hidden_items(response.text)
    course = 'B3I063130' #to modify
    rwh = '2021-2022-2-' + course + '-001'
    payload['pageXnxq'] = '2021-20222'
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
    response = session.post('http://jwxt.buaa.edu.cn:8080/ieas2.1/' + var1 + '/saveXsxk',data=payload)
    if "选课成功" in response.text:
        print("选课成功")
        exit()
    elif "容量已满" in response.text:
        print("容量已满")
    elif "不在学生选课时间范围内" in response.text:
        print("不在学生选课时间范围内")
    else:
        print("意料之外")


while True:
    chose()
    time.sleep(5)
