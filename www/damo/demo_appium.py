# coding=utf-8
from appium import webdriver
import time, os


class news:
    def __init__(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.1.1'
        desired_caps['deviceName'] = '127.0.0.1:62001'
        desired_caps['appPackage'] = 'com.tencent.mobileqq'
        desired_caps['appActivity'] = '.activity.SplashActivity'
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
if __name__ == '__main__':
    news = news()

