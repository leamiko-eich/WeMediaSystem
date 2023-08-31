import json
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from collections import defaultdict
try:
    from .BaseSelenium import BaseSelenium
except Exception as e:
    from BaseSelenium import BaseSelenium

 
class Crawler(BaseSelenium):
    def __init__(self):
        self.login_url = 'https://www.kuaishou.com/?isHome=1'
        self.name_selenium = "kuaishou"
        print(self.login_url)
        super().__init__(login_url=self.login_url, name_selenium=self.name_selenium)
        
        

    def get_options(self):
        chrome_options = Options()

        chrome_options.add_argument("window-size=1024,768")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4515.107 Safari/537.36')

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-browser-side-navigation')
        chrome_options.add_argument('enable-automation')
        chrome_options.add_argument('--disable-infobars')
        return chrome_options
   
    def login_with_password(self):
        chrome_options = self.get_chrome_options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.login_url)
        driver.maximize_window()
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, value="[class='guide-btn']").click()
        driver.find_element(By.CSS_SELECTOR, value="[class='user-default']").click()
        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR, value="[class='navbar-list-item']").click()
        driver.refresh()
        cookie = driver.get_cookies()
        print(cookie)
        jsonCookies = json.dumps(cookie)
        with open('data/%s_%s.json' % (self.name_selenium, username), 'w') as f:
            print("写cookie")
            f.write(jsonCookies)
        time.sleep(5)

    # def login_with_cookie(self, username = ''):

    #     chrome_options = self.get_chrome_options()
    #     driver = webdriver.Chrome(options=chrome_options)
    #     wait = WebDriverWait(driver, 1)

    #     ##登录百度知道
    
    #     #登录前清楚所有cookie
    #     driver.maximize_window()

    #     driver.delete_all_cookies()
    #     driver.get(self.login_url)
    #     time.sleep(2)
    #     driver.find_element(By.CSS_SELECTOR, value="[class='guide-btn']").click()

    #     f1 = open('data/%s.json' % (username))
    #     cookie = f1.read()
    #     cookie = json.loads(cookie)
    #     for c in cookie:
    #         print("add :", c)
    #         driver.add_cookie(c)
        
    #     # 重新登陆
    #     time.sleep(3)

    #     driver.refresh()
    #     driver.get(self.login_url)
    #     # driver.maximize_window()
    #     time.sleep(3)
    #     return driver


if __name__ == '__main__':
    ob_Crawler = Crawler()
    username = '18511400891'
    # ob_Crawler.login_with_password()
    # username = '18511400891'

    driver = ob_Crawler.login_with_cookie(username)
