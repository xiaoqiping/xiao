#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-

import os
import os.path
from pathlib import Path
import requests,json
from bs4 import BeautifulSoup
import re
import datetime
import time
import math
from mysql import mysql

from fake_useragent import UserAgent

mysql_config = {'host':'localhost', 'user':'root', 'password':'root','db':'jzic_crawl_data_v2'}
#d当前时间
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

location = 'file/气象数据家园/fake_useragent.json'
ua = UserAgent(path=location)


def data_category():
    db = mysql(host=mysql_config['host'], user=mysql_config['user'], password=mysql_config['password'],db=mysql_config['db'])
    headers = {
        "referer":"https://www.digikey.cn/products/zh/discrete-semiconductor-products/diodes-variable-capacitance-varicaps-varactors/282",
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    }
    url = 'https://www.digikey.cn/products/zh/integrated-circuits-ics/32'
    response = requests.get(url,headers=headers, timeout=(6.05, 27.05))
    response.encoding = response.apparent_encoding
    bs = BeautifulSoup(response.text, "html.parser")


    category_level_1 = bs.find(class_="catfiltersub").find_all('li')


    if(len(category_level_1) <=0):
        print("分类数据不存在")
        return False;

    #查询版本信息
    szlcsc_task_info = db.get_one("SELECT * FROM `cj_collection_company_task` where status = 1 and name = '贸泽电子网数据采集' ORDER BY `task_id` DESC LIMIT 1", params=())
    if szlcsc_task_info == None:
        print(szlcsc_task_info)
        print("任务不存在")
        return False;
    # cj_szlcsc_category_list = db.get_one("SELECT * FROM `cj_mouser_category` where category_level = 2 and status = 1 and task_id = " + str(szlcsc_task_info[0]) + "  LIMIT 1", params=())
    # if cj_szlcsc_category_list :
    #     print("已经更新为当前版本分类数据")
    #     return False;
    #分类数据
    category= [];
    for i in category_level_1:

        data = {
            'id': 0,
            'pid':32,
            'name': i.find('a').text,
            'goods_num':''.join(re.findall('\d+', i.find('a').text)),
            'category_level': 2,
            'from_url': i.find('a').get('href'),
            'create_time': now,
            'task_id': szlcsc_task_info[0],
        }

        id = re.findall(r'\b\d+\b', data['from_url'])
        data['id'] = id[0];

        category.append(tuple(list(data.values())))
        # 处理完一页出具延迟10秒
        print('=========================='+str(i.find('a').text))

    if (len(category) <= 0):
        print("没有可提交的数据")
        return False;

    try:
        #先清除分类数据，重新爬取最新数据
        # category_sql = " truncate  table cj_mouser_category;"
        # category_results = db.edit(category_sql, ())
        # #print(category_results)
        # if category_results == None:
        #     # 创建异常对象
        #     ex = Exception("清除分类数据失败")
        #     # 抛出异常对象
        #     raise ex

        sql = "INSERT INTO cj_mouser_category (`id`,`pid`,`name`,`goods_num`,`category_level`,`from_url`,`create_time`,`task_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
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
    task_info = db.get_one("SELECT * FROM `cj_collection_company_task` where status = 1 and name = '贸泽电子网数据采集' ORDER BY `task_id` DESC LIMIT 1",params=())
    if task_info:
        print("存在未处理完的任务继续处理")
    else:
        try:
            inset_data = ('贸泽电子网数据采集', '贸泽电子网数据采集自动新增任务', now, 1)
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

        db = mysql(host=mysql_config['host'], user=mysql_config['user'], password=mysql_config['password'],db=mysql_config['db'])
        task_info = db.get_one("SELECT * FROM `cj_collection_company_task` where status = 1 and name = '贸泽电子网数据采集' ORDER BY `task_id` DESC LIMIT 1", params=())
        if not task_info or task_info == None:
            print("任务不存在")
            return False;

        # 加1为当前处理版本
        cj_szlcsc_category_list = db.get_all(
            "SELECT * FROM `cj_mouser_category` where category_level = 2 and status = 1 and task_id = " + str(
                task_info[0]) + "", params=())
        if not cj_szlcsc_category_list or cj_szlcsc_category_list == None:
            print("本地版本没有需要处理的数据")
            return False;
        for i in cj_szlcsc_category_list:
            #总页数
            pagenun = math.ceil(i[3]/25)
            print("=============================正在处理分类："+str(i[2])+"总共******"+str(pagenun)+"******页，每页30条")
            p =i[10]+1
            for ii in  range(p,pagenun+1):
                # headers = {
                #     "user-agent": ua.random,
                # }
                # url = i[5]+'?'+str(ii)
                # response = requests.get(url, headers=headers, timeout=(6.05, 27.05))
                # response.encoding = response.apparent_encoding
                # bs = BeautifulSoup(response.text, "html.parser")

                title = i[2].replace('/', " ")
                title = title.replace('"', "")
                title = title.replace(' ', "")
                title = title.strip('.')
                title = title.strip('-')

                path = "file/贸泽电子网/" + str(i[2]) + "/"
                name = path +str(title) +'_download_'+str(ii)+'.csv'


                isExists = os.path.exists(path)
                # 判断结果
                # 如果不存在则创建目录    　
                if not isExists:
                    os.makedirs(path)
                    print("创建成功")
                my_file = Path(name)
                if my_file.exists():
                    print("==========================该城市指定的文件存在，跳过下载下一个文件")
                    # 指定的文件存在
                    continue

                write_url ='https://www.digikey.cn/products/zh/integrated-circuits-ics/specialized-ics/'
                write_url+="AdvancedSearchResultsDownload?&pageNumber="+str(ii)+"&sort=&sortDescending=0&sortType=S&qtyRequested=&c="+str(i[0])
                header = {
                    "cookie":'i10c.uid=1585814642778:2036; optimizelyEndUserId=oeu1585814645190r0.33377268925621806; EG-U-ID=E5b0b7cdcc-6f01-4791-8e22-78157d33db7c; i10c.uservisit=2; WC_PERSISTENT=%2bjrYkLsU4se6laI7EpfU0lXvvY8%3d%0a%3b2020%2d07%2d14+03%3a24%3a06%2e791%5f1594715046788%2d10248669%5f10001%5f%2d1002%2c%2d7%2cCNY%5f10001; _ga=GA1.2.1377909879.1594715057; _abck=B92310C1B84FF695BF2E60DDCE6DBFDF~0~YAAQFoyUGzZljThzAQAAu8tsTAThcidlPMwv/wzCXCDbZ06t2/CD42xt6iCJLwoSZ82uexZV9aUkpRUSgR154muGc802Zi3XA485wW3ThI/mfPcekjgqnI/6AzFEimx+OLJhQmG/jVHuuynQEC+FObNrQ/mAlTqIGR3qN6WfUv2tH0fPJQcrm79Ov1QUB5Rg2+F6uHWYyczEQso/ALjCfsRNe3Qc7igsYO+tvRc/7prQdXqiUBtsHltPJ/OD7VF571M04grCFy8V3KHwruTHTJldF7Pexucq7eLDHWgItuYjOFnXV03IVTuvIdpjw14ER/1iQdyaOw==~-1~-1~-1; _evga_cd68=e0bd9d4a370478bc.; _gid=GA1.2.294291151.1594867040; WC_SESSION_ESTABLISHED=true; WC_AUTHENTICATION_-1002=%2d1002%2cxClFneevJTCQwIkhZMqB6nffX7k%3d; WC_ACTIVEPOINTER=%2d7%2c10001; WC_USERACTIVITY_-1002=%2d1002%2c10001%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cuGrL3%2fz%2bLA6Cj2UpqYs7GTu4hXweHTv4JGiLQRB%2bvVrwuriPkes%2bG0mMa9ATRkj76IN3%2fJLFrgW4%0aGH1J4E6mIrRU17VRrzUNMy7mXo5%2fIvDpLOZhZK3dSDYCCIDVYFvKd8t9yA%2bg5afCeMNVZx6pPg%3d%3d; WC_GENERIC_ACTIVITYDATA=[1774758965%3atrue%3afalse%3a0%3aDjiuwsOSd916hEMBwiuPAROn8Hk%3d][com.ibm.commerce.context.audit.AuditContext|1594715046788%2d10248669][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][com.digikey.commerce.context.UserContext|null][CTXSETNAME|Store][com.ibm.commerce.context.globalization.GlobalizationContext|%2d7%26CNY%26%2d7%26CNY][com.ibm.commerce.catalog.businesscontext.CatalogContext|10001%26null%26false%26false%26false][com.ibm.commerce.context.base.BaseContext|10001%26%2d1002%26%2d1002%26%2d1][com.ibm.commerce.context.experiment.ExperimentContext|null][com.ibm.commerce.context.entitlement.EntitlementContext|10001%2610001%26null%26%2d2000%26null%26null%26null][com.ibm.commerce.giftcenter.context.GiftCenterContext|null%26null%26null]; EG-S-ID=A509394250-5789-4668-ba27-98210468fdf7; ak_bmsc=7BE84DA4C95D546622424637DF044C491B948C16127E0000ABEE0F5F7919AC3F~plfHqEhkBj/qAmIp/Y6kUUTort2zdI3gHq06UcmjZYUhf8HghMl6EZ/MAridd65V1m7cIdiLXIjuGXUwf0jhtKolrChntH6sHiXO3hdj27PpYsTDX9B7SsGaPmE7LTnidbRVjB03lZKMPyFWLcJd3b1m+XmvX7w2tDBDv3oJgwOTOvQ0zAh/rCPvOdcJd0TzZiLdBuTjThPZI9GXSWEHqFmQsy9G9xsCaZLSODlUqrxXPmOB1hwi0GzV8JCHoLNBRu; bm_sz=7623184328F1A59536B8AB03059550D5~YAAQZsU8t2nKujVzAQAANbVXVgiCKwidF247BDcbLEF6q2T0wKaSeUZ6SA5psD87BXDorvBuRX9xg6ALbeC8KjvDi7wcm7rkU7OG7qRW45hmlaKZ79UK4cCRCLkDO2ESkowtDqf5KHtnu37D5V3H9hVuIc/AGUOEDC13we7qr/Zu1M6l43kTfShIk2qdAddy; JSESSIONID=00045S7jrV5aq0YTTm5ylGlpTM_:-20D9B; QSI_HistorySession=https%3A%2F%2Fwww.digikey.cn%2Fproducts%2Fzh%2Fdiscrete-semiconductor-products%2Fdiodes-variable-capacitance-varicaps-varactors%2F282~1594879740251%7Chttps%3A%2F%2Fwww.digikey.cn%2Fproducts%2Fzh%2Fdiscrete-semiconductor-products%2Fdiodes-variable-capacitance-varicaps-varactors%2F282%3FpageNumber%3D1~1594881427266%7Chttps%3A%2F%2Fwww.digikey.cn%2Fproducts%2Fzh%2Fdiscrete-semiconductor-products%2Fdiodes-variable-capacitance-varicaps-varactors%2F282%3FpageNumber%3D2~1594884058063; TS01d239f3=01460246b62266a7bd1be1d2ab53a1b84e8c6c58e3b183a6fdd09ca4f52978685aef97cc21b1e779ed3e4652eb2a0ff049037b6412; TS01b442d5=01460246b68e74a79140e8396bf885c20ded2ac2f4849c126aeb63a990256f4427093ed75ed751037c39d7a22a602de9c343ee5204; website#lang=zh-CN-RMB; bm_sv=D8BB359A98579A35237D3ADA655F7C8E~M3Ggsx0u1O/HdheO/c1QLU7ng10ABJ26N7lhpO3eNX+KDpZzlPErRXbFaxSl8yHRvMFeJaPF6je14Q92mvMVtuBotmd/HEzmtCX1ZLgWQHYRWdDNdp5oXDoTxgTKG1BqZkU8fF+1G1RTVfTebksB/RGosqHzOWEvdgdXdEp0rqQ=; utag_main=v_id:017139eb7b2d004eba77bce306d803073008e06b00bd0$_sn:4$_ss:0$_st:1594886263294$ses_id:1594879672424%3Bexp-session$_pn:13%3Bexp-session; _gat_Production=1',
                    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                    "referer": "https://www.digikey.cn/products/zh/discrete-semiconductor-products/thyristors-diacs-sidacs/274"
                }
                r = requests.get(write_url, headers=header, timeout=(6.05, 27.05))
                with open(name, "wb") as code:
                    code.write(r.content)

                category_page_sql = "UPDATE `cj_mouser_category` SET `page` =  `page`+1 ,`update_time`='" + str(
                    now) + "'  WHERE(`id` = '" + str(i[0]) + "')"
                category_page_results = db.update(category_page_sql, ())
                if category_page_results == None:
                    print('==========================处理分页变更失败')
                    break

                print("==========================文件下载成功，执行下一个任务")
                print('==========================防止被封延时等待5秒钟再处理')
                for n in range(3):
                    print("3秒倒计时==========================" + str(3 - n)),
                    time.sleep(1)

            category_sql = "UPDATE `cj_mouser_category` SET `status` = '2',`update_time`='" + str(
                now) + "'  WHERE(`id` = '" + str(i[0]) + "')"
            category_results = db.update(category_sql, ())
            if category_results == None:
                print('==========================分类任务状态处理失败')
                break
            print('=====================分类任务变更成功，处理下一个分类')

if __name__ == '__main__':
    # 判断商品是否存在
    # def is_in_szlcsc_goods_sale_arr(arr, key):
    #cj_task()
    #data_category()
    data_goodslist()
    # szlcsc_goods_sale_where_in_arr()
