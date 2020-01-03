#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-

import pymysql
class mysql(object):
    conn = None

    def __init__(self, host='106.14.127.145', user='kaifa', password='yB8FtzFSlSa5QYE0vzd8', db='jzic_crawl_data_v2', charset='utf8', port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.port = port

    def connect(self):
        try:
            self.conn.ping(reconnect=True)
            self.cursor = self.conn.cursor()
        except:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,db=self.db, charset=self.charset)
            self.cursor = self.conn.cursor()


    def close(self):
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()
        return True
        #self.cursor.close()
        #self.conn.close()

    def get_one(self, sql, params=()):
        result = None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            self.close()
        except Exception as e:
            self.close()
            print(e)
        return result

    def get_all(self, sql, params=()):
        list_data = ()
        try:
            self.connect()
            self.cursor.execute(sql, params)
            list_data = self.cursor.fetchall()
            self.close()
        except Exception as e:
            self.close()
            print(e)
        return list_data

    def insert(self, sql, params=()):
        return self.edit(sql, params)

    def update(self, sql, params=()):
        return self.edit(sql, params)

    def delete(self, sql, params=()):
        return self.edit(sql, params)

    def edit(self, sql, params):
        count = 0
        try:
            self.connect()
            if isinstance(params, list):
                count = self.cursor.executemany(sql, params)
            else:
                count = self.cursor.execute(sql, params)
            self.conn.commit()
            self.close()
        except Exception as e:
            self.close()
            print(e)
            return None
        return count