#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-
# http://envbox.net/upar/upar_chn_mul_hor.html
##按年爬取资料

import os
import os.path
from pathlib import Path
import requests,json
import time


from time import strftime, localtime
import csv
import arrow
from fake_useragent import UserAgent

def token_check():
    code_name = 'meteorological_y_config'
    code = 'F7BC52B2D53115267CD1AC9662ADE22EYUQDHGTLB'
    try:
       url = 'http://39.100.113.43:9000/key.php'
       response = requests.get(url, timeout=(6.05, 27.05), params={"code_name": code_name, 'code': code})
       response.raise_for_status()
       response.encoding = response.apparent_encoding
       if response.text != '200':
            print("操作失败请联系管理员")
            exit()
    except requests.RequestException as e:
       print("操作失败请联系管理员")
       exit()

query_time = '2019-01-01'
UTC='00'#UTC 0时 UTC 12时   value分别为 00 12
def qx_city():
    token_check()

    query_time = input("请输入需要下载的年份，例如 2019 ,输完之后请按回车键确认:")
    if not query_time.isdigit():
        print("请输入数字，关闭程序重新启动")
        time.sleep(3)
        exit()

    select_UTC = input("请选择UTC，1 代表：UTC 0时、 2代表：UTC 12时 ,输完之后请按回车键确认:")
    if not select_UTC.isdigit():
        print("请输入数字，关闭程序重新启动")
        time.sleep(3)
        exit()
    select_UTC = int(select_UTC)
    if select_UTC == 1:
        UTC = '00'
    elif select_UTC == 2 :
        UTC = '12'
    else:
        print("输入非法字符，关闭程序重新启动")
        time.sleep(3)
        exit()


    path = r"file/气象数据家园/Data/"+str(query_time)+'-'+str((0 if UTC=='00' else 12))+"/"
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print("==========================创建年份目录成功")
    my_file = Path(path+"index.txt")
    if my_file.exists():
        print("==========================该年份已经执行完毕")
        input("程序执行完毕退出请按回车键确认:")
        time.sleep(3)



    location = 'file/气象数据家园/fake_useragent.json'
    ua = UserAgent(path=location)
    header = {
        "User-Agent": ua.random,
        'Host': 'api.envbox.net:8080',
        'Origin': 'http://envbox.net',
        'Referer': 'http://envbox.net/upar/upar_chn_mul_hor.html'
    }

    try:
        url = 'http://api.envbox.net:8080/getUparStations'
        response = requests.get(url,headers=header,timeout=(6.05, 27.05))
        response.raise_for_status()
        response.encoding = response.apparent_encoding
    except requests.RequestException as e:
        print("页面请求失败求延时等待3秒钟再重新请")
        for n in range(3):
            print("3秒倒计时==========================" + str(3 - n)),
            time.sleep(1)
        url = 'http://api.envbox.net:8080/getUparStations'
        response = requests.get(url,headers=header,timeout=(6.05, 27.05))
        response.raise_for_status()
        response.encoding = response.apparent_encoding
    res = json.loads(response.text)
#    print("==========================总共有" + str(len(res))+'数据')

###############################################################
    o_path = path  # 年份路径

    all_date_list = getAllDayPerYear(query_time)

    for j in all_date_list:
        path = o_path
        timeArray = j.split("-")

        otherStyleTime = str(timeArray[0]) + "-" + str(timeArray[1])
        print("==========================正在处理第" + str(otherStyleTime) + "-" + str(timeArray[2]) + "数据")

        path += str(otherStyleTime) + "/"
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            print("==========================创建月份目录成功")

        for i in res:
            path = o_path + str(otherStyleTime) + "/"

            print("==========================正在处理" + str(i[0]) + '-' + str(i[2]) + " 第" + str(otherStyleTime) + "-" + str(timeArray[2]) + "数据")
            path += str(otherStyleTime) + "-" + str(timeArray[2]) + "/"
            name = path + str(i[0]) + '-' + str(i[2]) + '-' + str(i[1]) + '-' + str(j) + '-' + str((0 if UTC == '00' else 12)) + '.csv'

            isExists = os.path.exists(path)
            # 判断结果
            # 如果不存在则创建目录    　
            if not isExists:
                os.makedirs(path)
                print("==========================创建成功")
            # else:
            # 如果目录存在则不创建，并提示目录已存在
            # print("==========================目录存在,不需重新创建")
            my_file = Path(path + "index.txt")
            if my_file.exists():
                print("==========================该日期已经执行完毕跳过")
                break

            my_file = Path(name)
            if my_file.exists():
                print("==========================该城市指定的文件存在，跳过下载下一个文件")
                # 指定的文件存在
                continue

            header = {
                "User-Agent": ua.random,
                'Host': 'api.envbox.net:8080',
                'Origin': 'http://envbox.net',
                'Referer': 'http://envbox.net/upar/upar_chn_mul_hor.html'
            }

            download_url = "http://api.envbox.net:8080/getUparDataByStation?Station_ID_C=%s&date=%s&hour=%s" % (
            i[1], str(otherStyleTime) + "-" + str(timeArray[2]), UTC)

            r = requests.get(download_url, headers=header, timeout=(6.05, 27.05))

            with open(name, "wb") as code:
                code.write(r.content)
            print("==========================文件下载成功，执行下一个任务")
            print('==========================防止被封延时等待5秒钟再处理')
            for n in range(5):
                print("5秒倒计时==========================" + str(5 - n)),
                time.sleep(1)
        print("==========================该日期所有城市已经执行完毕跳过")
        with open(path + "index.txt", "w") as code:
            code.write('当前日期任务成功判断文件')

    print("==========================该年份所有城市已经执行完毕跳过")
    with open(path + "index.txt", "w") as code:
        code.write('当前年份任务成功判断文件')



def isLeapYear(years):
    '''
    通过判断闰年，获取年份years下一年的总天数
    :param years: 年份，int
    :return:days_sum，一年的总天数
    '''
    # 断言：年份不为整数时，抛出异常。
    assert isinstance(years, int), "请输入整数年，如 2018"

    if ((years % 4 == 0 and years % 100 != 0) or (years % 400 == 0)):  # 判断是否是闰年
        # print(years, "是闰年")
        days_sum = 366
        return days_sum
    else:
        # print(years, '不是闰年')
        days_sum = 365
        return days_sum


def getAllDayPerYear(years):
    '''
    获取一年的所有日期
    :param years:年份
    :return:全部日期列表
    '''
    start_date = '%s-1-1' % years
    a = 0
    all_date_list = []
    days_sum = isLeapYear(int(years))
    print()
    while a < days_sum:
        b = arrow.get(start_date).shift(days=a).format("YYYY-MM-DD")
        a += 1
        all_date_list.append(b)
    # print(all_date_list)
    return all_date_list


def is_valid_date(str):
  '''判断是否是一个有效的日期字符串'''
  try:
    time.strptime(str, "%Y-%m-%d")
    return True
  except:
    return False

if __name__ == '__main__':
    qx_city()

    # 获取一年的所有日期
    # all_date_list = getAllDayPerYear("2019")
    # print(all_date_list)
