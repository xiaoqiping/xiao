import selenium
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

#https://imshusheng.com/

from Base_piliang import Base_piliang
class jianshu(Base_piliang):
    def __init__(self):
        #Base_piliang.__init__(self,'https://www.jianshu.com/')
        super(jianshu, self).__init__('https://www.jianshu.com/',1)

    def ping_lun(self):
        # 获取当前窗口的句柄
        self.browser.find_element_by_css_selector("#sign_in").click()
        time.sleep(1)
        self.browser.find_element_by_css_selector("#qq").click()
        time.sleep(8)

        all_h = self.browser.window_handles
        self.browser.switch_to.window(all_h[1])
        h = self.browser.current_window_handle

        allzan = self.browser.find_elements_by_css_selector("ul.note-list>li>div.content>div.meta>.nickname + a")

        i = 0
        p = 0
        while True:
            try:
                print('第' + str(p + 1) + '页第' + str(i + 1) + '条')
                if i % 10 ==0 and i !=0:
                    Base_piliang.fun_execute_script(self)
                    time.sleep(2)
                    if Base_piliang.is_element_exist(self, '.load-more'):
                        self.browser.find_element_by_css_selector("a.load-more").click()
                    allzan = self.browser.find_elements_by_css_selector("ul.note-list>li>div.content>div.meta>.nickname + a")

                allzan[i].click()
                # #需要延迟一下才能获得所有句柄
                time.sleep(2)
                # #获取所有句柄
                all_h = self.browser.window_handles
                self.browser.switch_to.window(all_h[2])

                self.browser.find_element_by_css_selector("form.new-comment>textarea").send_keys(self.kewods)
                self.browser.find_element_by_css_selector(".btn.btn-send").click()

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
    t = jianshu()
    t.ping_lun()

