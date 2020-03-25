#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-

import os
import requests,json
import re
from bs4 import BeautifulSoup
import pymysql
import MySQLdb
from mysql import mysql
import time


def cj_szlcsc_task():
    db = mysql()
    sum_page = 533
    for i in range(1, sum_page):
        print('正在爬取第'+ str(i)+'页')
        url = 'https://www.chinacourt.org/law/more/law_type_id/MzAwNEAFAA/page/'+str(i)+'.shtml'
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        bs = BeautifulSoup(response.text, "html.parser")

        root_url = 'https://www.chinacourt.org'

        law_list = bs.find(class_="law_list").find('ul').find_all('a')
      
        data_list = [];
        for ii in law_list:
            try:
                print(ii.get('href'))
                url = root_url + ii.get('href')
                response = requests.get(url)
                response.raise_for_status()
                response.encoding = response.apparent_encoding

            except requests.RequestException as e:
                print(e)
                continue
            print("接口请求响应状态:" + str(response.status_code))
            try:
                details_bs = BeautifulSoup(response.text, "html.parser")
                num = re.findall(r'\b\d+\b', ii.get('href'))
                content = str(details_bs.find(class_="law_content").text)
            except Exception  as e:
                print(e)
                continue

            data = {
                    'china_court_id':num[2] ,
                    'from_url':root_url + ii.get('href'),
                    'title': ii.text,
                    'fabu_time':num[0],
                    'content':  content,
                    'page':i
             }
            data_list.append(tuple(list(data.values())))

        db.connect()
        sql = "INSERT INTO data_china_court (`china_court_id`,`from_url`,`title`, `fabu_time`, `content`, `page`) VALUES (%s,%s, %s, %s, %s, %s);"
        results = db.cursor.executemany(sql, data_list)
        db.conn.commit()
        db.close()
        print('===================插入成功')
        # 处理完一页出具延迟10秒
        print('==========================延时等待5秒钟再处理')
        for n in range(3):
            print("3秒倒计时==========================" + str(3 - n)),
            time.sleep(1)



def word_task():

    db = mysql()
    page = 1
    page_size = 200
    while True:
        start_idx = (page - 1) * page_size
        list = db.get_all("SELECT * FROM `data_china_court` where  status =1  Limit %d,%d " % (start_idx, page_size), params=())
        if not list or list == None:
            print("本地版本没有需要处理的数据")
            break

        for i in list:
            path = "file/国家法律法规/"+str(i[3])+"/"
            isExists = os.path.exists(path)
            # 判断结果
            # 如果不存在则创建目录    　
            if not isExists:
                os.makedirs(path)
                print("创建成功")
            else:
                # 如果目录存在则不创建，并提示目录已存在
                print("目录存在")

            title = i[2].replace('/', " ")
            title = title.replace('"', "")
            title = title.replace(' ', "")
            title =title.strip('.')
            title = title.strip('-')

            with open(path+title+'.doc', 'a+', encoding='utf-8') as f:
                f.write(i[4])
                sql = "UPDATE `data_china_court` SET `status` = '2'  WHERE(`id` = '" + str(i[0]) + "')"
            results = db.update(sql, ())
            if results == None:
                print('==========================任务状态处理失败')
                break
            print('=====================任务变更成功，处理下一个')
    page += 1

if __name__ == '__main__':
    word_task()