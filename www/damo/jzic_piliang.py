import selenium
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

#https://imshusheng.com/

from Base_piliang import Base_piliang
class jzic(Base_piliang):
    def __init__(self):
        #Base_piliang.__init__(self,'https://www.toutiao.com/')
        super(jzic, self).__init__('http://www.hjzic.com/')

    def index_category_link(self):
        #第一层链接
        like=self.browser.find_elements_by_css_selector("ul.dropdown-menu.self.borderNone>li.f_size14>a")
        count = 0
        while (count < len(like)):
            tmp=self.browser.find_elements_by_css_selector("ul.dropdown-menu.self.borderNone>li.f_size14>a")[count]
            tmp.click()
            count += 1
            time.sleep(2)
            self.browser.back()
            time.sleep(2)


        #第二层链接
        like1= self.browser.find_elements_by_css_selector("div.menuShow_left.pull-left>a")
        # 第三层链接
        like2 = self.browser.find_elements_by_css_selector("div.menuShow_content.pull-left>ul>li>a")


if __name__ == "__main__":
    t = jzic()
    t.index_category_link()

