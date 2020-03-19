# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import traceback
import MySQLdb
import pymysql
import hashlib


def main():
    try:
        crawl_url("face+mask", 12)
    except:
        print('main:' + traceback.format_exc())

def crawl_url(keyworks, start):
    browser = False
    try:
        url = 'https://sourcing.alibaba.com/rfq_search_list.htm?spm=a2700.8073608.1998677539.4.724e65aa3w01bd&searchText=%s&openTime=3i' % keyworks
        options = Options()
        options.add_argument('--headless')
        browser = webdriver.Firefox(executable_path = 'D:/geckodriver.exe', options=options)
        print("-------------crawl start-------------")

        for i in range(start, 251):
            browser.get("%s&page=%d" % (url, i))
            WebDriverWait(browser, 10).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR,'.rfqSearchList')))
            pageSource = browser.page_source
            data = parse_data(pageSource)
            print("crawl current:%d num:%d" % (i, len(data)))
            print("write mysql start")
            wirte_mysql(data)
            print("write mysql end")
            #time.sleep(1)
        browser.close()
        browser = False
        '''
        print("-------------crawl end-------------")
        print("-------------write csv start-------------")
        #headers = ["subject", "quantity", "country", "detail", "buyerInfo", "buyerTag", "quoteLeft"]
        headers = ["标题", "采购量", "发布地点", "描述", "发布者", "标签", "剩余报价位"]
        wirte_csv("data.csv", headers, datas)
        print("-------------write csv end-------------")
        '''
    except:
        print('crawl_url:' + traceback.format_exc())
    finally:
        if browser:
            browser.close()

def ceshi():
    try:
        datas = parse_data(read_file("a.txt"))
        wirte_mysql(datas)
    except:
        print('ceshi:' + traceback.format_exc())

def parse_data(content):
    datas = []
    try:
        soup = BeautifulSoup(content,"html.parser")
        searchContents = soup.select("#rfqSearchindex .alife-bc-brh-rfq-list__row")
        for item in searchContents:
            data = {}
            m = hashlib.md5()
            m.update(item.select(".brh-rfq-item__subject-link")[0].attrs["href"].encode("utf8"))
            data["link"] = m.hexdigest()
            data["subject"] = item.select(".brh-rfq-item__subject")[0].get_text()
            data["quantity"] = "%s %s" % (item.select(".brh-rfq-item__quantity span")[1].get_text(), item.select(".brh-rfq-item__quantity span")[2].get_text())
            data["country"] = item.select(".brh-rfq-item__country")[0].get_text()
            data["detail"] = item.select(".brh-rfq-item__detail")[0].get_text() if len(item.select(".brh-rfq-item__detail")) else ""
            data["buyerInfo"] = item.select(".brh-rfq-item__other-info .text")[0].get_text()
            data["buyerTag"] = ",".join([tag.get_text() for tag in item.select(".brh-rfq-item__buyer-tag .next-tag-body")])
            data["quoteLeft"] = item.select(".brh-rfq-quote-now span")[0].get_text()
            datas.append(data)
    except:
        print('parse_data:' + traceback.format_exc())
    finally:
        return datas

def wirte_mysql(datas):
    try:
        db = MySQLdb.connect("106.14.127.145", "kaifa", "yB8FtzFSlSa5QYE0vzd8", "jzic_crawl_data_v2", charset='utf8' )
        cursor = db.cursor()
        for data in datas:
            try:
                sql = "SELECT count(*) FROM data_v1 WHERE link = '%s'" % data["link"]
                cursor.execute(sql)
                results = cursor.fetchone()
                if int(results[0]) == 0:
                    cursor.execute('insert into data_v1 values(null, "%s","%s", "%s", "%s", "%s", "%s", "%s", "%s")' % \
                     (pymysql.escape_string(data["link"]), \
                        pymysql.escape_string(data["subject"]), \
                        pymysql.escape_string(data["quantity"]), \
                        pymysql.escape_string(data["country"]), \
                        pymysql.escape_string(data["detail"]), \
                        pymysql.escape_string(data["buyerInfo"]), \
                        pymysql.escape_string(data["buyerTag"]), \
                        pymysql.escape_string(data["quoteLeft"])) \
                     )
                    db.commit()
            except:
                print('wirte_mysql:' + traceback.format_exc())
                db.rollback()
        db.close()
    except:
        print('wirte_mysql:' + traceback.format_exc())

def export_data():
    try:
        datas = []
        db = MySQLdb.connect("106.14.127.145", "kaifa", "yB8FtzFSlSa5QYE0vzd8", "jzic_crawl_data_v2", charset='utf8')
        cursor = db.cursor()
        page = 1
        page_size = 1000
        try:
            while True:
                start_idx = (page - 1) * page_size
                sql = "SELECT * FROM data_v1 Limit %d,%d" % (start_idx, page_size)
                cursor.execute(sql)
                # 获取所有记录列表
                results = cursor.fetchall()
                print("page:%d, num:%d", (start_idx, len(results)))
                if len(results) == 0:
                    break
                for row in results:
                    data = {}
                    data["subject"] = str(row[2])
                    data["quantity"] = str(row[3])
                    data["country"] = str(row[4])
                    data["detail"] = str(row[5])
                    data["buyerInfo"] = str(row[6])
                    data["buyerTag"] = str(row[7])
                    data["quoteLeft"] = str(row[8])
                    datas.append(data)  
                page += 1  
        except:
            print('export_data:' + traceback.format_exc())
        db.close()
        headers = ["subject", "quantity", "country", "detail", "buyerInfo", "buyerTag", "quoteLeft"]
        wirte_csv("data.csv", headers, datas)
    except:
        print('export_data:' + traceback.format_exc())

def wirte_csv(file, headers, datas):
    try:
        with open(file,'w', newline='', encoding="utf-8") as f:
            f_csv = csv.DictWriter(f, headers)
            f_csv.writeheader()
            f_csv.writerows(datas)
    except:
        print('wirte_csv:' + traceback.format_exc())

def write_file(file, content):
    f = open(file, "w", encoding='utf-8')
    f.write(content)
    f.close()

def read_file(file):
    f = open(file, "r", encoding='utf-8')
    con = f.read()
    f.close()
    return con

if __name__ == "__main__":
    #main()
    export_data()