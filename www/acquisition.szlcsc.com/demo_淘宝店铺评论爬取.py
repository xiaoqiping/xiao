#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-

import requests,json
# from bs4 import BeautifulSoup
import re
# import datetime
import time
# import math
# import collections
# from datetime import timedelta
# import sys
# import os

from mysql import mysql

def data_category():
    db = mysql()
    movie = [
                # 'https://rate.tmall.com/list_detail_rate.htm?itemId=572525039156&spuId=1172644884&sellerId=3878105384&order=3&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvNpv9v3GvUvCkvvvvvjiPnLq9tj3Un2cpAjD2PmPUQjE8P2M90jDER2LwAjYj9phv2HiJLz36zHi47eJ%2FzghCvv14ceagxn147DiFNaGtvpvhphvvvUhCvv14ceagxn147Dikqr%2FCvpvW7DMSJbcw7Di4OLsN9phv2HiNqzklzHi47evSzTwCvvBvpvpZvphvCyCCvvvvvvyCvh12IU6vI16AxsBCAfyp%2B3%2B%2BjomxfXuKfvxYVVzwdiYApcCHTnkfVcxXnDeDyBvOJ193Zi7vVBDTmmxBlwyzhmyZEcqUaXGfa6nTLYLUkphvCyEmmvpwe4yCvv3vpvLEq%2F5e4byCvm3vpvvvvvCvphCvjvUvvhPuphvwv9vvBj1vpCQmvvChxhCvjvUvvhBZ2QhvCvvvMMGtvpvhphvvvUwCvvBvppvvdphvmZCHRhsVvhCmou6CvCEELUHZFpCvBHWQSfV7%2BF3WWDRrvpvEphxhZH6vphcqRphvChCvvvvtvpvhphvvvUhCvv14cyYgan147DieJr%2FCvpvW7DtPJjLw7Di4XT2N9phv2HiJLz36zHi47ey4zT6CvCEELnDp89CvZPJZSfV7%2BF3WWDRCvpvxOl%2FyJhUw7Di44M5NoW5V3qMoJ0%2BUdphvmZCh%2Fl2YvhC7vu6CvvDvpdiZCpCvxlKrvpvEphpvZnQvpHKpdphvmZCC7lChvhCwl46CvCCjBIxp0vCvcBYGSfyT%2Bkt4dphvhhaVDH2SvhCJw3VYKLuAbDuCvpvW7DTnJnLw7Di4eRfN&needFold=0&_ksTS=1592897407562_5627&callback=jsonp5628&currentPage=',
                #'https://rate.tmall.com/list_detail_rate.htm?itemId=619434122678&spuId=0&sellerId=2206425889810&order=3&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvDvvZvxhvUvCkvvvvvjiPnLq9tjnjPscUzjljPmPysjYbR2M9gjtER25ZQj3nRphvChCvvvmrvpvEphL1nPUvphu2dphvmZCC9AAAvhCUST6CvvDvBnZyavCvBCArvpvEphBXHvZvphU2iQhvChCvCCoivpvUphvhAcmomVoEvpvVpyUUCCAXKphv8hCvvvvvvhCvphvwv9vvpJavpCQmvvChNhCvjvUvvhBZphvwv9vvBHpEvpCWpaCMv8WTnZwK2ixre8tYVC%2Bda4Zzh2aJbyuYzB4AVA%2BaUExre8t%2BCc6OfwmK5znVJhdItEIwwHQ0747BhC3qVmHoDOvwjLEcnhjEKphCvvXvovvvvvvPvpvhvv2MMsyCvvBvpvvv3QhvChCCvvmrvpvEphoZVP6vphWHdphvmZC28sBkvhCE3T6CvvDvBnDW%2BvCvLM4rvpvEphp8oUvvpHVRdphvmZChGZLNvhCLhghCvCB4cin9na147DiKV%2FawBldk75qNhp%3D%3D&needFold=0&_ksTS=1592898444574_1092&callback=jsonp1093&currentPage=',
                'https://rate.tmall.com/list_detail_rate.htm?itemId=618979829347&spuId=0&sellerId=2201499362579&order=3&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvN9vcvc6vUvCkvvvvvjiPnLq9tjnbRFzOQjnEPmPZAjiRn2dWzjimRLcUljtP9phvHHiJeim0zHi47iKYtlAe7GD4NrGBdphvmpvUY9okI9C9yT6CvvyvmWO2O7hvxburvpvEvvFT99yEvHmjdphvmpvUTIUOVvCvXT6CvvyvmnOmMSgv8vJrvpvEvv3xvFp6vmCDRphvCvvvvvvPvpvhvv2MMgyCvvOUvvVvJhKivpvUvvmvR4mbTumtvpvIvvvvvhCvvvvvvUnvphvhe9vv96CvpC29vvm2phCvhhvvvUnvphvppvyCvhQv6bZvClsUQjc6eCru20zUzjZ7%2B3%2Bizjc6D40OaokG1nkQ%2BulAo5c6D76XVC6qD7zUQ8g7EcqUQjc6PqUf8JCl%2BE7rVc9DYExrAEKKvphvC9v9vvCvp8wCvvpvvUmm3QhvCvvhvvmrvpvEvvAjv%2Bd8v2AVdphvmpvUg987D9ChiIhCvv14cvfMHr147DirmnGtvpvhvvvvv86Cvvyv2Em2QWvvcV8rvpvpjvCE3WSbvVQLFfwznHVt6LyCvvpvvvvv&needFold=0&_ksTS=1592898878522_1116&callback=jsonp1117&currentPage='
    ]
    header = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        "X-Requested-With": "XMLHttpRequest",
        'Referer':'https://detail.tmall.com/item.htm?id=572525039156',
        'cookie':'hng=CN%7Czh-CN%7CCNY%7C156; enc=Qls7Hp5FvFPbAB%2BBCf3G%2Fxfi0G1bcwx0F5DqFVwKP8Htxj9s9HoJoAs8TO6ri%2FLOd45RQLaIULyZdpBbZNKOEUwV2QzrZVvW2U2JGVdfYG4%3D; cna=xTr3FsPSoy4CAXkPB3n64Khu; lid=tiamomeixiao; sgcookie=E8GUmJkIk4Bf1TXqgfctG; uc1=cookie14=UoTV7gm%2B4b90Ag%3D%3D; uc3=lg2=VFC%2FuZ9ayeYq2g%3D%3D&id2=UoH4FCzkxWc6Ow%3D%3D&nk2=F59eQlictE2SR%2FBf&vt3=F8dBxGDe2pvHLF9M9wc%3D; t=31f85f7e1514993bacb1247630ce14f8; tracknick=tiamomeixiao; uc4=id4=0%40UOnnEYTvD%2B2H1GSBKeFw4tR7mNfb&nk4=0%40FYWuvJYXpROYxzGk2FKININLCZQOSpk%3D; lgc=tiamomeixiao; _tb_token_=3a658ea5733e7; cookie2=105922b243efccfdb5788b0d40e31959; _m_h5_tk=665eaf886febf7a837efcbd5050287b2_1592901336977; _m_h5_tk_enc=6c07d87bb707ef679653f07e19da430e; x5sec=7b22726174656d616e616765723b32223a2266363762356234353139356134343764333536643139323936333336393936384350446578766346454d485473734b2f3565506f7567453d227d; l=eBjl1a_4Qc_Lo1eaBO5Zourza77OFCAbzsPzaNbMiInca1zhdOoFJNQDl7QDfdtjgt5fEetPOzL1BRnkPoUU-x_ceTwhKXIpBeJB8e1..; isg=BBcXKKHSBZ8AXoGeDvYLUeYkpothXOu-Ncm5RWlAHeSQmDXacSgjD1P--jiGcMM2'
        }

    paginator = 1;
    for i in movie:
        url = i+str(paginator)
        r = requests.get(url, headers=header)
        print(r.text)
        res = json.loads(re.match(".*?({.*}).*", r.text, re.S).group(1))
        movie_list =res['rateDetail']
        # 总页数
        pagenun = movie_list['paginator']['lastPage']


        print("=============================正在处理分类：" + str(url) + "总共******" + str(pagenun) + "******页，每页20条")
        p = 1
        for ii in range(p, pagenun + 1):
            url = i + str(p)
            rs = requests.get(url, headers=header)
            print(rs.text)
            callable_res = json.loads(re.match(".*?({.*}).*", rs.text, re.S).group(1))

            rateList = callable_res['rateDetail']['rateList']
            inset_data = []
            for iii in rateList:
                append_content = ''
                is_img = "否"
                is_v = "否"
                rateContent = ''
                if iii['appendComment']:
                    append_content = iii['appendComment']['content']
                if iii['rateContent']:
                    rateContent = iii['rateContent']
                if iii['pics']:
                    is_img = '是'
                append_content = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", append_content)
                rateContent = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", rateContent)

                inset_tmp = {
                        'user_id':  iii['id'],
                        'content':rateContent,
                        'append_content':append_content,
                        'comment_time':iii['rateDate'],
                        'is_img':is_img,
                        'is_v':is_v,
                        'from_url':url

                }

                inset_data.append(tuple(list(inset_tmp.values())))
        # 存在新增型号
            if len(inset_data) > 0:
                try:
                    db.connect()
                    # 商品数据插入
                    sql = "INSERT INTO cj_taobao_pinlun_data (`user_id`,`content`,`append_content`, `comment_time`, `is_img`,`is_v`,`from_url`) VALUES (%s,%s, %s, %s, %s, %s, %s);"
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
            time.sleep(5)
            p+=1







if __name__ == '__main__':
    # 判断商品是否存在
    # def is_in_szlcsc_goods_sale_arr(arr, key):

    data_category()

    # szlcsc_goods_sale_where_in_arr()


