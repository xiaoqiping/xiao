#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests,json
from bs4 import BeautifulSoup
import re
from mysql import mysql


def data_category():
    # c创建session会话
    url = 'https://www.szlcsc.com/catalog.html'
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    bs = BeautifulSoup(response.text, "html.parser")
    category_level_1 = bs.find(class_="page-www-catalog").find_all('dl')


    category= [];
    for i in category_level_1:
        data = {
            'id': 0,
            'pid': 0,
            'name': i.find('dt').find('a').text,
            'goods_num':0,
            'category_level': 1,
            'from_url': i.find('dt').find('a').get('href'),
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
            }
            id = re.findall(r'\b\d+\b', data_1['from_url'])
            data_1['id'] = id[0];
            data_1['name'] = data_1['name'].split(' ')[0]
            data_1['goods_num'] = re.findall(r'\b\d+\b',  ii.find('a').text)[0]
            category.append(tuple(list(data_1.values())))


    db = mysql()
    sql = "INSERT INTO cj_szlcsc_category (`id`,`pid`,`name`,`goods_num`,`category_level`,`from_url`) VALUES (%s, %s, %s, %s, %s, %s);"
    results = db.insert(sql,category)
    print(results)

def data_goodslist():
    url = 'https://list.szlcsc.com/products/list'
    data = {'catalogNodeId': '380', 'pageNumber': '1'}
    r = requests.post(url, data)
    res = json.loads(r.text)
    print(res['productRecordList'])











    #
    #
    #
    # db = mysql()
    #
    # results = db.get_one('SELECT * FROM ic_menbers limit 1')
    #
    # print(results)



data_category()