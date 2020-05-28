#coding=utf-8
import requests
import json
import csv
import time
import datetime

import MySQLdb
import pymysql

from fake_useragent import UserAgent

from datetime import timedelta
# from selenium import webdriver
# from bs4 import BeautifulSoup
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver import ActionChains

#
# url 中的经纬度去掉了，可以自行查询添加需要爬取地点的经纬度，也可以通过调用地图api获取经纬度；
#
# headers 需要加 Cookies ，不然会有登录权限限制爬取页数；

def get_page(page):
    location = 'file/气象数据家园/fake_useragent.json'
    ua = UserAgent(path=location)
    try:
        url = 'https://h5.ele.me/restapi/shopping/v3/restaurants?latitude=22.54286&longitude=114.059563&offset={page}&limit=8&terminal=h5'.format(page=page*8)
        print("==========================正在处理 第" + str(page)  + "页数据")

        print(url)
        headers = {
            "user-agent": ua.random,
        }
        cookies = {
            'SID': '8jrj6HtJFzs2TB3b290Lq4YMP4tLhjDUG34w29',
            # 'USERID':'220292471',
            # 'UTUSER':'220292471',
            # 'ubt_ssid':'ird3ymxqtdnhk5c2cs1y33ka357lt0zq_2020-04-14',
            # 'ut_ubt_ssid':'zckkempirwt1ieeqcf59hhb35bszwwuw_2020-04-14',
            # '__wpkreporterwid_':'f88a687f-fe7e-4838-af68-6389ab4a5f3a',
            # '_bl_uid': 'bskn08qwz2jiv2hLgb2CvwRaUkFd',
            # 'perf_ssid': '83lz0ldhbe4xk4rfvd73its4u1xod881_2020-04-14',
            'x5sec': '7b227466653b32223a223461393234323965373461323236313861393637666364613739623338633633434e6178322f5146454e502f384b4843764f753057686f4d4d6a49774d6a6b794e4463784f7a4578227d',#这个是滑动验证码，出现滑动了需要更新他
        }
        response = requests.get(url, headers=headers, cookies=cookies,timeout=(6.05, 27.05))
        response.raise_for_status()

        response.encoding = response.apparent_encoding

        re = json.loads(response.text)
        if 'rgv587_flag' in re:
            # options = Options()
            # options.add_argument('--headless')
            # driver = webdriver.Chrome(executable_path="D:\chromedriver", options=options)
            # driver.get(re['url'])
            # time.sleep(2)
            # action = ActionChains(driver)
            # source = driver.find_element_by_css_selector("#nc_1_n1z")# 需要滑动的元素
            # time.sleep(2)
            # action.click_and_hold(source).perform() # 鼠标左键按下不放
            # time.sleep(4)
            # action.move_by_offset(1357, 381)  # 需要滑动的坐标
            # action.release().perform()  # 释放鼠标
            print(re)
            print('访问超时')
            time.sleep(5)
            exit()

    except  requests.RequestException as e:
        print(json.loads(response.text))
        print(e)
        exit()
    re = json.loads(response.text)

    # # 建立csv文件，保存数据
    # csvFile = open(r'file/饿了么/senlin_down.csv', 'a+', newline='', encoding='utf_8_sig')
    # # csvFile.write(codecs.BOM_UTF8)
    # writer = csv.writer(csvFile)
    # writer.writerow(('名称', '月销售量','配送费', '起送价', '风味', '评分', '配送时长', '评分统计', '距离', '地址'))


    data_list = []
    productId_arr = data_arr_key(re.get('items'), 'id')
    ci_elm_data_arr = ci_elm_data_where_in_arr(productId_arr)

    p = 1
    has_next = re.get('has_next')
    print("has_next%s"%has_next)
    for item in re.get('items'):
        restaurant = item.get('restaurant')
        print("==========================正在处理" + str(restaurant.get('name'))  + " 第" + str(p)  + "数据")

        # d当前时间
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        headers = {
            "user-agent":ua.random,
           "cookie":'cna=xTr3FsPSoy4CAXkPB3n64Khu; ubt_ssid=ird3ymxqtdnhk5c2cs1y33ka357lt0zq_2020-04-14; _utrace=da7f038dd5e3eae5b97ab5f35aad6a89_2020-04-14; __wpkreporterwid_=f88a687f-fe7e-4838-af68-6389ab4a5f3a; perf_ssid=83lz0ldhbe4xk4rfvd73its4u1xod881_2020-04-14; ut_ubt_ssid=zckkempirwt1ieeqcf59hhb35bszwwuw_2020-04-14; _bl_uid=bskn08qwz2jiv2hLgb2CvwRaUkFd; track_id=1586845016|853fdd20b910ac77083161a8a1f9507ba55e36d6aa640d9964|dde6f3ffc120bca6e42b3a5c804f4946; USERID=220292471; UTUSER=220292471; tzyy=afc371ee6d5334eef14db3387c3d00a8; ZDS=1.0|1586845068|6IYsYKL4WFhF5SLkMlar+yjjtkQOdCPYGJ1Ugx4F7+gsS1WysK8wUKMXKuxsKcYo; _samesite_flag_=true; cookie2=1de4e9a2c6cac49b5996113ef1d4ab38; t=bf25132472f2d168aedf10601a859345; _tb_token_=e3a1e1ee983ee; munb=2204636879897; csg=a3843ea2; t_eleuc4=id4=0%40BA%2FvuHCrrRkcV6zD4F72sYFWyIWXOndxM8C1Lw%3D%3D; SID=8jrj6HtJFzs2TB3b290Lq4YMP4tLhjDUG34w29; x5check_ele=RcimLIFLTAuNH3cDWUdrZKmi9J0s%2BZP6TV1HQXiqy0Y%3D; l=eBxmaEu4QpybVsXKBO5i-V-11A7T3IOb4sPrQGmG7IHca6G1_FmG2OQcU-Py8dtjgt13vetPZ7K-WRLHR3fRwxDDBti2PH-Enxf..; isg=BFVVhzSapwKFwoN9DT8e_wtQZFEPUglkXr0AjNf6EUwbLnUgn6IZNGPk_DSYLiEc; x5sec=7b227466653b32223a2262616538306139333361393132316239623864313637663239363832396436314349534e322f51464550586f344c76546b59627236674561437a49794d4449354d6a51334d547334227d'
        }
        try:
            response = requests.get('https://h5.ele.me/pizza/shopping/restaurants/'+str(restaurant.get('id'))+'/batch_shop?extras=%5B"activities"%2C"albums"%2C"license"%2C"identification"%2C"qualification"%5D&latitude='+str(restaurant.get('latitude'))+'&longitude='+str(restaurant.get('longitude')), headers=headers, timeout=(6.05, 27.05))
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            re = json.loads(response.text)
            if 'rgv587_flag' in re:
                print(re)
                print('访问超时')
                continue

            phone_response = requests.get('https://h5.ele.me/restapi/giraffe/restaurant/phone?shopId='+str(restaurant.get('id')),headers=headers, timeout=(6.05, 27.05))
            phone_response.raise_for_status()
            phone_response.encoding = phone_response.apparent_encoding
            phone_response_re = json.loads(phone_response.text)
            if 'rgv587_flag' in phone_response_re:
                print(phone_response_re)
                print('访问超时')
                continue
        except  requests.RequestException as e:
            print(e)
            continue

        rst = re.get('rst')
        if not rst.get('activities') == None:
            activities = ''
            j = 1;
            for activities_item in rst.get('activities'):
                activities += str(j)+":"+activities_item['description']+";"
                j += 1

        if not rst.get('flavors') == None:
            category = ''
            for category_item in rst.get('flavors'):
                category += category_item.get('name') + "|"

        if not phone_response_re == None:
            phone = ''
            j = 1;
            for phone_item in phone_response_re:
                phone += str(j)+":"+phone_item.get('numbers')[0]+";"
                j += 1

        try:
            ci_elme_info = ci_elm_data_arr[str(restaurant.get('id'))]
        except Exception  as result:
            ci_elme_info = []

        if not len(ci_elme_info):
            data = {
                'e_id':restaurant.get('id'),
                'shop_name': restaurant.get('name'),
                'address': rst.get('address'),
                'longitude': restaurant.get('longitude'),
                'latitude': restaurant.get('latitude'),
                'category':  category,
                'delivery': rst.get('delivery_mode').get('text'),
                'phone': phone,
                'business_hours': rst.get('opening_hours')[0],
                'recent_sales_volume': restaurant.get('recent_order_num'),
                'activity': activities,
                'initial_delivery_price': restaurant.get('float_minimum_order_amount'),
                'distribution_fee': restaurant.get('float_delivery_fee'),
                'score': restaurant.get('rating'),
                'score_statistics': restaurant.get('rating_count'),
                'distance': restaurant.get('distance'),
                'createtime': now,
            }
            data_list.append(tuple(list(data.values())))
        else:
            print('商铺数据已存在')
        p+=1

    # 存在新增型号
    if len(data_list) > 0:
        db = MySQLdb.connect("localhost", "root", "root", "jzic_crawl_data_v2", charset='utf8')
        cursor = db.cursor()
        try:
            # 商品数据插入
            sql = "INSERT INTO ci_elm_data (`e_id`,`shop_name`, `address`, `longitude`" \
                  ",`latitude`, `category`, `delivery`, `phone`, `business_hours`, `recent_sales_volume`" \
                  ", `activity`, `initial_delivery_price`, `distribution_fee`, `score`, `score_statistics`, `distance`, `createtime`)" \
                  " VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s);"
            print(data_list)
            # results = db.insert(sql, inset_data)
            results = cursor.executemany(sql, data_list)
            if results == None:
                # 创建异常对象
                ex = Exception("===================插入数据失败")
                # 抛出异常对象
                raise ex
            print('===================数据插入成功')
            db.commit()
            db.close()
        except Exception  as result:
            print('===================数据插入异常', result)
            db.rollback()
            db.close()
            exit()

    if has_next == True:
        print("处理下一页")
        get_page(page + 1)


#回去数组指定key值
def data_arr_key(arr,key):
    if len(arr) <= 0:
        return arr
    reurn_arr=[]
    for item in arr:
        restaurant = item.get('restaurant')
        reurn_arr.append(restaurant.get('id'))
    return reurn_arr


def ci_elm_data_where_in_arr(arr):
    if not arr:
        return arr
    db = MySQLdb.connect("localhost", "root", "root", "jzic_crawl_data_v2", charset='utf8')
    cursor = db.cursor()
    select_sql = 'select * from ci_elm_data where e_id in (%s)'
    in_p = ', '.join((map(lambda x: '%s', arr)))
    cursor.execute(select_sql % in_p,arr)
    # 获取所有记录列表
    reurn_arr = cursor.fetchall()
    #print(reurn_arr)
    tmp = {}
    for i in reurn_arr:
        tmp[str(str(i[1]))] = i

    #print ('430523' in tmp.keys())
    return tmp


get_page(0)