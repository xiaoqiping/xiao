#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import hashlib

def LoginByPost():
    #c创建session会话
    s=requests.session()
    password = 'KBkx05jt';

    loginUrl='http://pms.jzic.com/index.php?m=user&f=login'
    login_res = s.get(loginUrl)
    login_res.encoding = 'utf-8'

    bs = BeautifulSoup(login_res.text, "html.parser")

    verifyRand = bs.find(id="verifyRand").get('value')
    verifyRand = verifyRand.encode('utf-8')

    md5password = hashlib.md5(password.encode('utf-8')).hexdigest()
    md5password = md5password.encode('utf-8')
    md5passwordverifyRand =  hashlib.md5((str(md5password) + str(verifyRand)).encode('utf-8')).hexdigest()

    ##设置cookies参数
    cookies = requests.utils.cookiejar_from_dict({'__root_domain_v': '.jzic.com','_qddaz':'QD.bxv6id.1b4qf9.k1lfu34z','goodsBrowseHistory=':'a%3A1%3A%7Bi%3A0%3Bs%3A5%3A%2219695%22%3B%7D','zentaosid':'s2bcdsg1vu4p9hmmm104lct6hq'})
    #print(type(cookies), cookies)
    s.cookies = cookies

    postData={'account':'xiaoqiping','password':md5passwordverifyRand,'referer':'http://pms.jzic.com/index.php?m=my&f=index','verifyRand':verifyRand,'passwordStrength':1,'keepLogin[]':'on'}
    header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
              "Referer": "http://pms.jzic.com/index.php?m=user&f=login"
              }
    rs=s.post(loginUrl,data = postData ,headers = header)
    #print(rs.cookies.values())


    #
    #
    # print(rs)
    url='http://pms.jzic.com/index.php?m=story&f=view&storyID=1130'
    res=s.get(url)
    print(res.text)
    # res.encoding='utf-8'
    # print(res.text)

LoginByPost()