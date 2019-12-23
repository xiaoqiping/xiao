'''
Created on 2019年6月11日

@author: jzic-001
'''
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import pymysql
import time

class mydb:
    def __init__(self):
        self.conn = False
    
    def db_connect(self):
        '''
        连接数据库
        '''
        while True:
            try:
                self.conn = pymysql.connect(host='106.14.127.145', user='kaifa', passwd='yB8FtzFSlSa5QYE0vzd8', db='jzic_crawl_data', port=3306, charset='utf8')
                #self.conn.autocommit(True)
                self.cursor = self.conn.cursor()
                break
            except pymysql.Error() as e:
                print(e)
                time.sleep(60);
        return True
    
    def db_close(self):
        '''
        关闭数据库连接
        '''
        self.conn.close()
    
    def db_isconnect(self):
        '''
        检查数据库连接状态，断开后重新连接数据库
        '''
        try:
            self.conn.ping()
            return True
        except:
            return self.db_connect()
            
    def db_insert(self, data):
        '''
        数据插入
        '''
        self.db_isconnect()
        try:
            # 执行sql语句，插入记录
            sql = "INSERT INTO mlcc_goods_series_module (`series_id`,`module`,`module_url`) VALUES (%s, %s, %s);"
            if isinstance(data, list):
                print('批量插入')
                self.cursor.executemany(sql, data)
            else:
                print('单条插入')
                self.cursor.execute(sql, data)
            self.conn.commit()

        except pymysql.MySQLError() as e:
            print(e)
    
    def db_select(self, num):
        '''
        查询一条记录
        '''
        self.db_isconnect()
        try:
            # 执行sql语句，查询记录
            sql = "SELECT * FROM mlcc_goods_series WHERE handle_status=0 LIMIT {};"
            sql = sql.format(num)
            data = self.cursor.execute(sql)
            if(data>0):
                return self.cursor.fetchall()
            else:
                return False
        except pymysql.MySQLError() as e:
            print(e)

    def db_update(self, handle_status, series_id):
        '''
        更新记录
        '''
        self.db_isconnect()
        try:
            # 执行sql语句，查询记录
            sql = "UPDATE mlcc_goods_series SET handle_status={} WHERE series_id={};"
            sql = sql.format(handle_status,series_id)
            data = self.cursor.execute(sql)
            self.conn.commit()
            if(data>0):
                return True
            else:
                return False
        except pymysql.MySQLError() as e:
            print(e)

def get_module(series_id, series_url):
    '''
    获取系列下的型号
    '''
    global db, browser
    
    isOver = 0
    
    while True:
        
        if 1==isOver:
            break
        print('当前请求页：' + series_url)
        
        while True:
            try:
                browser.get(series_url)
                break
            except:
                browser.execute_script('window.stop()')
                time.sleep(60)
        
        bs = BeautifulSoup(browser.page_source, 'lxml')
        divObj = bs.find('div', attrs={"class":"server_right"})
        if None == divObj:
            print('服务器返回空页面，等待5分钟')
            time.sleep(300)
            continue
        aArr = divObj.findAll('a')
        dataArr = []
        for aObj in aArr:
            if '首页'==aObj.get_text() : 
                continue
            elif '上一页'==aObj.get_text():
                continue
            elif '下一页'==aObj.get_text():
                if 'href' in aObj.attrs:
                    # 本页处理完毕 进入下一页
                    print('进入下一页')
                    series_url = 'http://www.mlcc1.com' + aObj.attrs['href']
                    db.db_insert(dataArr)
                    dataArr.clear()
                else:                    
                    db.db_insert(dataArr)
                    dataArr.clear()
                    db.db_update(2,series_id)
                    isOver = 1
                    print('系列采集完毕' + series_id.__str__())
                break
            elif '尾页'==aObj.get_text():
                continue
            else:
                module = aObj.get_text()
                module_url = aObj.attrs['href']
                dataArr.append((series_id, module, module_url))

db = mydb()
db.db_connect()

options = Options()
options.add_argument('--headless')
#options.add_argument('--proxy-server=http://27.46.22.185:888')
browser = webdriver.Firefox(executable_path="D:/spider/geckodriver.exe", firefox_options=options)
browser.set_page_load_timeout(60)
browser.set_script_timeout(60)

#get_module(1130, 'http://www.mlcc1.com/mlcc_list/brand/15/id/950/p/378.html')

while True:    
    data = db.db_select(1)
    if False == data:
        break
    for row in data:
        db.db_update(1,row[0])
        get_module(row[0], 'http://www.mlcc1.com' + row[3])
print ("采集完毕")

browser.close()

# python D:\spider\mlcc_goods_series_module_selenium_firefox.py

