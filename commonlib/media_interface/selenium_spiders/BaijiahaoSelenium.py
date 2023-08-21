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
        self.logurl = 'https://baijiahao.baidu.com/'

    def get_options(self):
        chrome_options = Options()

        chrome_options.add_argument("window-size=1024,768")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.4515.107 Safari/537.36')

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
        driver.get(self.logurl)
        driver.maximize_window()
        time.sleep(10)
        driver.find_element(By.CSS_SELECTOR, value="[class='btnlogin--i1pF9']").click()
        driver.refresh()
        time.sleep(2)
        cookie = driver.get_cookies()
        print(cookie)
        jsonCookies = json.dumps(cookie)
        with open('data/%s.json' % (username), 'w') as f:
            print("写cookie")
            f.write(jsonCookies)
        time.sleep(10)

    def login_with_cookie(self, username = ''):

        chrome_options = self.get_chrome_options()
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 1)

        ##登录百度知道
    
        #登录前清楚所有cookie
        driver.delete_all_cookies()
        driver.get(self.logurl)
        time.sleep(2)
    
        f1 = open('data/%s.json' % (username))
        cookie = f1.read()
        cookie = json.loads(cookie)
        for c in cookie:
            print("add :", c)
            driver.add_cookie(c)
        
        # 重新登陆
        driver.get(self.logurl)
        driver.maximize_window()
        time.sleep(3)
        return driver
        

    def get_context(self, driver):
        # 刷新页面
        driver.refresh()
        time.sleep(2)
        driver.find_elements(By.CSS_SELECTOR, value="[class='all-btn']")[1].click()
        windows = driver.window_handles
        driver.switch_to.window(windows[1])
        time.sleep(10)
        context = defaultdict(list)
        hot_lost = driver.find_elements(By.CSS_SELECTOR, value="[class='client_pages_hotspotCenter_components_listItem']")
        for i, item_driver in enumerate(hot_lost):
            time.sleep(1)
            if i != 0 and i % 2 == 0:
                driver.execute_script("window.scrollBy(0,500)") # 一屏两条热点，后续可以考虑直接定位到元素可见的位置。
            item_driver.click()
            time.sleep(2)
            windows = driver.window_handles
            driver.switch_to.window(windows[2])
            time.sleep(1)
            # 获取热点信息
            title = driver.find_element(By.CLASS_NAME, value="client_pages_hotspotEvents_components_eventContentInfo").find_element(By.CLASS_NAME, value="content-info-title").get_attribute("innerText")
            text = driver.find_element(By.CSS_SELECTOR, value="[class='longWorldFold-content-wrap longWorldFold-font-style']").find_element(By.CLASS_NAME, value="longWorldFold-content").get_attribute("innerText")
            image = driver.find_element(By.CLASS_NAME, value="client_pages_hotspotEvents_components_eventContentInfo").find_element(By.CLASS_NAME, value="content-info-img-wrap").find_element(By.CLASS_NAME, value="content-info-img").get_attribute("src")
            status = driver.find_element(By.CLASS_NAME, value="content-info-status-wrap").find_element(By.CLASS_NAME, value="status-item").text
            date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 数据入库
            # =================== #
            # 关闭当前页面
            time.sleep(2)
            driver.close()
            driver.switch_to.window(windows[1])
            context[title] = [status, date_str, text, image]

            return context

if __name__ == '__main__':
    ob_Crawler = Crawler()
    username = '18511400888'
    # username = '18511400319'
    # ob_Crawler.load_user_pass()
    ob_Crawler.login_with_password()
    driver = ob_Crawler.login_with_cookie(username)
