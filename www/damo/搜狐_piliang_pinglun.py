import selenium
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
kewods = '打开支付宝首页搜索“527479816”，即可领红包'
#https://imshusheng.com/

browser = webdriver.Firefox(executable_path ="D:\geckodriver")

#http://business.sohu.com/998
browser.get('http://business.sohu.com/998')
browser.implicitly_wait(30)

#获取当前窗口的句柄
h  = browser.current_window_handle

time.sleep(10)

allzan = browser.find_elements_by_css_selector("div.news-list.clearfix>div>div>div>h4>a")

# js="document.documentElement.scrollTop=10000"
# browser.execute_script(js)
browser.execute_script(""" 
        (function () { 
            var y = document.body.scrollTop; 
            var step = 100; 
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
            setTimeout(f, 3000); 
        })(); 
        """)


i=0
p=0
while True:
    try:
        print('第' + str(p+1) + '页第' + str(i+1) + '条')
        if i == 20:
            allzan = browser.find_elements_by_css_selector("div.news-list.clearfix>div>div>div>h4>a")

        # #需要延迟一下才能获得所有句柄
        allzan[i].click()
        time.sleep(3)
        # #获取所有句柄
        all_h = browser.window_handles
        #跳转到子窗口句柄
        browser.switch_to.window(all_h[1])

        browser.find_element_by_css_selector("textarea.c-comment-textbox").clear()
        browser.find_element_by_css_selector("textarea.c-comment-textbox").send_keys(kewods)
        browser.find_element_by_css_selector("div.c-submit-btn.c-submit ").click()
        time.sleep(2)
        browser.close()
        browser.switch_to.window(h)
        i+=1
    except Exception as e:
        print(e)
        i += 1
        browser.close()
        browser.switch_to.window(h)
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






