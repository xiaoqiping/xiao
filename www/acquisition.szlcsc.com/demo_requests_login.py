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

#d当前时间
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def data_category():
    db = mysql()

    url = 'https://www.szlcsc.com/catalog.html'
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    bs = BeautifulSoup(response.text, "html.parser")
    category_level_1 = bs.find(class_="page-www-catalog").find_all('dl')

    if(len(category_level_1) <=0):
        print("分类数据不存在")
        return False;

    #查询版本信息
    szlcsc_task_info = db.get_one("SELECT * FROM `cj_szlcsc_task` where status = 1 ORDER BY `task_id` DESC LIMIT 1", params=())
    if szlcsc_task_info == None:
        print(szlcsc_task_info)
        print("任务不存在")
        return False;

    cj_szlcsc_category_list = db.get_one("SELECT * FROM `cj_szlcsc_category` where category_level = 2 and status = 1 and task_id = " + str(szlcsc_task_info[0]) + "  LIMIT 1", params=())
    if cj_szlcsc_category_list :
        print("已经更新为当前版本分类数据")
        return False;
    #分类数据
    category= [];
    for i in category_level_1:
        data = {
            'id': 0,
            'pid': 0,
            'name': i.find('dt').find('a').text,
            'goods_num':0,
            'category_level': 1,
            'from_url': i.find('dt').find('a').get('href'),
            'create_time': now,
            'task_id': szlcsc_task_info[0],
        }
        id = re.findall(r'\b\d+\b', data['from_url'])
        data['id'] = id[0];
        data['name'] = data['name'].split(' ')[1]
        data['goods_num'] =re.findall(r'\b\d+\b', i.find('dt').find('a').text)[1]
        #print('字典所有值为 :', tuple(list(data.values())))

        category.append(tuple(list(data.values())))

        for ii in i.find_all('dd') :
            data_1 = {
                'id': 0,
                'pid': data['id'],
                'name': ii.find('a').text,
                'goods_num': 0,
                'category_level': 2,
                'from_url': ii.find('a').get('href'),
                'create_time':now,
                'task_id': szlcsc_task_info[0],
            }
            id = re.findall(r'\b\d+\b', data_1['from_url'])
            data_1['id'] = id[0];
            data_1['name'] = data_1['name'].split(' ')[0]
            data_1['goods_num'] = re.findall(r'\b\d+\b',  ii.find('a').text)[0]
            category.append(tuple(list(data_1.values())))

    if (len(category) <= 0):
        print("没有可提交的数据")
        return False;

    try:
        #先清除分类数据，重新爬取最新数据
        category_sql = " truncate  table cj_szlcsc_category;"
        category_results = db.edit(category_sql, ())
        #print(category_results)
        if category_results == None:
            # 创建异常对象
            ex = Exception("清除分类数据失败")
            # 抛出异常对象
            raise ex

        sql = "INSERT INTO cj_szlcsc_category (`id`,`pid`,`name`,`goods_num`,`category_level`,`from_url`,`create_time`,`task_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
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


def data_goodslist():
    try:
        db = mysql()

        szlcsc_task_info = db.get_one("SELECT * FROM `cj_szlcsc_task` where status = 1 ORDER BY `task_id` DESC LIMIT 1", params=())
        if not szlcsc_task_info or szlcsc_task_info == None:
            print("任务不存在")
            return False;

        #加1为当前处理版本
        cj_szlcsc_category_list = db.get_all("SELECT * FROM `cj_szlcsc_category` where category_level = 2 and status = 1 and task_id = "+str(szlcsc_task_info[0])+"", params=())
        if not cj_szlcsc_category_list or cj_szlcsc_category_list == None:
            print("本地版本没有需要处理的数据")
            return False;

        #数据请求地址
        url = 'https://list.szlcsc.com/products/list'
        for i in cj_szlcsc_category_list:
            #总页数
            pagenun = math.ceil(i[3]/30)
            print("=============================正在处理分类："+str(i[2])+"总共******"+str(pagenun)+"******页，每页30条")
            p =i[10]+1
            for ii in  range(p,pagenun+1):
                nf = open("/home/wwwroot/www/log.txt", "w")
                nf.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                nf.close()

                print("=============================正在处理分类：" + str(i[2]) + "正在处理第******"+str(ii)+"******页的数据")
                #请求参数
                post_data = {}
                #分页商品数据
                productRecordList =[]
                post_data['catalogNodeId'] = i[0]
                post_data['pageNumber']=ii
                print(post_data)
                try:
                    # proxies = {
                    #     "http": "112.95.205.2:9999",
                    # }
                    #proxies=proxies
                    r = requests.post(url, post_data,timeout=(6.05, 27.05))
                    r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
                except requests.RequestException as e:
                    print(e)
                    continue
                print("接口请求响应状态:"+str(r.status_code))
                res = json.loads(r.text)
                productRecordList = res['productRecordList']
                #print(res['productRecordList'])
                print(url)
                #分页数据不存在则跳出
                if len(productRecordList) <= 0:
                    print("当前分页没有可处理的商品数据，跳出")
                    break

                #=============================不存在当前型号============================
                #新增数据数组
                inset_data = []
                #价格变动日志数组
                price_change_log_inset_data = []
                #库存变动日志数组
                stock_change_log_inset_data = []
                # 销量变动日志数组
                sale_num_change_log_inset_data = []
                # =============================存在当前型号============================
                # 更新数据数组
                update_data = []
                # 价格变动日志数组
                price_change_log_update_data = []
                # 库存变动日志数组
                stock_change_log_update_data = []
                # 销量变动日志数组
                sale_num_change_log_update_data = []

                j = 1;#当前处理条数
                productId_arr = data_arr_key(productRecordList,'productId')
                szlcsc_goods_sale_arr = szlcsc_goods_sale_where_in_arr(productId_arr)
                for iii in productRecordList:
                    print("===========================正在处理第"+str(j)+"条数据")

                    #================================数据处理==================================
                    szlcsc_min_ladder_price = 0;
                    szlcsc_brand_id = 0
                    spNumber = 0
                    # 库存为负数的时候默认为0
                    if(int(iii['stockNumber']) <=0):
                        iii['stockNumber']=0
                    #当具体价格不存在的时候默认为0
                    if(iii['productPriceList']):
                        szlcsc_min_ladder_price = iii['productPriceList'][-1]['productPrice']
                        spNumber= iii['productPriceList'][-1]['spNumber']
                    # 当匹品牌不存在的时候默认为0
                    if (iii['productGradePlateId']):
                        szlcsc_brand_id = int(iii['productGradePlateId'])
                    # ================================数据处理==================================

                    try:
                        szlcsc_goods_sale_info = szlcsc_goods_sale_arr[int(iii['productId'])]
                    except Exception  as result:
                        szlcsc_goods_sale_info = []
                        #szlcsc_goods_sale_info = db.get_one("SELECT * FROM `cj_szlcsc_goods_sale` where szlcsc_goods_id= "+str(iii['productId'])+" LIMIT 1", params=())
                    if not len(szlcsc_goods_sale_info):
                        inset_tmp = {
                            'szlcsc_goods_id': int(iii['productId']),
                            'szlcsc_goods_module_no':db.conn.escape_string(iii['productModel']),
                            'szlcsc_goods_name': db.conn.escape_string(iii['remarkPrefix']+iii['lightProductIntro']),
                            'szlcsc_goods_no': db.conn.escape_string(iii['lightProductCode']),
                            'szlcsc_category_id': int(iii['productTypeCode']),
                            'szlcsc_category_name':db.conn.escape_string(iii['productType']),
                            'szlcsc_brand_id': szlcsc_brand_id,
                            'szlcsc_brand_name': db.conn.escape_string(iii['productGradePlateName']),
                            'szlcsc_goods_unit': iii['productMinEncapsulationUnit'],
                            'szlcsc_min_packing': int(iii['productMinEncapsulationNumber']),
                            'szlcsc_goods_package':db.conn.escape_string(iii['encapsulationModel']),
                            'szlcsc_sale_num': int(iii['encapsulateProductMinEncapsulationNumber']),
                            'szlcsc_sale_stock': int(iii['stockNumber']),
                            'szlcsc_ladder_quantity': int(iii['theRatio'])*int(spNumber),
                            'szlcsc_min_ladder_price': szlcsc_min_ladder_price,
                            'from_url': db.conn.escape_string('https://item.szlcsc.com/'+str(iii['productId'])+'.html'),
                            'create_time': now,
                            'task_id':szlcsc_task_info[0],
                            'szlcsc_desc':'新增型号',# '新增型号',
                        }
                        #print(tuple(list(inset_tmp.values())))
                        inset_data.append(tuple(list(inset_tmp.values())))
                        #价格日志
                        price_change_log_inset_tmp= {
                            'szlcsc_goods_id': int(iii['productId']),
                            'is_first': 1,
                            'quantity': inset_tmp['szlcsc_ladder_quantity'],
                            'price': szlcsc_min_ladder_price,
                            'change_time': now,
                        }
                        price_change_log_inset_data.append(tuple(list(price_change_log_inset_tmp.values())))
                        # 库存日志
                        stock_change_log_inset_tmp = {
                            'szlcsc_goods_id': int(iii['productId']),
                            'is_first': 1,
                            'stock': int(iii['stockNumber']),
                            'change_time': now,
                        }
                        stock_change_log_inset_data.append(tuple(list(stock_change_log_inset_tmp.values())))
                        # 销量日志
                        sale_num_change_log_inset_tmp = {
                            'szlcsc_goods_id': int(iii['productId']),
                            'is_first': 1,
                            'sale_num': int(iii['encapsulateProductMinEncapsulationNumber']),
                            'change_time': now,
                        }
                        sale_num_change_log_inset_data.append(tuple(list(sale_num_change_log_inset_tmp.values())))
                        print("===========================为新增型号追加到插入队列中")
                    elif int(szlcsc_goods_sale_info[18]) == int(szlcsc_task_info[0]):
                        print("szlcsc_sale_id:"+str(szlcsc_goods_sale_info[0])+":已更新为当前任务版本 不重复处理，跳出")
                        continue
                    else:
                        print("szlcsc_sale_id:" + str(szlcsc_goods_sale_info[0]) + ":数据更新")
                        update_tmp = {
                            'szlcsc_goods_module_no': db.conn.escape_string(iii['productModel']),
                            'szlcsc_goods_name': db.conn.escape_string(iii['remarkPrefix'] + iii['lightProductIntro']),
                            'szlcsc_goods_no': db.conn.escape_string(iii['lightProductCode']),
                            'szlcsc_category_id': int(iii['productTypeCode']),
                            'szlcsc_category_name': db.conn.escape_string(iii['productType']),
                            'szlcsc_brand_id': szlcsc_brand_id,
                            'szlcsc_brand_name': db.conn.escape_string(iii['productGradePlateName']),
                            'szlcsc_goods_unit': iii['productMinEncapsulationUnit'],
                            'szlcsc_min_packing': int(iii['productMinEncapsulationNumber']),
                            'szlcsc_goods_package': db.conn.escape_string(iii['encapsulationModel']),
                            'szlcsc_sale_num': int(iii['encapsulateProductMinEncapsulationNumber']),
                            'szlcsc_sale_stock': int(iii['stockNumber']),
                            'szlcsc_ladder_quantity': int(iii['theRatio']) * int(spNumber),
                            'szlcsc_min_ladder_price': szlcsc_min_ladder_price,
                            'update_time': now,
                            'task_id': szlcsc_task_info[0],  # szlcsc_task_info[0],
                            'szlcsc_desc': '型号更新',  # '新增型号',
                            'szlcsc_sale_id': szlcsc_goods_sale_info[0],
                        }
                        # print(tuple(list(inset_tmp.values())))
                        update_data.append(tuple(list(update_tmp.values())))
                        if (szlcsc_goods_sale_info[14] != update_tmp['szlcsc_ladder_quantity'] or float(szlcsc_goods_sale_info[15]) != float(update_tmp['szlcsc_min_ladder_price'])):
                            # 价格日志
                            price_change_log_update_tmp = {
                                'szlcsc_goods_id': int(iii['productId']),
                                'is_first': 0,
                                'quantity': update_tmp['szlcsc_ladder_quantity'],
                                'price': szlcsc_min_ladder_price,
                                'change_time': now,
                            }
                            price_change_log_update_data.append(tuple(list(price_change_log_update_tmp.values())))
                        if int(szlcsc_goods_sale_info[13]) != int(update_tmp['szlcsc_sale_stock']):
                            # 库存日志
                            stock_change_log_update_tmp = {
                                'szlcsc_goods_id': int(iii['productId']),
                                'is_first': 0,
                                'stock': int(iii['stockNumber']),
                                'change_time': now,
                            }
                            stock_change_log_update_data.append(tuple(list(stock_change_log_update_tmp.values())))
                        if int(szlcsc_goods_sale_info[13]) != int(update_tmp['szlcsc_sale_stock']):
                            # 销量日志
                            sale_num_change_log_update_tmp = {
                                'szlcsc_goods_id': int(iii['productId']),
                                'is_first': 0,
                                'sale_num': int(iii['encapsulateProductMinEncapsulationNumber']),
                                'change_time': now,
                            }
                            sale_num_change_log_update_data.append(tuple(list(sale_num_change_log_update_tmp.values())))
                        print("===========================为更新型号追加到插入队列中")
                    print("===========================数据处理完成")
                    j+=1#当前处理条数加一

                #存在新增型号
                if len(inset_data) > 0:
                    try:
                        db.connect()
                        #商品数据插入
                        sql = "INSERT INTO cj_szlcsc_goods_sale (`szlcsc_goods_id`,`szlcsc_goods_module_no`, `szlcsc_goods_name`, `szlcsc_goods_no`" \
                              ",`szlcsc_category_id`, `szlcsc_category_name`, `szlcsc_brand_id`, `szlcsc_brand_name`, `szlcsc_goods_unit`, `szlcsc_min_packing`" \
                              ", `szlcsc_goods_package`, `szlcsc_sale_num`, `szlcsc_sale_stock`, `szlcsc_ladder_quantity`, `szlcsc_min_ladder_price`, `from_url`, `create_time`, `task_id`, `szlcsc_desc`)" \
                              " VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s);"
                        print(inset_data)
                        #results = db.insert(sql, inset_data)
                        results = db.cursor.executemany(sql, inset_data)
                        if results == None:
                            # 创建异常对象
                            ex = Exception("===================插入商品数据失败")
                            # 抛出异常对象
                            raise ex
                        print('===================商品数据数据插入成功')
                        if results !=None:
                            #价格变动日志插入
                            sql = "INSERT INTO cj_szlcsc_goods_price_change_log (`goods_id`,`is_first`, `quantity`, `price`, `change_time`) VALUES (%s, %s, %s, %s, %s);"
                            print(price_change_log_inset_data)
                            #results = db.insert(sql, price_change_log_inset_data)
                            results = db.cursor.executemany(sql, price_change_log_inset_data)
                            if results == None:
                                # 创建异常对象
                                ex = Exception("===================插入价格变动日志失败")
                                # 抛出异常对象
                                raise ex
                        print('===================价格变动日志插入成功')
                        # 库存变动日志插入
                        if results != None:
                            sql = "INSERT INTO cj_szlcsc_goods_stock_change_log (`goods_id`,`is_first`, `stock`, `change_time`) VALUES (%s, %s, %s, %s);"
                            print(stock_change_log_inset_data)
                            #results = db.insert(sql, stock_change_log_inset_data)
                            results = db.cursor.executemany(sql, stock_change_log_inset_data)
                            if results == None:
                                # 创建异常对象
                                ex = Exception("===================插入库存变动日志失败")
                                # 抛出异常对象
                                raise ex
                        print('===================库存变动日志插入成功')
                        # 销量变动日志插入
                        if results != None:
                            sql = "INSERT INTO cj_szlcsc_goods_sale_num_change_log (`goods_id`,`is_first`, `sale_num`, `change_time`) VALUES (%s, %s, %s, %s);"
                            print(stock_change_log_inset_data)
                            #results = db.insert(sql, sale_num_change_log_inset_data)
                            results = db.cursor.executemany(sql, sale_num_change_log_inset_data)
                            if results == None:
                                # 创建异常对象
                                ex = Exception("===================插入销量变动日志失败")
                                # 抛出异常对象
                                raise ex
                        print('===================销量变动日志插入成功')

                        db.conn.commit()
                        db.close()
                    except Exception  as result:
                        print('===================数据插入异常',result)
                        db.connect()
                        db.conn.rollback()
                        db.close()
                        exit()

                #存在更新数据
                if len(update_data) > 0:
                    try:
                        db.connect()
                        # 商品数据更新
                        sale_sql = "update cj_szlcsc_goods_sale set " \
                                   "szlcsc_goods_module_no=%s,szlcsc_goods_name=%s,szlcsc_goods_no=%s,szlcsc_category_id=%s,szlcsc_category_name=%s,szlcsc_brand_id=%s,szlcsc_brand_name=%s" \
                                   ",szlcsc_goods_unit=%s,szlcsc_min_packing=%s,szlcsc_goods_package=%s,szlcsc_sale_num=%s,szlcsc_sale_stock=%s,szlcsc_ladder_quantity=%s,szlcsc_min_ladder_price=%s" \
                                   ",update_time=%s,task_id=%s,szlcsc_desc=%s" \
                                   " where (`szlcsc_sale_id` = %s)"
                        results = db.cursor.executemany(sale_sql,update_data)
                        print(update_data)
                        if results == None:
                            # 创建异常对象
                            ex = Exception("更新商品数据失败")
                            # 抛出异常对象
                            raise ex
                        print('===================更新商品数据成功')

                        if results !=None and len(price_change_log_update_data) > 0:
                            #价格变动日志插入
                            sql = "INSERT INTO cj_szlcsc_goods_price_change_log (`goods_id`,`is_first`, `quantity`, `price`, `change_time`) VALUES (%s, %s, %s, %s, %s);"
                            print(price_change_log_update_data)
                            #results = db.insert(sql, price_change_log_update_data)
                            results = db.cursor.executemany(sql, price_change_log_update_data)
                            if results == None:
                                # 创建异常对象
                                ex = Exception("===================插入价格变动日志失败")
                                # 抛出异常对象
                                raise ex
                            print('===================更新型号价格变动日志插入成功')

                        # 库存变动日志插入
                        if results != None and len(stock_change_log_update_data) > 0:
                            sql = "INSERT INTO cj_szlcsc_goods_stock_change_log (`goods_id`,`is_first`, `stock`, `change_time`) VALUES (%s, %s, %s, %s);"
                            print(stock_change_log_update_data)
                            # results = db.insert(sql, stock_change_log_update_data)
                            results = db.cursor.executemany(sql, stock_change_log_update_data)
                            if results == None:
                                # 创建异常对象
                                ex = Exception("===================插入库存变动日志失败")
                                # 抛出异常对象
                                raise ex
                            print('===================更新型号库存变动日志插入成功')
                        # 销量变动日志插入
                        if results != None and len(sale_num_change_log_update_data) > 0:
                            sql = "INSERT INTO cj_szlcsc_goods_sale_num_change_log (`goods_id`,`is_first`, `sale_num`, `change_time`) VALUES (%s, %s, %s, %s);"
                            print(stock_change_log_update_data)
                            # results = db.insert(sql, sale_num_change_log_update_data)
                            results = db.cursor.executemany(sql, sale_num_change_log_update_data)
                            if results == None:
                                # 创建异常对象
                                ex = Exception("===================插入销量变动日志失败")
                                # 抛出异常对象
                                raise ex
                            print('===================更新型号销量变动日志插入成功')

                        db.conn.commit()
                        db.close()
                    except Exception  as result:
                        print('===================数据更新异常', result)
                        db.connect()
                        db.conn.rollback()
                        db.close()
                        exit()

                category_page_sql = "UPDATE `cj_szlcsc_category` SET `page` =  `page`+1 ,`update_time`='"+str(now)+"'  WHERE(`id` = '" + str(i[0]) + "')"
                category_page_results = db.update(category_page_sql, ())
                if category_page_results == None:
                    print('==========================处理分页变更失败')
                    break
                print('==========================处理分页变更成功')
                sys.stdout.flush()
                os.system("clear")
                #处理完一页出具延迟10秒
                print('==========================延时等待5秒钟再处理')
                for n in range(3):
                    print("3秒倒计时==========================" + str(3 - n)),
                    time.sleep(1)

            category_sql = "UPDATE `cj_szlcsc_category` SET `status` = '2',`update_time`='"+str(now)+"'  WHERE(`id` = '"+str(i[0])+"')"
            category_results = db.update(category_sql,())
            if category_results == None:
                print('==========================分类任务状态处理失败')
                break
            print('=====================分类任务变更成功，处理下一个分类')

        task_sql = "UPDATE `cj_szlcsc_task` SET `status` = '2',`update_time`='" + str(
            now) + "'  WHERE(`task_id` = '" + str(szlcsc_task_info[0]) + "')"
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
        return arr
    reurn_arr=[]
    for iii in arr:
        reurn_arr.append(iii[key])
    return reurn_arr


def szlcsc_goods_sale_where_in_arr(arr):
    if not arr:
        return arr
    db = mysql()
    select_sql = 'select * from cj_szlcsc_goods_sale where szlcsc_goods_id in (%s)'
    in_p = ', '.join((map(lambda x: '%s', arr)))
    reurn_arr = db.get_all(select_sql % in_p, arr)
    #print(reurn_arr)
    tmp = {}
    for i in reurn_arr:
        tmp[int(str(i[1]))] = i

    #print ('430523' in tmp.keys())
    return tmp

if __name__ == '__main__':
    # 判断商品是否存在
    # def is_in_szlcsc_goods_sale_arr(arr, key):

    data_category()
    data_goodslist()
    # szlcsc_goods_sale_where_in_arr()


