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

mysql_config = {'host':'106.14.127.145', 'user':'kaifa', 'password':'yB8FtzFSlSa5QYE0vzd8','db':'jzic_crawl_data'}
#d当前时间
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
location = 'file/气象数据家园/fake_useragent.json'
ua = UserAgent(path=location)

def data_category():
    db = mysql(host=mysql_config['host'], user=mysql_config['user'], password=mysql_config['password'],db=mysql_config['db'])

    url = 'https://www.hc360.com/'
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    bs = BeautifulSoup(response.text, "html.parser")
    category_level_1 = bs.find(class_="item_Vlist").find(attrs={'data-name':'电子智能硬件'}).find(class_='sideBarLeft').find_all('a')
    if(len(category_level_1) <=0):
        print("分类数据不存在")
        return False;

    #查询版本信息
    szlcsc_task_info = db.get_one("SELECT * FROM `cj_collection_company_task` where status = 1 and name = '慧聪网数据采集' ORDER BY `task_id` DESC LIMIT 1", params=())
    if szlcsc_task_info == None:
        print(szlcsc_task_info)
        print("任务不存在")
        return False;
    cj_szlcsc_category_list = db.get_one("SELECT * FROM `cj_hc360_category` where category_level = 2 and status = 1 and task_id = " + str(szlcsc_task_info[0]) + "  LIMIT 1", params=())
    if cj_szlcsc_category_list :
        print("已经更新为当前版本分类数据")
        return False;
    #分类数据
    category= [];
    for ii in category_level_1:
        data = {
            'pid': 0,
            'name': ii.text,
            'goods_num':0,
            'category_level': 2,
            'from_url': db.conn.escape_string(ii.get('href')),
            'create_time': now,
            'task_id': szlcsc_task_info[0],
        }
        response = requests.get(ii.get('href'))
        response.encoding = response.apparent_encoding
        bs = BeautifulSoup(response.text, "html.parser")
        if bs:
            goods_num = bs.find(class_="item_r").find('em').text
            data['goods_num'] = goods_num;
        else:
            data['goods_num'] = 0;
        print(data)
        category.append(tuple(list(data.values())))

    if (len(category) <= 0):
        print("没有可提交的数据")
        return False;

    print(category)
    try:
        #先清除分类数据，重新爬取最新数据
        category_sql = " truncate  table cj_hc360_category;"
        category_results = db.edit(category_sql, ())
        #print(category_results)
        if category_results == None:
            # 创建异常对象
            ex = Exception("清除分类数据失败")
            # 抛出异常对象
            raise ex

        sql = "INSERT INTO cj_hc360_category (`pid`,`name`,`goods_num`,`category_level`,`from_url`,`create_time`,`task_id`) VALUES ( %s, %s, %s, %s, %s, %s, %s);"
        results = db.insert(sql,category)
        print(results)
        if results == None: 
            # 创建异常对象
            ex = Exception("插入分类数据失败")
            # 抛出异常对象
            raise ex

    except Exception  as result:
        print(result)
        db.connect()
        db.conn.rollback()


#任务处理
def cj_task():
    db = mysql(host=mysql_config['host'], user=mysql_config['user'], password=mysql_config['password'],db=mysql_config['db'])
    # 查询版本信息
    task_info = db.get_one("SELECT * FROM `cj_collection_company_task` where status = 1 and name='慧聪网数据采集' ORDER BY `task_id` DESC LIMIT 1",params=())
    if task_info:
        print("存在未处理完的任务继续处理")
    else:
        try:
            inset_data = ('慧聪网数据采集', '慧聪网数据采集系统自动新增任务', now, 1)
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

        task_info = db.get_one("SELECT * FROM `cj_collection_company_task` where status = 1 and name = '慧聪网数据采集' ORDER BY `task_id` DESC LIMIT 1", params=())
        if not task_info or task_info == None:
            print("任务不存在")
            return False;

        #加1为当前处理版本
        cj_szlcsc_category_list = db.get_all("SELECT * FROM `cj_hc360_category` where category_level = 2 and status = 1 and task_id = "+str(task_info[0])+"  ", params=())
        if not cj_szlcsc_category_list or cj_szlcsc_category_list == None:
            print("本地版本没有需要处理的数据")
            return False;


        for i in cj_szlcsc_category_list:
            #总页数
            pagenun = math.ceil(i[3]/60)
            print("=============================正在处理分类："+str(i[2])+"总共******"+str(pagenun)+"******页，每页30条")
            p =i[10]+1
            for ii in  range(p,pagenun+1):
                # nf = open("/home/wwwroot/www/log.txt", "w")
                # nf.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                # nf.close()
                print("=============================正在处理分类：" + str(i[2]) + "正在处理第******"+str(ii)+"******页的数据")
                try:
                    # proxies = {
                    #     "http": "112.95.205.2:9999",
                    # }
                    #proxies=proxies
                    r = requests.post(i[5]+'&pnum='+str(ii)+'&ee='+str(ii),data={},timeout=(6.05, 27.05))
                    r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
                except requests.RequestException as e:
                    print(e)
                    continue
                print("接口请求响应状态:"+str(r.status_code))
                bs = BeautifulSoup(r.text, "html.parser")
                productRecordList = bs.find_all(class_="grid-list")
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
                    #====================================数据处理==================================
                    try:
                        company_info_name = iii.find(class_="newCname").find('p').find('a').text.strip()
                        print("===========================正在处理第" + str(j) + "条数据" + str(company_info_name) )
                        company_info_id = iii.get('data-sellerproviderid')
                        user_name = iii.find('div',class_="NewItem").get('data-username')
                        href ="https://"+str(user_name)+".b2b.hc360.com/"
                        user_name = urlsplit(href).netloc.split('.')[0]
                        lxr_phone = iii.get('data-telphone');

                        from_url = href
                        create_time = now
                        update_time = now
                        task_id = task_info[0]
                        brand_name = ''
                        business_category = iii.find('div',class_="NewItem").get('data-obj')
                        main_products = iii.find('div', class_="NewItem").get('data-kind')


                    except Exception  as result:
                        print(result)
                        # continue
                    # ================================数据处理==================================
                    # print(address)
                    # exit()

                    try:
                        szlcsc_goods_sale_info = szlcsc_goods_sale_arr['hc360_'+str(company_info_id)]
                    except Exception  as result:
                        szlcsc_goods_sale_info = []
                    if not len(szlcsc_goods_sale_info):
                        if company_info_id in company_info_id_arr:
                            j += 1  #
                            print(company_info_name)
                            continue

                        company_info_id_arr.append(company_info_id);

                        # 公司信息
                        lxr_people = ''
                        lxr_tel = ''
                        address = ''
                        # try:
                        Host = href.replace('https:', '')
                        Host = Host.replace('/', '')
                        headers = {
                            'Host': Host,
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
                            'Referer': href
                        }
                        print(headers)
                        print(href)
                        email_r = requests.get(href + 'shop/company.html', headers=headers, timeout=(6.05, 27.05))
                        # email_r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
                        email_bs = BeautifulSoup(email_r.text, "html.parser")
                        if (email_bs.find(class_="ContacCon3") != None):
                            for li in email_bs.find(class_="ContacCon3").find_all('li'):
                                if li.find(class_="con3Left") != None:
                                    if li.find(class_="con3Left").text.strip().startswith('联系人'):
                                        lxr_people = li.find(class_="con3Rig").find('a').text.strip()
                                    if li.find(class_="con3Left").text.strip().startswith('电话'):
                                        lxr_tel = li.find(class_="con3Rig").text.strip()
                                    if not lxr_phone:
                                        if li.find(class_="con3Left").text.strip().startswith('手机'):
                                            lxr_phone = li.find(class_="con3Rig").text.strip()
                                    if li.find(class_="con3Left").text.strip().startswith('地址'):
                                        address = li.find(class_="con3Rig").text.strip()

                        inset_tmp = {
                            'company_info_id':'hc360_'+str(company_info_id),
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

                category_page_sql = "UPDATE `cj_hc360_category` SET `page` =  `page`+1 ,`update_time`='"+str(now)+"'  WHERE(`id` = '" + str(i[0]) + "')"
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

            category_sql = "UPDATE `cj_hc360_category` SET `status` = '2',`update_time`='"+str(now)+"'  WHERE(`id` = '"+str(i[0])+"')"
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
        id = iii.get('data-sellerproviderid')
        reurn_arr.append('hc360_'+str(id))
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
    data_category()
    data_goodslist()



