import selenium
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import win32api

import win32con
#https://imshusheng.com/

from Base_piliang import Base_piliang
class toutiao(Base_piliang):
    def __init__(self):
        #Base_piliang.__init__(self,'https://www.toutiao.com/')
        super(toutiao, self).__init__('http://quan.qq.com/square?tab=0',2)

    def ping_lun(self):
        h = self.browser.current_window_handle
        self.browser.find_element_by_css_selector("i.ico-usr").click()
        time.sleep(6)
        self.browser.back()
        allzan = self.browser.find_elements_by_css_selector("i.G-ico.G-ico-recommend")

        i = 0
        p = 0
        s = 0
        while True:
            try:
                print('第' + str(p + 1) + '页第' + str(i + 1) + '条')
                if i % 20 == 0 and i !=0 :
                    Base_piliang.fun_execute_script(self)
                    allzan = self.browser.find_elements_by_css_selector("i.G-ico.G-ico-recommend")
                    time.sleep(5)

                allzan[i].click()
                time.sleep(2)
                self.browser.find_element_by_css_selector("div.input").click()
                time.sleep(2)
                self.browser.find_element_by_css_selector("textarea.input-editor").send_keys(self.kewods)
                time.sleep(2)
                self.browser.find_element_by_css_selector("a.fr.green").click()
                time.sleep(2)


                self.browser.back()
                self.browser.back()
                time.sleep(2)

                i += 1
                allzan = self.browser.find_elements_by_css_selector("i.G-ico.G-ico-recommend")
            except Exception as e:
                print(e)
                i += 1
                continue

if __name__ == "__main__":
    t = toutiao()
    t.ping_lun()

