import selenium 
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

#https://imshusheng.com/

from Base_piliang import Base_piliang
class toutiao(Base_piliang):
    def __init__(self):
        #Base_piliang.__init__(self,'https://www.toutiao.com/')
        super(toutiao, self).__init__('https://www.toutiao.com/',2)

    def ping_lun(self):
        # 获取当前窗口的句柄
        h =self.browser.current_window_handle
        self.browser.find_element_by_css_selector("li.sns.qq").click()
        time.sleep(8)
        # 进入娱乐栏目 /ch/news_entertainment/  /游戏/ch/news_game/  财经 /ch/news_finance/   搞笑/ch/funny/
        self.browser.find_element_by_css_selector("a[href=\"/ch/news_finance/\"]").click()
        time.sleep(3)
        allzan = self.browser.find_elements_by_css_selector("a.link.title")

        i = 0
        p = 0
        while True                      :
              try:
                    print('第' + str(p +  1) + '页第' + str(i + 1) + '条')
                    if i % 10 ==0:
                        Base_piliang.fun_execute_script(self)
                        time.sleep(5)
                        allzan = self.browser.find_elements_by_css_selector("a.link.title")

                     # #需要延迟一下才能获得所有句柄
                    allzan[i].click()
                    time.sleep(2)
                    # #获取所有句柄
                    all_h = self.browser.window_handles
                    self.browser.switch_to.window(all_h[1])

                    self.browser.find_element_by_css_selector("div.c-textarea>textarea").send_keys(self.kewods)
                    self.browser.find_element_by_css_selector("div.c-submit").click()

                    time.sleep(3)
                    self.browser.close()
                    self.browser.switch_to.window(h)
                    i += 1
              except Exception as e:
                    print(e)
                    i += 1
                    self.browser.close()
                    self.browser.switch_to.window(h)
                    continue

if __name__ == "__main__":
    t = toutiao()
    t.ping_lun()

