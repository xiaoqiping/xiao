#!/usr/bin/python3.8
import requests ,json #line:4
from bs4 import BeautifulSoup #line:5
import re #line:6
import datetime #line:7
import time #line:8
import math #line:9
import collections #line:10
from datetime import timedelta #line:11
import sys #line:13
import os #line:14
from mysql import mysql #line:16
now =datetime .datetime .now ().strftime ('%Y-%m-%d %H:%M:%S')#line:19
def cj_szlcsc_task ():#line:22
    O000O0OO00OOO0O0O =mysql ()#line:23
    O0O00OO0O00OOO0O0 =O000O0OO00OOO0O0O .get_one ("SELECT * FROM `cj_szlcsc_task` where status = 1 ORDER BY `task_id` DESC LIMIT 1",params =())#line:25
    if O0O00OO0O00OOO0O0 :#line:26
        print ("存在未处理完的任务继续处理")#line:27
    else :#line:28
        try :#line:29
            O00O00O0O0OOO00OO =('立创数据采集','立创数据采集系统自动新增任务',now ,1 )#line:30
            OO0000OOO0OOOO000 ="INSERT INTO cj_szlcsc_task (`name`,`desc`, `update_time`, `status`) VALUES (%s, %s, %s, %s);"#line:31
            O0O000OO0OO00O000 =O000O0OO00OOO0O0O .edit (OO0000OOO0OOOO000 ,O00O00O0O0OOO00OO )#line:32
            if O0O000OO0OO00O000 ==None :#line:33
                O0OO0OO0OO00OOOO0 =Exception ("===================新增任务失败")#line:35
                raise O0OO0OO0OO00OOOO0 #line:37
        except Exception as O000OOO0OOOOOOOOO :#line:38
            print ('===================新增任务异常异常',O000OOO0OOOOOOOOO )#line:39
            exit ()#line:40
        print ('===================新增任务成功')#line:41
def data_category ():#line:43
    OOOOO00OO000OOO00 =mysql ()#line:44
    O00O00OO00OOOO00O ='https://www.szlcsc.com/catalog.html'#line:46
    O0O0O000O0O00OOOO =requests .get (O00O00OO00OOOO00O )#line:47
    O0O0O000O0O00OOOO .encoding =O0O0O000O0O00OOOO .apparent_encoding #line:48
    O00000OOOO000O000 =BeautifulSoup (O0O0O000O0O00OOOO .text ,"html.parser")#line:49
    OOOOO00OOOOO0OOOO =O00000OOOO000O000 .find (class_ ="page-www-catalog").find_all ('dl')#line:50
    if (len (OOOOO00OOOOO0OOOO )<=0 ):#line:52
        print ("分类数据不存在")#line:53
        return False ;#line:54
    OO0O00000O0OOO00O =OOOOO00OO000OOO00 .get_one ("SELECT * FROM `cj_szlcsc_task` where status = 1 ORDER BY `task_id` DESC LIMIT 1",params =())#line:57
    if OO0O00000O0OOO00O ==None :#line:58
        print (OO0O00000O0OOO00O )#line:59
        print ("任务不存在")#line:60
        return False ;#line:61
    O0000OO00OO0OOO0O =OOOOO00OO000OOO00 .get_one ("SELECT * FROM `cj_szlcsc_category` where category_level = 2 and status = 1 and task_id = "+str (OO0O00000O0OOO00O [0 ])+"  LIMIT 1",params =())#line:63
    if O0000OO00OO0OOO0O :#line:64
        print ("已经更新为当前版本分类数据")#line:65
        return False ;#line:66
    OO0OO00O0O0O00OO0 =[];#line:68
    for OOO0O000O0OOOOO0O in OOOOO00OOOOO0OOOO :#line:69
        O00O000000000O000 ={'id':0 ,'pid':0 ,'name':OOO0O000O0OOOOO0O .find ('dt').find ('a').text ,'goods_num':0 ,'category_level':1 ,'from_url':OOO0O000O0OOOOO0O .find ('dt').find ('a').get ('href'),'create_time':now ,'task_id':OO0O00000O0OOO00O [0 ],}#line:79
        O0O00O0000O000O0O =re .findall (r'\b\d+\b',O00O000000000O000 ['from_url'])#line:80
        O00O000000000O000 ['id']=O0O00O0000O000O0O [0 ];#line:81
        O00O000000000O000 ['name']=O00O000000000O000 ['name'].split (' ')[1 ]#line:82
        O00O000000000O000 ['goods_num']=re .findall (r'\b\d+\b',OOO0O000O0OOOOO0O .find ('dt').find ('a').text )[1 ]#line:83
        OO0OO00O0O0O00OO0 .append (tuple (list (O00O000000000O000 .values ())))#line:86
        for OO0OOO00OOOO00OOO in OOO0O000O0OOOOO0O .find_all ('dd'):#line:88
            OOO0O00000OOOO000 ={'id':0 ,'pid':O00O000000000O000 ['id'],'name':OO0OOO00OOOO00OOO .find ('a').text ,'goods_num':0 ,'category_level':2 ,'from_url':OO0OOO00OOOO00OOO .find ('a').get ('href'),'create_time':now ,'task_id':OO0O00000O0OOO00O [0 ],}#line:98
            O0O00O0000O000O0O =re .findall (r'\b\d+\b',OOO0O00000OOOO000 ['from_url'])#line:99
            OOO0O00000OOOO000 ['id']=O0O00O0000O000O0O [0 ];#line:100
            OOO0O00000OOOO000 ['name']=OOO0O00000OOOO000 ['name'].split (' ')[0 ]#line:101
            OOO0O00000OOOO000 ['goods_num']=re .findall (r'\b\d+\b',OO0OOO00OOOO00OOO .find ('a').text )[0 ]#line:102
            OO0OO00O0O0O00OO0 .append (tuple (list (OOO0O00000OOOO000 .values ())))#line:103
    if (len (OO0OO00O0O0O00OO0 )<=0 ):#line:105
        print ("没有可提交的数据")#line:106
        return False ;#line:107
    try :#line:109
        OO000O000OO0O0000 =" truncate  table cj_szlcsc_category;"#line:111
        O00000O00OO00OO00 =OOOOO00OO000OOO00 .edit (OO000O000OO0O0000 ,())#line:112
        if O00000O00OO00OO00 ==None :#line:114
            OO0O0O0O0O0OO0O0O =Exception ("清除分类数据失败")#line:116
            raise OO0O0O0O0O0OO0O0O #line:118
        O0O000O00O00OOOOO ="INSERT INTO cj_szlcsc_category (`id`,`pid`,`name`,`goods_num`,`category_level`,`from_url`,`create_time`,`task_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"#line:120
        O00OO0000OO0OOO0O =OOOOO00OO000OOO00 .insert (O0O000O00O00OOOOO ,OO0OO00O0O0O00OO0 )#line:121
        print (O00OO0000OO0OOO0O )#line:122
        if O00OO0000OO0OOO0O ==None :#line:123
            OO0O0O0O0O0OO0O0O =Exception ("插入分类数据失败")#line:125
            raise OO0O0O0O0O0OO0O0O #line:127
    except Exception as OO0O000O00OO0O0O0 :#line:129
        print (OO0O000O00OO0O0O0 )#line:130
        OOOOO00OO000OOO00 .connect ()#line:131
        OOOOO00OO000OOO00 .conn .rollback ()#line:132
def data_goodslist ():#line:135
    try :#line:136
        OOO0O0O0000OOOO0O =mysql ()#line:137
        OOOOOO00O00OOOOO0 =OOO0O0O0000OOOO0O .get_one ("SELECT * FROM `cj_szlcsc_task` where status = 1 ORDER BY `task_id` DESC LIMIT 1",params =())#line:139
        if not OOOOOO00O00OOOOO0 or OOOOOO00O00OOOOO0 ==None :#line:140
            print ("任务不存在")#line:141
            return False ;#line:142
        OO0O0OO00000OOO00 =OOO0O0O0000OOOO0O .get_all ("SELECT * FROM `cj_szlcsc_category` where category_level = 2 and status = 1 and task_id = "+str (OOOOOO00O00OOOOO0 [0 ])+"",params =())#line:145
        if not OO0O0OO00000OOO00 or OO0O0OO00000OOO00 ==None :#line:146
            print ("本地版本没有需要处理的数据")#line:147
            return False ;#line:148
        O0OO00000O0OO000O ='https://list.szlcsc.com/products/list'#line:151
        for OOO0O000000OO000O in OO0O0OO00000OOO00 :#line:152
            O0OOOO00O0OOOOO00 =math .ceil (OOO0O000000OO000O [3 ]/30 )#line:154
            print ("=============================正在处理分类："+str (OOO0O000000OO000O [2 ])+"总共******"+str (O0OOOO00O0OOOOO00 )+"******页，每页30条")#line:155
            OOO0000OO000000O0 =OOO0O000000OO000O [10 ]+1 #line:156
            for O0OOOO0OO0O00O00O in range (OOO0000OO000000O0 ,O0OOOO00O0OOOOO00 +1 ):#line:157
                O00OO0OO0OO00O000 =open ("/home/wwwroot/www/log.txt","w")#line:158
                O00OO0OO0OO00O000 .write (datetime .datetime .now ().strftime ('%Y-%m-%d %H:%M:%S'))#line:159
                O00OO0OO0OO00O000 .close ()#line:160
                print ("=============================正在处理分类："+str (OOO0O000000OO000O [2 ])+"正在处理第******"+str (O0OOOO0OO0O00O00O )+"******页的数据")#line:162
                O00O0OOOO0OOOO000 ={}#line:164
                OOO0OO0O0OO00O0O0 =[]#line:166
                O00O0OOOO0OOOO000 ['catalogNodeId']=OOO0O000000OO000O [0 ]#line:167
                O00O0OOOO0OOOO000 ['pageNumber']=O0OOOO0OO0O00O00O #line:168
                print (O00O0OOOO0OOOO000 )#line:169
                try :#line:170
                    O0O00OO0O0O00O00O =requests .post (O0OO00000O0OO000O ,O00O0OOOO0OOOO000 ,timeout =(6.05 ,27.05 ))#line:175
                    O0O00OO0O0O00O00O .raise_for_status ()#line:176
                except requests .RequestException as OOO0000OO00O0OOO0 :#line:177
                    print (OOO0000OO00O0OOO0 )#line:178
                    continue #line:179
                print ("接口请求响应状态:"+str (O0O00OO0O0O00O00O .status_code ))#line:180
                O0O0OO0O000OOO00O =json .loads (O0O00OO0O0O00O00O .text )#line:181
                OOO0OO0O0OO00O0O0 =O0O0OO0O000OOO00O ['productRecordList']#line:182
                print (O0OO00000O0OO000O )#line:184
                if len (OOO0OO0O0OO00O0O0 )<=0 :#line:186
                    print ("当前分页没有可处理的商品数据，跳出")#line:187
                    break #line:188
                OO0OO000O00000O00 =[]#line:192
                O00O0000O00O0000O =[]#line:194
                O000000O00OO00OO0 =[]#line:196
                O0O00OO000O0O0OOO =[]#line:198
                OOOO0OOOO0O0000OO =[]#line:201
                OOOO0OO0O0O0OO0OO =[]#line:203
                O0000O00O0000OO00 =[]#line:205
                OO0OOOO00OO0OOO0O =[]#line:207
                O00O0O000OO00O00O =1 ;#line:209
                O00OOO00O000000OO =data_arr_key (OOO0OO0O0OO00O0O0 ,'productId')#line:210
                OO00O0O0O0000OO00 =szlcsc_goods_sale_where_in_arr (O00OOO00O000000OO )#line:211
                for OO00O0O00OO00OOOO in OOO0OO0O0OO00O0O0 :#line:212
                    print ("===========================正在处理第"+str (O00O0O000OO00O00O )+"条数据")#line:213
                    O0O0OOO0O0O0O0000 =0 ;#line:216
                    O0000O00O00O00000 =0 #line:217
                    OO0O0000OO0O000OO =0 #line:218
                    if (int (OO00O0O00OO00OOOO ['stockNumber'])<=0 ):#line:220
                        OO00O0O00OO00OOOO ['stockNumber']=0 #line:221
                    if (OO00O0O00OO00OOOO ['productPriceList']):#line:223
                        O0O0OOO0O0O0O0000 =OO00O0O00OO00OOOO ['productPriceList'][-1 ]['productPrice']#line:224
                        OO0O0000OO0O000OO =OO00O0O00OO00OOOO ['productPriceList'][-1 ]['spNumber']#line:225
                    if (OO00O0O00OO00OOOO ['productGradePlateId']):#line:227
                        O0000O00O00O00000 =int (OO00O0O00OO00OOOO ['productGradePlateId'])#line:228
                    try :#line:231
                        OO000000O000OO0OO =OO00O0O0O0000OO00 [int (OO00O0O00OO00OOOO ['productId'])]#line:232
                    except Exception as OOOO00O0OO00O0000 :#line:233
                        OO000000O000OO0OO =[]#line:234
                    if not len (OO000000O000OO0OO ):#line:236
                        OO000OOOOOO000000 ={'szlcsc_goods_id':int (OO00O0O00OO00OOOO ['productId']),'szlcsc_goods_module_no':OOO0O0O0000OOOO0O .conn .escape_string (OO00O0O00OO00OOOO ['productModel']),'szlcsc_goods_name':OOO0O0O0000OOOO0O .conn .escape_string (OO00O0O00OO00OOOO ['remarkPrefix']+OO00O0O00OO00OOOO ['lightProductIntro']),'szlcsc_goods_no':OOO0O0O0000OOOO0O .conn .escape_string (OO00O0O00OO00OOOO ['lightProductCode']),'szlcsc_category_id':int (OO00O0O00OO00OOOO ['productTypeCode']),'szlcsc_category_name':OOO0O0O0000OOOO0O .conn .escape_string (OO00O0O00OO00OOOO ['productType']),'szlcsc_brand_id':O0000O00O00O00000 ,'szlcsc_brand_name':OOO0O0O0000OOOO0O .conn .escape_string (OO00O0O00OO00OOOO ['productGradePlateName']),'szlcsc_goods_unit':OO00O0O00OO00OOOO ['productMinEncapsulationUnit'],'szlcsc_min_packing':int (OO00O0O00OO00OOOO ['productMinEncapsulationNumber']),'szlcsc_goods_package':OOO0O0O0000OOOO0O .conn .escape_string (OO00O0O00OO00OOOO ['encapsulationModel']),'szlcsc_sale_num':int (OO00O0O00OO00OOOO ['encapsulateProductMinEncapsulationNumber']),'szlcsc_sale_stock':int (OO00O0O00OO00OOOO ['stockNumber']),'szlcsc_ladder_quantity':int (OO00O0O00OO00OOOO ['theRatio'])*int (OO0O0000OO0O000OO ),'szlcsc_min_ladder_price':O0O0OOO0O0O0O0000 ,'from_url':OOO0O0O0000OOOO0O .conn .escape_string ('https://item.szlcsc.com/'+str (OO00O0O00OO00OOOO ['productId'])+'.html'),'create_time':now ,'task_id':OOOOOO00O00OOOOO0 [0 ],'szlcsc_desc':'新增型号',}#line:257
                        OO0OO000O00000O00 .append (tuple (list (OO000OOOOOO000000 .values ())))#line:259
                        OO000O0O00OO0O000 ={'szlcsc_goods_id':int (OO00O0O00OO00OOOO ['productId']),'is_first':1 ,'quantity':OO000OOOOOO000000 ['szlcsc_ladder_quantity'],'price':O0O0OOO0O0O0O0000 ,'change_time':now ,}#line:267
                        O00O0000O00O0000O .append (tuple (list (OO000O0O00OO0O000 .values ())))#line:268
                        O0OO0OO0OO00O0O0O ={'szlcsc_goods_id':int (OO00O0O00OO00OOOO ['productId']),'is_first':1 ,'stock':int (OO00O0O00OO00OOOO ['stockNumber']),'change_time':now ,}#line:275
                        O000000O00OO00OO0 .append (tuple (list (O0OO0OO0OO00O0O0O .values ())))#line:276
                        OOO0O0O000OO0OOOO ={'szlcsc_goods_id':int (OO00O0O00OO00OOOO ['productId']),'is_first':1 ,'sale_num':int (OO00O0O00OO00OOOO ['encapsulateProductMinEncapsulationNumber']),'change_time':now ,}#line:283
                        O0O00OO000O0O0OOO .append (tuple (list (OOO0O0O000OO0OOOO .values ())))#line:284
                        print ("===========================为新增型号追加到插入队列中")#line:285
                    elif int (OO000000O000OO0OO [18 ])==int (OOOOOO00O00OOOOO0 [0 ]):#line:286
                        print ("szlcsc_sale_id:"+str (OO000000O000OO0OO [0 ])+":已更新为当前任务版本 不重复处理，跳出")#line:287
                        continue #line:288
                    else :#line:289
                        print ("szlcsc_sale_id:"+str (OO000000O000OO0OO [0 ])+":数据更新")#line:290
                        O0000O00OOO0000O0 ={'szlcsc_goods_module_no':OOO0O0O0000OOOO0O .conn .escape_string (OO00O0O00OO00OOOO ['productModel']),'szlcsc_goods_name':OOO0O0O0000OOOO0O .conn .escape_string (OO00O0O00OO00OOOO ['remarkPrefix']+OO00O0O00OO00OOOO ['lightProductIntro']),'szlcsc_goods_no':OOO0O0O0000OOOO0O .conn .escape_string (OO00O0O00OO00OOOO ['lightProductCode']),'szlcsc_category_id':int (OO00O0O00OO00OOOO ['productTypeCode']),'szlcsc_category_name':OOO0O0O0000OOOO0O .conn .escape_string (OO00O0O00OO00OOOO ['productType']),'szlcsc_brand_id':O0000O00O00O00000 ,'szlcsc_brand_name':OOO0O0O0000OOOO0O .conn .escape_string (OO00O0O00OO00OOOO ['productGradePlateName']),'szlcsc_goods_unit':OO00O0O00OO00OOOO ['productMinEncapsulationUnit'],'szlcsc_min_packing':int (OO00O0O00OO00OOOO ['productMinEncapsulationNumber']),'szlcsc_goods_package':OOO0O0O0000OOOO0O .conn .escape_string (OO00O0O00OO00OOOO ['encapsulationModel']),'szlcsc_sale_num':int (OO00O0O00OO00OOOO ['encapsulateProductMinEncapsulationNumber']),'szlcsc_sale_stock':int (OO00O0O00OO00OOOO ['stockNumber']),'szlcsc_ladder_quantity':int (OO00O0O00OO00OOOO ['theRatio'])*int (OO0O0000OO0O000OO ),'szlcsc_min_ladder_price':O0O0OOO0O0O0O0000 ,'update_time':now ,'task_id':OOOOOO00O00OOOOO0 [0 ],'szlcsc_desc':'型号更新','szlcsc_sale_id':OO000000O000OO0OO [0 ],}#line:310
                        OOOO0OOOO0O0000OO .append (tuple (list (O0000O00OOO0000O0 .values ())))#line:312
                        if (OO000000O000OO0OO [14 ]!=O0000O00OOO0000O0 ['szlcsc_ladder_quantity']or float (OO000000O000OO0OO [15 ])!=float (O0000O00OOO0000O0 ['szlcsc_min_ladder_price'])):#line:313
                            O0O00O00OOO0O0O00 ={'szlcsc_goods_id':int (OO00O0O00OO00OOOO ['productId']),'is_first':0 ,'quantity':O0000O00OOO0000O0 ['szlcsc_ladder_quantity'],'price':O0O0OOO0O0O0O0000 ,'change_time':now ,}#line:321
                            OOOO0OO0O0O0OO0OO .append (tuple (list (O0O00O00OOO0O0O00 .values ())))#line:322
                        if int (OO000000O000OO0OO [13 ])!=int (O0000O00OOO0000O0 ['szlcsc_sale_stock']):#line:323
                            O0O000000OO000O00 ={'szlcsc_goods_id':int (OO00O0O00OO00OOOO ['productId']),'is_first':0 ,'stock':int (OO00O0O00OO00OOOO ['stockNumber']),'change_time':now ,}#line:330
                            O0000O00O0000OO00 .append (tuple (list (O0O000000OO000O00 .values ())))#line:331
                        if int (OO000000O000OO0OO [13 ])!=int (O0000O00OOO0000O0 ['szlcsc_sale_stock']):#line:332
                            OOOOOO0O000OO000O ={'szlcsc_goods_id':int (OO00O0O00OO00OOOO ['productId']),'is_first':0 ,'sale_num':int (OO00O0O00OO00OOOO ['encapsulateProductMinEncapsulationNumber']),'change_time':now ,}#line:339
                            OO0OOOO00OO0OOO0O .append (tuple (list (OOOOOO0O000OO000O .values ())))#line:340
                        print ("===========================为更新型号追加到插入队列中")#line:341
                    print ("===========================数据处理完成")#line:342
                    O00O0O000OO00O00O +=1 #line:343
                if len (OO0OO000O00000O00 )>0 :#line:346
                    try :#line:347
                        OOO0O0O0000OOOO0O .connect ()#line:348
                        OOOO00O0OOO0OO00O ="INSERT INTO cj_szlcsc_goods_sale (`szlcsc_goods_id`,`szlcsc_goods_module_no`, `szlcsc_goods_name`, `szlcsc_goods_no`" ",`szlcsc_category_id`, `szlcsc_category_name`, `szlcsc_brand_id`, `szlcsc_brand_name`, `szlcsc_goods_unit`, `szlcsc_min_packing`" ", `szlcsc_goods_package`, `szlcsc_sale_num`, `szlcsc_sale_stock`, `szlcsc_ladder_quantity`, `szlcsc_min_ladder_price`, `from_url`, `create_time`, `task_id`, `szlcsc_desc`)" " VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s);"#line:353
                        print (OO0OO000O00000O00 )#line:354
                        O0O000O00O0O0O0O0 =OOO0O0O0000OOOO0O .cursor .executemany (OOOO00O0OOO0OO00O ,OO0OO000O00000O00 )#line:356
                        if O0O000O00O0O0O0O0 ==None :#line:357
                            O0OOOO0OOO00OOOOO =Exception ("===================插入商品数据失败")#line:359
                            raise O0OOOO0OOO00OOOOO #line:361
                        print ('===================商品数据数据插入成功')#line:362
                        if O0O000O00O0O0O0O0 !=None :#line:363
                            OOOO00O0OOO0OO00O ="INSERT INTO cj_szlcsc_goods_price_change_log (`goods_id`,`is_first`, `quantity`, `price`, `change_time`) VALUES (%s, %s, %s, %s, %s);"#line:365
                            print (O00O0000O00O0000O )#line:366
                            O0O000O00O0O0O0O0 =OOO0O0O0000OOOO0O .cursor .executemany (OOOO00O0OOO0OO00O ,O00O0000O00O0000O )#line:368
                            if O0O000O00O0O0O0O0 ==None :#line:369
                                O0OOOO0OOO00OOOOO =Exception ("===================插入价格变动日志失败")#line:371
                                raise O0OOOO0OOO00OOOOO #line:373
                        print ('===================价格变动日志插入成功')#line:374
                        if O0O000O00O0O0O0O0 !=None :#line:376
                            OOOO00O0OOO0OO00O ="INSERT INTO cj_szlcsc_goods_stock_change_log (`goods_id`,`is_first`, `stock`, `change_time`) VALUES (%s, %s, %s, %s);"#line:377
                            print (O000000O00OO00OO0 )#line:378
                            O0O000O00O0O0O0O0 =OOO0O0O0000OOOO0O .cursor .executemany (OOOO00O0OOO0OO00O ,O000000O00OO00OO0 )#line:380
                            if O0O000O00O0O0O0O0 ==None :#line:381
                                O0OOOO0OOO00OOOOO =Exception ("===================插入库存变动日志失败")#line:383
                                raise O0OOOO0OOO00OOOOO #line:385
                        print ('===================库存变动日志插入成功')#line:386
                        if O0O000O00O0O0O0O0 !=None :#line:388
                            OOOO00O0OOO0OO00O ="INSERT INTO cj_szlcsc_goods_sale_num_change_log (`goods_id`,`is_first`, `sale_num`, `change_time`) VALUES (%s, %s, %s, %s);"#line:389
                            print (O000000O00OO00OO0 )#line:390
                            O0O000O00O0O0O0O0 =OOO0O0O0000OOOO0O .cursor .executemany (OOOO00O0OOO0OO00O ,O0O00OO000O0O0OOO )#line:392
                            if O0O000O00O0O0O0O0 ==None :#line:393
                                O0OOOO0OOO00OOOOO =Exception ("===================插入销量变动日志失败")#line:395
                                raise O0OOOO0OOO00OOOOO #line:397
                        print ('===================销量变动日志插入成功')#line:398
                        OOO0O0O0000OOOO0O .conn .commit ()#line:400
                        OOO0O0O0000OOOO0O .close ()#line:401
                    except Exception as OOOO00O0OO00O0000 :#line:402
                        print ('===================数据插入异常',OOOO00O0OO00O0000 )#line:403
                        OOO0O0O0000OOOO0O .connect ()#line:404
                        OOO0O0O0000OOOO0O .conn .rollback ()#line:405
                        OOO0O0O0000OOOO0O .close ()#line:406
                        exit ()#line:407
                if len (OOOO0OOOO0O0000OO )>0 :#line:410
                    try :#line:411
                        OOO0O0O0000OOOO0O .connect ()#line:412
                        O0OOOOO0O00OO0O00 ="update cj_szlcsc_goods_sale set " "szlcsc_goods_module_no=%s,szlcsc_goods_name=%s,szlcsc_goods_no=%s,szlcsc_category_id=%s,szlcsc_category_name=%s,szlcsc_brand_id=%s,szlcsc_brand_name=%s" ",szlcsc_goods_unit=%s,szlcsc_min_packing=%s,szlcsc_goods_package=%s,szlcsc_sale_num=%s,szlcsc_sale_stock=%s,szlcsc_ladder_quantity=%s,szlcsc_min_ladder_price=%s" ",update_time=%s,task_id=%s,szlcsc_desc=%s" " where (`szlcsc_sale_id` = %s)"#line:418
                        O0O000O00O0O0O0O0 =OOO0O0O0000OOOO0O .cursor .executemany (O0OOOOO0O00OO0O00 ,OOOO0OOOO0O0000OO )#line:419
                        print (OOOO0OOOO0O0000OO )#line:420
                        if O0O000O00O0O0O0O0 ==None :#line:421
                            O0OOOO0OOO00OOOOO =Exception ("更新商品数据失败")#line:423
                            raise O0OOOO0OOO00OOOOO #line:425
                        print ('===================更新商品数据成功')#line:426
                        if O0O000O00O0O0O0O0 !=None and len (OOOO0OO0O0O0OO0OO )>0 :#line:428
                            OOOO00O0OOO0OO00O ="INSERT INTO cj_szlcsc_goods_price_change_log (`goods_id`,`is_first`, `quantity`, `price`, `change_time`) VALUES (%s, %s, %s, %s, %s);"#line:430
                            print (OOOO0OO0O0O0OO0OO )#line:431
                            O0O000O00O0O0O0O0 =OOO0O0O0000OOOO0O .cursor .executemany (OOOO00O0OOO0OO00O ,OOOO0OO0O0O0OO0OO )#line:433
                            if O0O000O00O0O0O0O0 ==None :#line:434
                                O0OOOO0OOO00OOOOO =Exception ("===================插入价格变动日志失败")#line:436
                                raise O0OOOO0OOO00OOOOO #line:438
                            print ('===================更新型号价格变动日志插入成功')#line:439
                        if O0O000O00O0O0O0O0 !=None and len (O0000O00O0000OO00 )>0 :#line:442
                            OOOO00O0OOO0OO00O ="INSERT INTO cj_szlcsc_goods_stock_change_log (`goods_id`,`is_first`, `stock`, `change_time`) VALUES (%s, %s, %s, %s);"#line:443
                            print (O0000O00O0000OO00 )#line:444
                            O0O000O00O0O0O0O0 =OOO0O0O0000OOOO0O .cursor .executemany (OOOO00O0OOO0OO00O ,O0000O00O0000OO00 )#line:446
                            if O0O000O00O0O0O0O0 ==None :#line:447
                                O0OOOO0OOO00OOOOO =Exception ("===================插入库存变动日志失败")#line:449
                                raise O0OOOO0OOO00OOOOO #line:451
                            print ('===================更新型号库存变动日志插入成功')#line:452
                        if O0O000O00O0O0O0O0 !=None and len (OO0OOOO00OO0OOO0O )>0 :#line:454
                            OOOO00O0OOO0OO00O ="INSERT INTO cj_szlcsc_goods_sale_num_change_log (`goods_id`,`is_first`, `sale_num`, `change_time`) VALUES (%s, %s, %s, %s);"#line:455
                            print (O0000O00O0000OO00 )#line:456
                            O0O000O00O0O0O0O0 =OOO0O0O0000OOOO0O .cursor .executemany (OOOO00O0OOO0OO00O ,OO0OOOO00OO0OOO0O )#line:458
                            if O0O000O00O0O0O0O0 ==None :#line:459
                                O0OOOO0OOO00OOOOO =Exception ("===================插入销量变动日志失败")#line:461
                                raise O0OOOO0OOO00OOOOO #line:463
                            print ('===================更新型号销量变动日志插入成功')#line:464
                        OOO0O0O0000OOOO0O .conn .commit ()#line:466
                        OOO0O0O0000OOOO0O .close ()#line:467
                    except Exception as OOOO00O0OO00O0000 :#line:468
                        print ('===================数据更新异常',OOOO00O0OO00O0000 )#line:469
                        OOO0O0O0000OOOO0O .connect ()#line:470
                        OOO0O0O0000OOOO0O .conn .rollback ()#line:471
                        OOO0O0O0000OOOO0O .close ()#line:472
                        exit ()#line:473
                O00OO0OOO000O00O0 ="UPDATE `cj_szlcsc_category` SET `page` =  `page`+1 ,`update_time`='"+str (now )+"'  WHERE(`id` = '"+str (OOO0O000000OO000O [0 ])+"')"#line:475
                OOOO00O0O0O0O0OO0 =OOO0O0O0000OOOO0O .update (O00OO0OOO000O00O0 ,())#line:476
                if OOOO00O0O0O0O0OO0 ==None :#line:477
                    print ('==========================处理分页变更失败')#line:478
                    break #line:479
                print ('==========================处理分页变更成功')#line:480
                sys .stdout .flush ()#line:481
                os .system ("clear")#line:482
                print ('==========================延时等待5秒钟再处理')#line:484
                for OOOOOO00OO0O0OO0O in range (3 ):#line:485
                    print ("3秒倒计时=========================="+str (3 -OOOOOO00OO0O0OO0O )),#line:486
                    time .sleep (1 )#line:487
            O0OO00OO0OOOOOO0O ="UPDATE `cj_szlcsc_category` SET `status` = '2',`update_time`='"+str (now )+"'  WHERE(`id` = '"+str (OOO0O000000OO000O [0 ])+"')"#line:489
            O0O0OO0O0OOOO000O =OOO0O0O0000OOOO0O .update (O0OO00OO0OOOOOO0O ,())#line:490
            if O0O0OO0O0OOOO000O ==None :#line:491
                print ('==========================分类任务状态处理失败')#line:492
                break #line:493
            print ('=====================分类任务变更成功，处理下一个分类')#line:494
        O0OO00O00OOOO0000 ="UPDATE `cj_szlcsc_task` SET `status` = '2',`update_time`='"+str (now )+"'  WHERE(`task_id` = '"+str (OOOOOO00O00OOOOO0 [0 ])+"')"#line:497
        OOO00OOOO00OOOO0O =OOO0O0O0000OOOO0O .update (O0OO00O00OOOO0000 ,())#line:498
        if OOO00OOOO00OOOO0O ==None :#line:499
            print ('==========================任务状态处理失败')#line:500
        print ('=====================任务变更成功，处理完成')#line:502
    except Exception as OOOO00O0OO00O0000 :#line:503
        print ('==========================程序运行异常')#line:504
        print (OOOO00O0OO00O0000 )#line:505
def data_arr_key (O000O0OOO0OOOO0O0 ,O0O0O00O00000OO0O ):#line:508
    if len (O000O0OOO0OOOO0O0 )<=0 :#line:509
        return O000O0OOO0OOOO0O0 #line:510
    O0O0O00O0OOO0OOOO =[]#line:511
    for OOO00000O0O00OO0O in O000O0OOO0OOOO0O0 :#line:512
        O0O0O00O0OOO0OOOO .append (OOO00000O0O00OO0O [O0O0O00O00000OO0O ])#line:513
    return O0O0O00O0OOO0OOOO #line:514
def szlcsc_goods_sale_where_in_arr (OOO0OOOO0000O0OO0 ):#line:517
    if not OOO0OOOO0000O0OO0 :#line:518
        return OOO0OOOO0000O0OO0 #line:519
    O0OOO00OO0OOOO000 =mysql ()#line:520
    O0O00O0OOOO000O00 ='select * from cj_szlcsc_goods_sale where szlcsc_goods_id in (%s)'#line:521
    OO0O000OOO0OOO0OO =', '.join ((map (lambda OOO0000OO0O0OOOOO :'%s',OOO0OOOO0000O0OO0 )))#line:522
    O0O0O0O0OO0OOOO0O =O0OOO00OO0OOOO000 .get_all (O0O00O0OOOO000O00 %OO0O000OOO0OOO0OO ,OOO0OOOO0000O0OO0 )#line:523
    O000O00OOOO000OOO ={}#line:525
    for O00OOO00000OO0OOO in O0O0O0O0OO0OOOO0O :#line:526
        O000O00OOOO000OOO [int (str (O00OOO00000OO0OOO [1 ]))]=O00OOO00000OO0OOO #line:527
    return O000O00OOOO000OOO #line:530
if __name__ =='__main__':#line:532
    cj_szlcsc_task ()#line:535
    data_category ()#line:536
    data_goodslist ()#line:537
