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

#任务处理
def cj_task():
    db = mysql(host=mysql_config['host'], user=mysql_config['user'], password=mysql_config['password'],db=mysql_config['db'])
    # 查询版本信息
    task_info = db.get_one("SELECT * FROM `cj_collection_company_task` where status = 1 ORDER BY `task_id` DESC LIMIT 1",params=())
    if task_info:
        print("存在未处理完的任务继续处理")
    else:
        try:
            inset_data = ('华强电子网数据采集', '华强电子网数据采集系统自动新增任务', now, 1)
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
    try:
        db = mysql(host=mysql_config['host'], user=mysql_config['user'], password=mysql_config['password'],db=mysql_config['db'])

        task_info = db.get_one("SELECT * FROM `cj_collection_company_task` where status = 1 and name = '华强电子网数据采集' ORDER BY `task_id` DESC LIMIT 1", params=())
        if not task_info or task_info == None:
            print("任务不存在")
            return False;

        #加1为当前处理版本
        cj_szlcsc_category_list = db.get_all("SELECT * FROM `cj_hqew_category` where category_level = 1 and status = 1 and task_id = "+str(task_info[0])+"", params=())
        if not cj_szlcsc_category_list or cj_szlcsc_category_list == None:
            print("本地版本没有需要处理的数据")
            return False;

        for i in cj_szlcsc_category_list:
            #总页数
            pagenun = math.ceil(i[3]/30)
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
                    r = requests.post(i[5]+'__________'+str(ii)+'.html',data={},timeout=(6.05, 27.05))
                    r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
                except requests.RequestException as e:
                    print(e)
                    continue
                print("接口请求响应状态:"+str(r.status_code))
                bs = BeautifulSoup(r.text, "html.parser")
                productRecordList = bs.find_all(class_="company-info")
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

                j = 1;#当前处理条数
                productId_arr = data_arr_key(productRecordList,'company_info_id')
                szlcsc_goods_sale_arr = szlcsc_goods_sale_where_in_arr(productId_arr)
                for iii in productRecordList:
                    print("===========================正在处理第"+str(j)+"条数据")

                    #================================数据处理==================================
                    try:
                        company_info_name = iii.find(class_="max-company").text.strip()
                        company_info_id = iii.find(class_="max-company").get('uid')
                        href = iii.find(class_="max-company").get('href')
                        user_name = urlsplit(href).netloc.split('.')[0]
                        from_url = href

                        lxr_tel = '';
                        lxr_people = ''
                        address = ''
                        brand_name = ''
                        business_category = ''
                        main_products = ''
                        li_i=0
                        for p in iii.find("ul").find_all('li'):
                            if li_i == 1:
                                brand_name = p.find('p').get('title')
                            if li_i == 2:
                                business_category = p.find('p').get('title')
                            if li_i == 3:
                                main_products = p.find('p').get('title')
                            if li_i == 5:
                                lxr_people_arr= p.find('span').text.split('，')
                                for people in lxr_people_arr:
                                    people_tmp = ''.join(re.findall('[\u4e00-\u9fa5]', people))
                                    lxr_people = lxr_people + '||' +people_tmp
                                    lxr_tel = lxr_tel + '||' + str(people.strip().replace(people_tmp, '').strip())
                            if li_i == 6:
                                address = p.find('p').get('title')
                            li_i+=1
                        lxr_tel = lxr_tel.strip('||')
                        lxr_people = lxr_people.strip('||')

                        email = ''
                        lxr_phone = ''
                        #请求邮箱
                        try:
                            headers = {
                                "user-agent": ua.random,
                            }
                            email_r = requests.get('http://zongxinda.hqew.com/',headers=headers, data={}, timeout=(6.05, 27.05))
                            email_r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
                            email_bs = BeautifulSoup(email_r.text, "html.parser")
                            if(email_bs.find(class_="company-info-contact") != None):
                                for li in email_bs.find(class_="company-info-contact").find_all('li'):
                                    if li.find(class_="contact-tit").string != None:
                                        if li.find(class_="contact-tit").string.strip().startswith('手'):
                                            lxr_phone = lxr_phone + '||' + str(li.find('div').text)
                                        if li.find(class_="contact-tit").string.strip().startswith('Email'):
                                            email = email + '||' + str(li.find('div').text)
                            elif (email_bs.find(class_="panel-bd pr-0") != None):
                                for li in email_bs.find(class_="panel-bd pr-0").find_all('li'):
                                    if li.find(class_="contact-tit").string != None:
                                        if li.find(class_="contact-tit").string.strip().startswith('手'):
                                            lxr_phone = lxr_phone + '||' + str(li.find('div').text)
                                        if li.find(class_="contact-tit").string.strip().startswith('Email'):
                                            email = email + '||' + str(li.find('div').text)
                        except requests.RequestException as e:
                            email = ''
                            lxr_phone = ''
                    except Exception  as result:
                        print(result)
                        continue

                    lxr_phone = lxr_phone.strip('||')
                    email = email.strip('||')

                    # ================================数据处理==================================

                    try:
                        szlcsc_goods_sale_info = szlcsc_goods_sale_arr['hqew_'+str(company_info_id)]
                    except Exception  as result:
                        szlcsc_goods_sale_info = []
                    if not len(szlcsc_goods_sale_info):
                        inset_tmp = {
                            'company_info_id':'hqew_'+str(company_info_id),
                            'company_info_name': db.conn.escape_string(company_info_name),
                            'address':address,
                            'user_name':user_name,
                            'email': db.conn.escape_string(email),
                            'lxr_tel': db.conn.escape_string(lxr_tel),
                            'lxr_phone': db.conn.escape_string(lxr_phone),
                            'lxr_people':db.conn.escape_string(lxr_people),
                            'brand_name':db.conn.escape_string(brand_name),
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
                        j += 1  # 当前处理条数加一
                        continue
                    else:
                        print("===========================已存在当前公司信息，跳过不处理")
                        j += 1  # 当前处理条数加一
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

                category_page_sql = "UPDATE `cj_hqew_category` SET `page` =  `page`+1 ,`update_time`='"+str(now)+"'  WHERE(`id` = '" + str(i[0]) + "')"
                category_page_results = db.update(category_page_sql, ())
                if category_page_results == None:
                    print('==========================处理分页变更失败')
                    break
                print('==========================处理分页变更成功')

                #处理完一页出具延迟10秒
                print('==========================延时等待5秒钟再处理')
                for n in range(3):
                    print("3秒倒计时==========================" + str(3 - n)),
                    time.sleep(1)

            category_sql = "UPDATE `cj_hqew_category` SET `status` = '2',`update_time`='"+str(now)+"'  WHERE(`id` = '"+str(i[0])+"')"
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
    except Exception  as result:
        print('==========================程序运行异常')
        print(result)

#回去数组指定key值
def data_arr_key(arr,key):
    if len(arr) <= 0:
        return None;
    reurn_arr=[]
    for iii in arr:
        id = iii.find(class_="max-company").get('uid')
        reurn_arr.append('hqew_'+str(id))
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
    # 判断商品是否存在
    # def is_in_szlcsc_goods_sale_arr(arr, key):
    cj_task()
    data_goodslist()
    # szlcsc_goods_sale_where_in_arr()


