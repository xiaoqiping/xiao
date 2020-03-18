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

def data_category():
    db = mysql()
    fruits = [20,40,60,80,100]
    movie = [
                'https://movie.douban.com/j/search_subjects?type=movie&tag=%E5%8A%A8%E4%BD%9C&sort=recommend&page_limit=10&page_start=0',
                 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E5%96%9C%E5%89%A7&sort=recommend&page_limit=10&page_start=0',
                 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%88%90%E9%95%BF&sort=recommend&page_limit=20&page_start=0',
                'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%A7%91%E5%B9%BB&sort=recommend&page_limit=10&page_start=0',
                 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%82%AC%E7%96%91&sort=recommend&page_limit=10&page_start=0',
                 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%81%90%E6%80%96&sort=recommend&page_limit=10&page_start=0',
             ]
    header = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        "X-Requested-With": "XMLHttpRequest",
        'Referer':'https://movie.douban.com/explore'
        }
    for i in movie:
        url = i
        response = requests.get(url, headers=header)
        movie_list = json.loads(response.text)['subjects']

        for ii in movie_list:
            header = {
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                "X-Requested-With": "XMLHttpRequest",
                'Referer': 'https://movie.douban.com/explore'
            }

            for jj in fruits:
                url = 'https://movie.douban.com/subject/'+ii['id']+'/comments?start=0&limit='+str(jj)+'&sort=new_score&status=P&comments_only=1'
                print(url)
                response = requests.get(url, headers=header)
                res = json.loads(response.text)
                html = res['html']
                bs = BeautifulSoup(html, "html.parser")
                category_level_1 = bs.find_all(class_="comment-item")

                # 新增数据数组
                inset_data = []
                for iii in category_level_1:
                    print(iii)
                    try:
                        comment_time = iii.find(class_="comment-time").get('title')
                        rating = iii.find(class_="rating").get('title')
                        comment_name = iii.find(class_="comment-info").find('a').text
                        votes =iii.find(class_="votes").text
                        rating_num = ''
                        if rating[0] == '很差':
                            rating_num = 1
                        elif rating[0] == '较差':
                            rating_num = 2
                        elif rating[0] == '还行':
                            rating_num = 3
                        elif rating[0] == '推荐':
                            rating_num = 4
                        elif rating[0] == '力荐':
                            rating_num = 5
                        else:
                            rating_num = '';
                    except:
                        rating = ''
                        rating_num = ''
                        comment_time = '0000-00-00 00:00:00 '
                        comment_name =''
                        votes =0
                    inset_tmp = {
                            'comment_id':  iii.get('data-cid'),
                            'movie_name':ii['title'],
                            'comment-time':comment_time,
                            'rating':rating,
                            'votes':votes,
                            'rating_num':rating_num,
                            'comment-name':comment_name

                    }

                    inset_data.append(tuple(list(inset_tmp.values())))
                # 存在新增型号
                if len(inset_data) > 0:
                    try:
                        db.connect()
                        # 商品数据插入
                        sql = "INSERT INTO douban_comments (`comment_id`,`movie_name`,`comment-time`, `rating`, `votes`,`rating_num`,`comment-name`) VALUES (%s,%s, %s, %s, %s, %s, %s);"
                        print(inset_data)
                        # results = db.insert(sql, inset_data)
                        results = db.cursor.executemany(sql, inset_data)
                        if results == None:
                            # 创建异常对象
                            ex = Exception("===================插入数据失败")
                            # 抛出异常对象
                            raise ex
                        print('===================数据数据插入成功')
                        db.conn.commit()
                        db.close()


                    except Exception  as result:
                        print(result)
                        db.connect()
                        db.conn.rollback()
                    print('===================延时2秒再执行')
                    time.sleep(2)







if __name__ == '__main__':
    # 判断商品是否存在
    # def is_in_szlcsc_goods_sale_arr(arr, key):

    data_category()

    # szlcsc_goods_sale_where_in_arr()


