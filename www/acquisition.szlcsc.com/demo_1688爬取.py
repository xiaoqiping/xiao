#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-

import requests,json
from bs4 import BeautifulSoup
import re
import datetime
import time
import math
import collections
from datetime import timedelta
import sys
import os
from mysql import mysql
from urllib.parse import urlsplit
from fake_useragent import UserAgent
import hashlib
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.adapters.DEFAULT_RETRIES = 10
s = requests.session()
s.keep_alive = False

mysql_config = {'host':'106.14.127.145', 'user':'kaifa', 'password':'yB8FtzFSlSa5QYE0vzd8','db':'jzic_crawl_data'}
#d当前时间
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
location = 'file/气象数据家园/fake_useragent.json'
ua = UserAgent(path=location)


#任务处理
def cj_task():
    db = mysql(host=mysql_config['host'], user=mysql_config['user'], password=mysql_config['password'],db=mysql_config['db'])
    # 查询版本信息
    task_info = db.get_one("SELECT * FROM `cj_collection_company_task` where status = 1 and name='1688数据采集' ORDER BY `task_id` DESC LIMIT 1",params=())
    if task_info:
        print("存在未处理完的任务继续处理")
    else:
        try:
            inset_data = ('1688数据采集', '1688数据采集系统自动新增任务', now, 1)
            sql = "INSERT INTO cj_collection_company_task (`name`,`desc`, `update_time`, `status`) VALUES (%s, %s, %s, %s);"
            results = db.edit(sql, inset_data)
            if results == None:
                # 创建异常对象
                ex = Exception("===================新增任务失败")
                # 抛出异常对象
                raise ex
        except Exception  as result:
            print('===================新增任务异常异常', result)
            exit()
        print('===================新增任务成功')


def data_goodslist():
    # try:
        db = mysql(host=mysql_config['host'], user=mysql_config['user'], password=mysql_config['password'],db=mysql_config['db'])

        task_info = db.get_one("SELECT * FROM `cj_collection_company_task` where status = 1 and name = '1688数据采集' ORDER BY `task_id` DESC LIMIT 1", params=())
        if not task_info or task_info == None:
            print("任务不存在")
            return False;

        #加1为当前处理版本
        cj_szlcsc_category_list = db.get_all("SELECT * FROM `cj_1688_category` where category_level = 2 and status = 1 and task_id = "+str(task_info[0])+"", params=())
        if not cj_szlcsc_category_list or cj_szlcsc_category_list == None:
            print("本地版本没有需要处理的数据")
            return False;


        for i in cj_szlcsc_category_list:
            #总页数
            print("=============================正在处理分类："+str(i[2])+"每页20条")
            p =i[10]+1
            ii =p
            while True:
                print("=============================正在处理分类：" + str(i[2]) + "正在处理第******"+str(ii)+"******页的数据")
                global proxies
                try:
                    r = requests.post(
                        'http://dynamic.goubanjia.com/dynamic/get/787b33d192b9275f9e6b1acd88c015a1.html?sep=6',
                        timeout=(6.05, 27.05))
                    r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
                    if r.text.strip(';'):
                        proxies = {"http": "http://" + str(r.text.strip(';')),
                                   "https": "https://" + str(r.text.strip(';'))}
                    else:
                        print("代理失效")
                        exit()
                except requests.RequestException as e:
                    print(e)
                    exit()
                try:
                    data ={
                        'namespace':'cateMarketOfferList',
                        'widgetId': 'cateMarketOfferList',
                        'methodName': 'execute',
                        'params':{"sceneId":i[0],"curPage":ii,"pageSize":20,"sortType":'null',"descendOrder":'null',"priceStart":'null',"priceEnd":'null',"province":"","city":""},
                        'sceneId': i[0],
                        'curPage': ii,
                        'pageSize': 20,
                        'sortType':'',
                        'descendOrder':'',
                        'priceStart':'',
                        'priceEnd':'',
                        'province':'',
                        'city':'',
                        '__mbox_csrf_token':'KoZ2gZluKKRE83Z4_1591866401301'
                    }
                    headers = {
                        # 'authority':"widget.1688.com",
                        # 'method': "POST",
                        # 'path': "/front/ajax/getJsonComponent.json",
                        # 'scheme':'https',
                        # "accept": "application/json,text/javascript,*/*;q=0.01",
                        # "accept-encoding": "gzip,deflate,br",
                        # "accept-language": "zh-CN, zh;q=0.9",
                        # "cache-control": "no-cache",
                        # "content-length": "455",
                        # "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
                        "cookie": "SameSite=none; SameSite=none; cna=xTr3FsPSoy4CAXkPB3n64Khu; UM_distinctid=17297aa564a74e-0ed0e7c41ce1fa-f7d1d38-1fa400-17297aa564b7a3; _csrf_token=1591682454281; taklid=654f531b949446a79af92c7f38e01dab; cookie2=1db9057217a3de624732cef46eefac80; hng=CN%7Czh-CN%7CCNY%7C156; t=2993b253a990044dadf2982c45a16332; _tb_token_=7770be5e3f987; lid=tiamomeixiao; uc4=id4=0%40UOnnEYTvD%2B2H1GSBKeFw4tR7mNfb&nk4=0%40FYWuvJYXpROYxzGk2FKININLCZQOSpk%3D; __cn_logon__=false; alicnweb=touch_tb_at%3D1591682425834; ali_beacon_id=119.137.53.121.1591682459304.685326.9; l=eBab1QUgQWP6CwjBBO5Clurza77OyIOb4rVzaNbMiInca6MFgF13uNQDKFe9zdtjgt13yetPOzL1BdLHR3ABOxDDBcsZvflZnxf..; isg=BElJt4Jpcycw7w9Uq2CeGWnzWHWjlj3IV3O3K-u_9DBvMmlEM-PTmDZqdJaEbNUA; __mbox_csrf_token=KoZ2gZluKKRE83Z4_1591866401301",
                        # "origin": "https://widget.1688.com",
                        # "pragma": "no-cache",
                        "referer": "https://widget.1688.com/front/ajax/bridge.html?target=brg-106239",
                        # "sec-fetch-dest": "empty",
                        # "sec-fetch-mode": "cors",
                        # "sec-fetch-site": "same-origin",
                        "User-Agent": ua.random,
                        # "x-requested-with":"XMLHttpRequest"
                    }
                    r = requests.post('https://widget.1688.com/front/ajax/getJsonComponent.json',headers=headers,proxies=proxies,verify=False,data=data,timeout=(6.05, 27.05))
                    r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
                except requests.RequestException as e:
                    print(e)
                    continue
                print("接口请求响应状态:"+str(r.status_code))
                print(r.text)
                res = json.loads(r.text)
                productRecordList =res['content']['result'][0]['data']['list']

                #分页数据不存在则跳出
                if len(productRecordList) <= 0:
                    print("当前分页没有可处理的商品数据，跳出")
                    break
                #=============================不存在当前型号============================
                #新增数据数组
                inset_data = []
                # =============================存在当前型号============================
                # 更新数据数组
                update_data = []
                company_info_id_arr = []
                j = 1;#当前处理条数
                productId_arr = data_arr_key(productRecordList,'company_info_id')
                szlcsc_goods_sale_arr = szlcsc_goods_sale_where_in_arr(productId_arr)
                for iii in productRecordList:
                    try:
                        r = requests.post(
                            'http://dynamic.goubanjia.com/dynamic/get/787b33d192b9275f9e6b1acd88c015a1.html?sep=6',
                            timeout=(6.05, 27.05))
                        r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
                        if r.text.strip(';'):
                            proxies = {"http": "http://" + str(r.text.strip(';')),
                                       "https": "https://" + str(r.text.strip(';'))}
                        else:
                            print("代理失效")
                            exit()
                    except requests.RequestException as e:
                        print(e)
                        continue

                    #====================================数据处理==================================
                    company_info_name = iii['company'].strip()
                    company_info_id = hashlib.md5(company_info_name.encode(encoding='UTF-8')).hexdigest()
                    create_time = now
                    update_time = now
                    task_id = task_info[0]
                    main_products = ''
                    brand_name = ''
                    email = ''
                    business_category=''

                    try:
                        szlcsc_goods_sale_info = szlcsc_goods_sale_arr['1688_'+str(company_info_id)]
                    except Exception  as result:
                        szlcsc_goods_sale_info = []
                    if not len(szlcsc_goods_sale_info):
                        if company_info_id in company_info_id_arr:
                            j += 1  #
                            print(company_info_name)
                            continue
                        company_info_id_arr.append(company_info_id);

                        print("===========================正在处理第" + str(j) + "条数据" + str(company_info_name))
                        try:
                            headers = {
                                "User-Agent": ua.random,
                            }

                            detail = 'https://detail.1688.com/offer/'+str(iii['offerId'])+'.html'
                            print(detail)
                            email_r = requests.get(detail, headers=headers, data={}, proxies=proxies, verify=False,
                                                   timeout=(12.05, 27.05))
                            email_r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
                            email_bs = BeautifulSoup(email_r.text, "html.parser")
                            # if email_bs.find(class_="contactinfo-page") == None:
                            #     print("===========================无联系方式，跳过不处理"+email_bs.find(class_="contactinfo-page"))
                            #     j += 1  #
                            #     continue
                            if  email_bs.find(class_='mod-contactSmall') != None:
                                print("详情页有联系方式")
                                lxr_people = email_bs.find(class_='mod-contactSmall').find(class_="membername").text
                                print(email_bs.find(class_="mod-contactSmall").get('data-view-config'))
                                address = email_bs.find(class_="mod-contactSmall").get('data-view-config')
                                address = address.replace('true', '1')
                                address = eval(address)
                                address = address['address']
                                lxr_tel = '';
                                lxr_phone = '';
                                address = ''
                                href = ''
                                for p in email_bs.find(class_='mod-contactSmall').find(class_="m-content").find_all('dl'):
                                    if p.find('dt').string != None:
                                        if p.find('dt').string.strip().startswith('电'):
                                            lxr_tel = p.find('dd').text.strip()
                                        # if p.find('dt').string.strip().startswith('地'):
                                        #     address = p.find('dd').text.strip()
                                        if p.find('dt').string.strip().startswith('移动电话'):
                                            lxr_phone = p.find('dd').text.strip()
                                        # if p.find('dt').string.strip().startswith('公司主页'):
                                        #     href = p.find('dd').text.strip()
                                href = email_bs.find(class_="index-page").find('a').get('href')
                                user_name = urlsplit(href).netloc.split('.')[0]
                                from_url = href
                            else:
                                print("详情页无联系方式，查看联系方式页是否有联系方式")
                                if email_bs.find(class_="contactinfo-page") == None:
                                    print("===========================无联系方式，跳过不处理")
                                    j += 1  #
                                    continue
                                contactinfo_page = email_bs.find(class_="contactinfo-page").find('a').get('href')
                                print(contactinfo_page)
                                headers = {
                                    "cookie": 'cna=xTr3FsPSoy4CAXkPB3n64Khu; UM_distinctid=17297aa564a74e-0ed0e7c41ce1fa-f7d1d38-1fa400-17297aa564b7a3; _csrf_token=1591682454281; taklid=654f531b949446a79af92c7f38e01dab; cookie2=1db9057217a3de624732cef46eefac80; hng=CN%7Czh-CN%7CCNY%7C156; t=2993b253a990044dadf2982c45a16332; _tb_token_=7770be5e3f987; lid=tiamomeixiao; uc4=id4=0%40UOnnEYTvD%2B2H1GSBKeFw4tR7mNfb&nk4=0%40FYWuvJYXpROYxzGk2FKININLCZQOSpk%3D; __cn_logon__=false; ali_beacon_id=119.137.53.121.1591682459304.685326.9; _m_h5_tk=cfc25ce2d5b2b815e9dde13aa67de954_1591694415938; _m_h5_tk_enc=81d3919faa445de8da7d0c9e5c5e356e; h_keys="%u5143%u5668%u4ef6#%u4e8c%u6781%u7ba1#%u534a%u5bfc%u4f53"; ad_prefer="2020/06/09 14:46:35"; alicnweb=touch_tb_at%3D1591690635462; l=eBab1QUgQWP6CTeCBOfanurza77OSIRYouPzaNbMiOCPOTfk5mQNWZvhU58DC3GVh6bJR35QyF6TBeYBqnbfb0Iqn6X5WNHmn; isg=BMTEv6HORmgTNvIjflurBrTolUK23ehHWviq_N5lUA9SCWTTBu241_qrSaHRFyCf',
                                    "User-Agent": ua.random,
                                }
                                company_info_r = requests.get(contactinfo_page, data={}, headers=headers, proxies=proxies,
                                                              verify=False, timeout=(6.05, 27.05))
                                company_info_r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
                                company_info_bs = BeautifulSoup(company_info_r.text, "html.parser")
                                lxr_people = company_info_bs.find(class_="contact-info").find(class_='membername').text
                                lxr_tel = '';
                                lxr_phone = '';
                                address = ''
                                href = ''
                                for p in company_info_bs.find(class_="contcat-desc").find_all('dl'):
                                    if p.find('dt').string != None:
                                        if p.find('dt').string.strip().startswith('电'):
                                            lxr_tel = p.find('dd').text.strip()
                                        if p.find('dt').string.strip().startswith('地'):
                                            address = p.find('dd').text.strip()
                                        if p.find('dt').string.strip().startswith('移动电话'):
                                            lxr_phone = p.find('dd').text.strip()
                                        if p.find('dt').string.strip().startswith('公司主页'):
                                            href = p.find('dd').text.strip()
                                user_name = urlsplit(href).netloc.split('.')[0]
                                from_url = href
                        except Exception  as result:
                            print(result)
                            continue
                        inset_tmp = {
                            'company_info_id':'1688_'+str(company_info_id),
                            'company_info_name': db.conn.escape_string(company_info_name),
                            'address':address,
                            'user_name':user_name,
                            'email': '',
                            'lxr_tel': db.conn.escape_string(lxr_tel),
                            'lxr_phone': db.conn.escape_string(lxr_phone),
                            'lxr_people':db.conn.escape_string(lxr_people),
                            'brand_name':brand_name,
                            'business_category':db.conn.escape_string(business_category),
                            'main_products': db.conn.escape_string(main_products),
                            'from_url': db.conn.escape_string(from_url),
                            'create_time': now,
                            'task_id':task_info[0],
                            'desc':'新增型号',# '新增型号',
                        }
                        inset_data.append(tuple(list(inset_tmp.values())))
                        print("===========================为新增公司信息追加到插入队列中")
                    elif int(szlcsc_goods_sale_info[14]) == int(task_info[0]):
                        print("company_info_id:"+str(szlcsc_goods_sale_info[1])+":已更新为当前任务版本 不重复处理，跳出")
                        j += 1  #
                        continue
                    else:
                        print("===========================已存在当前公司信息，跳过不处理")
                        j += 1  #
                        continue
                    print("===========================数据处理完成")
                    j+=1#当前处理条数加一

                #存在新增型号
                if len(inset_data) > 0:
                    try:
                        db.connect()
                        #商品数据插入
                        sql = "INSERT INTO cj_collection_company (`company_info_id`,`company_info_name`,`address`, `user_name`, `email`" \
                              ",`lxr_tel`, `lxr_phone`, `lxr_people`,`brand_name`, `business_category`, `main_products`, `from_url`" \
                              ", `create_time`, `task_id`, `desc`)" \
                              " VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s);"
                        print(inset_data)
                        results = db.cursor.executemany(sql, inset_data)
                        if results == None:
                            # 创建异常对象
                            ex = Exception("===================插入公司数据失败")
                            # 抛出异常对象
                            raise ex
                        print('===================公司数据数据插入成功')
                        db.conn.commit()
                        db.close()
                    except Exception  as result:
                        print('===================数据插入异常',result)
                        db.connect()
                        db.conn.rollback()
                        db.close()
                        exit()

                category_page_sql = "UPDATE `cj_1688_category` SET `page` =  `page`+1 ,`update_time`='"+str(now)+"'  WHERE(`id` = '" + str(i[0]) + "')"
                category_page_results = db.update(category_page_sql, ())
                if category_page_results == None:
                    print('==========================处理分页变更失败')
                    break
                print('==========================处理分页变更成功')

                #处理完一页出具延迟10秒
                print('==========================延时等待2秒钟再处理')
                for n in range(5):
                    print("3秒倒计时==========================" + str(5 - n)),
                    time.sleep(1)

                ii+=1

            category_sql = "UPDATE `cj_1688_category` SET `status` = '2',`update_time`='"+str(now)+"'  WHERE(`id` = '"+str(i[0])+"')"
            category_results = db.update(category_sql,())
            if category_results == None:
                print('==========================分类任务状态处理失败')
                break
            print('=====================分类任务变更成功，处理下一个分类')

        task_sql = "UPDATE `cj_collection_company_task` SET `status` = '2',`update_time`='" + str(
            now) + "'  WHERE(`task_id` = '" + str(task_info[0]) + "')"
        task_results = db.update(task_sql, ())
        if task_results == None:
            print('==========================任务状态处理失败')

        print('=====================任务变更成功，处理完成')
    # except Exception  as result:
    #     print('==========================程序运行异常')
    #     print(result)

#回去数组指定key值
def data_arr_key(arr,key):
    if len(arr) <= 0:
        return None;
    reurn_arr=[]

    for iii in arr:
        if iii['company']:
            id = iii['company']
            id = hashlib.md5(id.encode(encoding='UTF-8')).hexdigest()
            reurn_arr.append('1688_'+str(id))
    return reurn_arr


def szlcsc_goods_sale_where_in_arr(arr):
    if not arr:
        return arr
    db = mysql(host=mysql_config['host'], user=mysql_config['user'], password=mysql_config['password'],db=mysql_config['db'])
    select_sql = 'select * from cj_collection_company where company_info_id in (%s)'
    in_p = ', '.join((map(lambda x: '%s', arr)))
    reurn_arr = db.get_all(select_sql % in_p, arr)
    #print(reurn_arr)
    tmp = {}
    for i in reurn_arr:
        tmp[str(str(i[1]))] = i
    return tmp

if __name__ == '__main__':
    cj_task()
    data_goodslist()



