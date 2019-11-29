import selenium
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains

#https://imshusheng.com/

from Base_piliang import Base_piliang
class toutiao(Base_piliang):
    def __init__(self):
        super(toutiao, self).__init__('http://blog.cnfol.com/list/1461.html',2)

    def ping_lun(self):
        # 获取当前窗口的句柄
        h =self.browser.current_window_handle

        ele = self.browser.find_element_by_css_selector('a.NewLog')
        # 将鼠标移动到定位的元素上面
        ActionChains(self.browser).move_to_element(ele).perform()

        self.browser.find_element_by_css_selector("a.AQQ").click()
        time.sleep(8)
        allzan = self.browser.find_elements_by_css_selector("ul.BlogArtList.Cf>li>h3>a")

        i = 1
        p = 0
        while True                      :
              try:
                    print('第' + str(p +  1) + '页第' + str(i + 1) + '条')
                    if i % 10 ==0 and i !=0:
                        self.browser.find_element_by_css_selector("button.LoadM").click()
                        allzan = self.browser.find_elements_by_css_selector("ul.BlogArtList.Cf>li>h3>a")

                    # #需要延迟一下才能获得所有句柄
                    allzan[i].click()
                    time.sleep(2)
                    # #获取所有句柄
                    all_h = self.browser.window_handles
                    self.browser.switch_to.window(all_h[1])

                    time.sleep(1)
                    self.browser.find_element_by_css_selector("textarea.js_comment_content").send_keys(self.kewods)
                    self.browser.find_element_by_css_selector("a.sayBtn").click()

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

