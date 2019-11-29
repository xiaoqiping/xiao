import selenium
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

#https://imshusheng.com/

from Base_piliang import Base_piliang
class toutiao(Base_piliang):
    def __init__(self):
        super(toutiao, self).__init__('https://new.qq.com/rolls/?ext=news',1)

    def ping_lun(self):
        # 获取当前窗口的句柄
        h =self.browser.current_window_handle
        self.browser.find_element_by_css_selector("a.quickLink.loginBtn").click()
        time.sleep(8)
        allzan = self.browser.find_elements_by_css_selector("a.cmt")

        i = 0
        p = 0
        while True                      :
              try:
                    print('第' + str(p +  1) + '页第' + str(i + 1) + '条')
                    if i % 5 ==0 and i !=0:
                        Base_piliang.fun_execute_script(self)
                        time.sleep(5)
                        allzan = self.browser.find_elements_by_css_selector("a.cmt")
                        time.sleep(1)

                    # #需要延迟一下才能获得所有句柄
                    allzan[i].click()
                    time.sleep(2)
                    # #获取所有句柄
                    all_h = self.browser.window_handles
                    self.browser.switch_to.window(all_h[1])
                    self.browser.switch_to_frame("commentIframe")

                    time.sleep(1)
                    self.browser.find_element_by_css_selector("div.box-textarea-block>textarea").send_keys(self.kewods)
                    self.browser.find_element_by_css_selector("div.J_PostBtn").click()

                    time.sleep(2)
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

