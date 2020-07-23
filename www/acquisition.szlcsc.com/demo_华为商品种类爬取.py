#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-

import requests,json
from bs4 import BeautifulSoup
import pandas as pd

def data_category():
    url = 'https://www.vmall.com/'
    r = requests.get(url)
    bs = BeautifulSoup(r.text, "html.parser")
    category_list = bs.find(class_="category-list").find_all(id='zxnav_8')

    result_data = []
    for i in category_list:
        for ii in i.find_all('li'):
            print(ii.find('a').text.strip())
            list_id = ii.find('a').get('href').split('-')[1]
            url = 'https://openapi.vmall.com/mcp/queryPrd?lang=zh-CN&country=CN&portal=1&keyword='+str(list_id)+'&pageSize=20&pageNum=1&searchSortField=0&searchSortType=desc&searchFlag=1'
            res = requests.get(url)
            res = json.loads(res.text)
            print(res['totalCount'])
            if(  ii.find('a').text.strip() != '查看全部' ):
                formated_data = {
                    '种类': ii.find('a').text.strip(),
                    '数目': res['totalCount'],
                }
                result_data.append(formated_data)

                df = pd.DataFrame(result_data)
                df.to_csv(r"file/华为商品种类/华为生态商品种类.csv" , encoding='utf-8-sig')
if __name__ == '__main__':
    # 判断商品是否存在
    # def is_in_szlcsc_goods_sale_arr(arr, key):

    data_category()

    # szlcsc_goods_sale_where_in_arr()


