import selenium
import time
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
class Base_piliang(object):
    kewods = '粽子节福利哦!打开支付宝首页搜索“527479816” 立即领红包'

    def __init__(self,url,web_type = 2 ):
        self.url = url
        if web_type == 2:
            self.browser = webdriver.Chrome(executable_path="D:\chromedriver")
        else:
            self.browser = webdriver.Firefox(executable_path="D:\geckodriver")
        self.browser.get(self.url)
        self.browser.implicitly_wait(10)

    def login_set(self,loginname,password):
        loginname_val=sys._getframe().f_back.f_locals[loginname]
        password_val = sys._getframe().f_back.f_locals[password]
        self.browser.find_element_by_id(loginname).clear()
        self.browser.find_element_by_id(loginname).send_keys(loginname_val)
        self.browser.find_element_by_name(password).send_keys(password_val)

    #滚动条
    def fun_execute_script(self):
        self.browser.execute_script(""" 
            (function () { 
                var y = document.body.scrollTop; 
                var step = 3000; 
                window.scroll(0, y); 
                function f() { 
                    if (y < document.body.scrollHeight) { 
                        y += step; 
                        window.scroll(0, y); 
                        setTimeout(f, 50); 
                    }
                    else { 
                        window.scroll(0, y); 
                        document.title += "scroll-done"; 
                    } 
                } 
                f();
               // setTimeout(f, 3000); 
            })(); 
            """)

    def is_element_exist(self,css):

        s =  self.browser.find_elements_by_css_selector(css_selector=css)
        if len(s) == 0:
            return False
        elif len(s) == 1:
            return True
        else:
            return False