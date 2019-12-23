import pymysql
class mysql(object):
    conn = None

    def __init__(self, host='106.14.127.145', user='kaifa', password='yB8FtzFSlSa5QYE0vzd8', db='jzic_crawl_data', charset='utf8', port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.port = port

    def connect(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db,charset=self.charset)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_one(self, sql, params=()):
        result = None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            self.close()
        except Exception as e:
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
            print(e)
        return list_data

    def insert(self, sql, params=()):
        return self.__edit(sql, params)

    def update(self, sql, params=()):
        return self.__edit(sql, params)

    def delete(self, sql, params=()):
        return self.__edit(sql, params)

    def __edit(self, sql, params):
        count = 0
        try:
            self.connect()
            if isinstance(params, list):

                print(params)
                print('批量插入')
                count = self.cursor.executemany(sql, params)
            else:
                print('单条插入')
                count = self.cursor.execute(sql, params)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e)
        return count