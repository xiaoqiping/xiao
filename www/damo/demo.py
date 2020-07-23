#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-

import requests,json
def prox():

    a={"features":{"isAllowCompanyMap":"WP_WIDGET_VAS_COMPANY_MAP"},"address":"中国 广东 广州市越秀区惠福西路294号首层商场内第5A号档","showAlert":True,"showTitle":True,"showResult":True,"companyName":"广州市越秀区民娜涛电子经营部"}
    print(eval(a))
    exit()
    s = requests.session()
    s.keep_alive = False
    url = 'https://suying138.1688.com/page/contactinfo.htm?spm=a261y.7663282.autotrace-topNav.8.228f89bb4Tyl0L'
    proxies = {'http': 'http://125.66.51.42:49936',
               'https': 'https://125.66.51.42:49936'}
    headers = {

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",

    }

    html = requests.get(url, headers=headers,proxies=proxies,timeout=(6.05, 27.05))
    print(html.text)
    exit()


    ip_list = [
        'http://60.216.20.210:8001',
        'http://120.192.75.82:808',
        'http://124.205.155.153:9090',
        'http://117.141.155.242:53281',
        'http://114.98.24.221:4216',
        'http://163.125.29.106:8118'
    ]


    for i in ip_list:
        ip_list1={'http':i}
        headers = {
            'Host': 'liu13432460447.b2b.hc360.com',
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
            'Referer': 'https://liu13432460447.b2b.hc360.com/'
        }

        html = requests.get(url,headers=headers,proxies=proxies,timeout=(6.05, 27.05)).text
        print(html)
        break
        if '<html>' in html:
            pass
        else:
            print (i)
if __name__=='__main__':
    prox()




