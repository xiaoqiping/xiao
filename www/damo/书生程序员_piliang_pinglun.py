import selenium
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
kewods = '[红包]支付宝大额红包！ 瓜分15亿！打开支付宝首页搜数字“打开支付宝首页搜索“527479816” 立即领红包” 立即领取。昨天领到几块甚至几十块的人超级多，快试试吧。～[礼物]记得收藏，红包每天都可以领！'
#https://imshusheng.com/

browser = webdriver.Firefox(executable_path ="D:\geckodriver")
browser.get('https://imshusheng.com/')
browser.implicitly_wait(30)

#获取当前窗口的句柄
h  = browser.current_window_handle
allzan = browser.find_elements_by_css_selector("div.media-heading>a")

# js="document.documentElement.scrollTop=10000"
# browser.execute_script(js)


i=0
p=0
while True:
    try:
        print('第' + str(p+1) + '页第' + str(i+1) + '条')
        if i==20:
            i=0
            p+=1
            browser.get('https://imshusheng.com/page/'+str(p)+'/')
            time.sleep(2)
            allzan= browser.find_elements_by_css_selector("div.media-heading>a")

        # #需要延迟一下才能获得所有句柄
        allzan[i].click()
        time.sleep(2)
        # #获取所有句柄
        all_h = browser.window_handles

        browser.switch_to.window(all_h[1])
        browser.find_element_by_css_selector("textarea#reply-content").send_keys(kewods)
        browser.find_element_by_css_selector("input#reply-create-submit").click()
        time.sleep(1)
        browser.close()
        browser.switch_to.window(h)
        i+=1
    except Exception as e:
        i+= 1
        continue




#
# #需要延迟一下才能获得所有句柄
# time.sleep(2)
# #获取所有句柄
# all_h = browser.window_handles
#
# #切换到子窗口句柄
# browser.switch_to.window(all_h[1])
#
#
# browser.find_element_by_css_selector("textarea#reply-content").send_keys('haha')
#
# #browser.find_element_by_css_selector("input#reply-create-submit").click()
# time.sleep(1)
#
# #关闭子窗口
# browser.close()
# #切换到首页句柄
# browser.switch_to.window(h)






