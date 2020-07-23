#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-

import requests,json
from bs4 import BeautifulSoup
import pandas as pd

def data_category():
    f = open('file/小米商品种类/aa.html', 'rb')  # 里面为文件路径

    bs = BeautifulSoup(f.read(), "html.parser")
    category_list = bs.find_all(class_='categoryHeader-G-sic')

    boardsWrap_uKvGG = bs.find_all(class_='boardsWrap-uKvGG')

    result_data = []
    p = 0
    for ii in category_list:
        print(ii.find('span').text.strip())

        totalCount = len(boardsWrap_uKvGG[p].find_all(class_='boardCard-3nuYn'))
        formated_data = {
            '圈子': ii.find('span').text.strip(),
            '数目': totalCount,
        }


        result_data.append(formated_data)
        df = pd.DataFrame(result_data)
        df.to_csv(r"file/小米商品种类/小米社区圈子及数量.csv" , encoding='utf-8-sig')
        p+=1
if __name__ == '__main__':
    # 判断商品是否存在
    # def is_in_szlcsc_goods_sale_arr(arr, key):

    data_category()

    # szlcsc_goods_sale_where_in_arr()


