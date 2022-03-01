import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import quote
import time
import re


username = ''                    #帐号
password = ''                  #密码
type = '一般专业'                        #选课类型（一般专业课 核心专业课 核心通识课 一般专业课）
typeDict = {'一般专业':('xslbxk','ZYL','xslbxk'), '核心专业':('xslbxk', 'ZYL', 'xslbxk'), '核心通识':('xsxk','TSL','tsk'),'一般通识':('xsxk','TSL','qxrx')}
var1,var2,var3 = typeDict[type]
course = 'B3J063220'                    #课程编号  B3J063220为举例
rwh = '2021-2022-2-' + course + '-001'  #001为默认 同一课程编号有不同老师时改为00n n为搜索该课出现的第n个
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
    item_pattern = re.compile(r'<input type="hidden" id="(.*?)" name="(.*?)"\s+value="(.*?)"')
    items = re.findall(item_pattern, text)
    return {item[1]: item[2] for item in items}


def chose():
    session = requests.Session()
    login(username, password, session)
    list_url = 'http://jwxt.buaa.edu.cn:8080/ieas2.1/xslbxk/queryXsxkList?pageXkmkdm=' + var2
    response = session.post(list_url,allow_redirects=True)
    payload=_get_hidden_items(response.text)
    payload['pageXnxq'] = '2021-20222'
    payload['pageKkxiaoqu'] = ''
    payload['pageKkyx'] = ''
    payload['pageKcmc'] = ''
    payload['pageXklb'] = var3  
    payload['rwh'] = rwh
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
    time.sleep(1)