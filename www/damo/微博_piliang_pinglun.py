import selenium
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
kewods = '打开支付宝首页搜索“527479816”，即可领红包'

browser = webdriver.Firefox(executable_path ="D:\geckodriver")
browser.get('https://weibo.com/login.php')
browser.implicitly_wait(30)

#获取当前窗口的句柄
currentWin = browser.current_window_handle

browser.find_element_by_id('loginname').clear()
browser.find_element_by_id("loginname").send_keys('15107332193')
browser.find_element_by_name("password").send_keys('tiamomei713714')
browser.find_element_by_css_selector(".W_btn_a.btn_32px").click()

WebDriverWait(browser,30,1).until(expected_conditions.title_contains("我的首页"))
time.sleep(8)
# 进入校园生活栏目
browser.find_elements_by_css_selector("a[title=\"八卦杂谈\"]")[0].click()

time.sleep(5)
# 所有评论图标
#allzan = browser.find_elements_by_css_selector('span.pos>span>span>em.W_ficon.ficon_repeat.S_ficon')

# time.sleep(3)
# browser.find_elements_by_css_selector('textarea.W_input')[1].send_keys('hahahaha')
# browser.find_elements_by_css_selector('div.p_opt.clearfix>div')[0].click()
#
# allzan = browser.find_elements_by_css_selector('em.W_ficon.ficon_repeat.S_ficon')[0].click()
# allzan = browser.find_elements_by_css_selector('em.W_ficon.ficon_repeat.S_ficon')[1].click()
# browser.find_elements_by_css_selector('textarea.W_input')[2].send_keys('haha')

i = 0
j = 1
p = 1
while True:
#for temp in allzan:
    try:
        allzan = browser.find_elements_by_css_selector('span.pos>span>span>em.W_ficon.ficon_repeat.S_ficon')
        print('第' + str(p)+'页第'+str(j)+'条')
        allzan[i].click()
        time.sleep(2)
        textarea_arr = browser.find_elements_by_css_selector('textarea.W_input')
        textarea_arr[j].send_keys(kewods)
        time.sleep(1)
        #if i>=19:
        browser.find_elements_by_css_selector('div.p_opt.clearfix>div.btn.W_fr')[i].click()
        time.sleep(8)
        if j == 45:
            browser.find_elements_by_css_selector('a.page.next.S_txt1.S_line1')[0].click()
            time.sleep(2)
            p += 1
            i=0
            j=1
        else:
            i+=1
            j+=1
    except Exception as e:
        i += 1
        continue







