#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pymysql

class Mysql:
    __instance=None         #定义一个变量，来接收实例化对象，方便下面做判断
    def __init__(self,ip,port):
            self.ip = ip
            self.port = port

    @classmethod
    def from_conf(cls):
        if cls.__instance is None:
            cls.__instance =  pymysql.connect(host='106.14.127.145', user='kaifa', passwd='yB8FtzFSlSa5QYE0vzd8', db='jzdzzj', port=3306)
        return cls.__instance

db=Mysql.from_conf()


cursor = db.cursor()

# SQL 查询语句
sql = "SELECT * FROM ic_menbers limit 1 "

try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()

    print(results)
    for row in results:
        fname = row[0]
        lname = row[1]
        age = row[2]
        sex = row[3]
        income = row[4]
        # 打印结果
        print("fname=%s,lname=%s,age=%s,sex=%s,income=%s" % \
              (fname, lname, age, sex, income))
except:
    print("Error: unable to fetch data")

# 关闭数据库连接
db.close()