#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import hashlib

import xlsxwriter
import datetime
from datetime import timedelta

import getpass

def LoginByPost():
    #c创建session会话
    s=requests.session()
    account =  input("请输入账号");#'xiaoqiping'
    password = getpass.getpass("请输入密码");#'KBkx05jt';

    loginUrl='http://pms.jzic.com/index.php?m=user&f=login'
    login_res = s.get(loginUrl)
    login_res.encoding = 'utf-8'

    bs = BeautifulSoup(login_res.text, "html.parser")

    verifyRand = bs.find(id="verifyRand").get('value')
    verifyRand = verifyRand.encode('utf-8')

    md5password = hashlib.md5(password.encode('utf-8')).hexdigest()
    md5password = md5password.encode('utf-8')
    md5passwordverifyRand =  hashlib.md5((str(md5password) + str(verifyRand)).encode('utf-8')).hexdigest()

    ##设置cookies参数
    cookies = requests.utils.cookiejar_from_dict({'__root_domain_v': '.jzic.com','_qddaz':'QD.bxv6id.1b4qf9.k1lfu34z','goodsBrowseHistory=':'a%3A1%3A%7Bi%3A0%3Bs%3A5%3A%2219695%22%3B%7D','zentaosid':'s2bcdsg1vu4p9hmmm104lct6hq'})
    #print(type(cookies), cookies)
    s.cookies = cookies
    postData={'account':account,'password':md5passwordverifyRand,'referer':'http://pms.jzic.com/index.php?m=my&f=index','verifyRand':verifyRand,'passwordStrength':1,'keepLogin[]':'on'}
    header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
              "Referer": "http://pms.jzic.com/index.php?m=user&f=login"
              }
    rs=s.post(loginUrl,data = postData ,headers = header)
    #print(rs.cookies.values())

    # print(rs)
    url='http://pms.jzic.com/index.php?m=project&f=task&projectID=4&status=myinvolved&param=0&orderBy=&recTotal=158&recPerPage=1000&pageID=1&project=4&type=myinvolved'
    res=s.get(url)
    bs = BeautifulSoup(res.text, "html.parser")

    data = []
    now = datetime.datetime.now()
    last_week_start = now - timedelta(days=now.weekday() + 7)
    last_week_start = last_week_start.strftime('%m-%d')
    for i in bs.find(id="taskList").find('tbody').find_all("tr",attrs={"data-status":'done'}):
        if(i.find('td',attrs={"class":'c-deadline'}).text >= last_week_start ):
            data.append(i.find('td',attrs={"class":'c-name'}).get('title'))



    xlsx(account,data)

def xlsx(account,data):
    now = datetime.datetime.now()
    last_week_start = now - timedelta(days=now.weekday() + 7)
    last_week_end = now - timedelta(days=now.weekday() + 3)
    last_week_start = last_week_start.strftime('%Y年%m月%d日')
    last_week_end = last_week_end.strftime('%m月%d日')

    # data_list = []
    # k = 1
    # for i in data:
    #     data_list.append(str(k) + '、' + i)
    #     k += 1

    data_str = ''
    k = 1
    for i in data:
        if data_str == '':
            data_str =str(k) + '、' + i + '\r\n'
        else:
            data_str += str(k) + '、' + i + '\r\n'
        k += 1

    workbook = xlsxwriter.Workbook(r'D:\\'+last_week_start + '-' + last_week_end +account+'.xlsx')
    worksheet = workbook.add_worksheet('sheet1')
    headings = ['日期/（周）：' + last_week_start + '-' + last_week_end]
    data_title = ['日期/（周）：', '本周工作内容', '本周工作中的问题', '下周工作计划'];

    # 设置宽度
    worksheet.set_column("A:A", 40)
    worksheet.set_column("B:B", 100)
    worksheet.merge_range('A1:B1', '日期/（周）：' + last_week_start + '-' + last_week_end, workbook.add_format({
        'bold': True,
        'border': 1,
        'align': 'center',  # 水平居中
        'valign': 'vcenter',  # 垂直居中
        'text_wrap': True,
    }))

    #worksheet.write_row('A1', headings)
    merge_format = workbook.add_format({
        'bold': True,
        'border': 1,
        'align': 'center',  # 水平居中
        'valign': 'vcenter',  # 垂直居中
        'fg_color': '#D7E4BC',  # 颜色填充
        'text_wrap': True,
    })
    # 设置行内容
    #worksheet.merge_range('A2:A2', '本周工作内容', merge_format)
    worksheet.write_row('A2', [data_title[2]], merge_format)
    worksheet.write_row('A3', [data_title[2]], merge_format)
    worksheet.write_row('A4', [data_title[3]], merge_format)
    # 设置高度
    worksheet.set_row(1, 100)
    worksheet.set_row(2, 100)

    # 设置下周工作计划的格式和内容
    worksheet.write_row('B4', ["1、官网上线，以及上线之后的bug修复 \r\n2、后续任务的开发\r\n\r\n"], workbook.add_format({
        'align': 'left',  # 水平居中
        'valign': 'vcenter',  # 垂直居中
        'text_wrap': True,
    }))
    worksheet.write_row('B2', [data_str+ str(k) + '、修改这周提测的项目的bug，以及优化现有代码出现的问题\r\n'], workbook.add_format({
        'align': 'left',  # 水平居中
        'valign': 'vcenter',  # 垂直居中
        'text_wrap': True,
    }))
    workbook.close()


LoginByPost()