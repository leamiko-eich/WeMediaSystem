#encoding=utf-8
try:
    from .BaseSelenium import BaseSelenium
except Exception as e:
    from BaseSelenium import BaseSelenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import time, json

class XiaohongshuSelenium(BaseSelenium):
    def __init__(self):
        super().__init__()
        self.name_selenium = 'Xiaohongshu'

    def login_with_password(self, username=''):
        print("username: %s" % (username))
        url = 'https://www.xiaohongshu.com'
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("window-size=1024,768")
        # chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')
   
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument('start-maximized')
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-browser-side-navigation')
        # chrome_options.add_argument('enable-automation')
        # chrome_options = self.get_chrome_options()
        # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:5003")
        driver = webdriver.Chrome(options=chrome_options)
        # driver = webdriver.Firefox(options=chrome_options)

        # options = Options()
        # options.set_preference('profile',  r'C:\Users\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\3opi7avg.default-release')

        # driver = webdriver.Firefox(options=options)

        wait = WebDriverWait(driver, 1)

        driver.get(url)
        print(" 登录")
        time.sleep(30)

        filename = "%s_%s" % (self.name_selenium, username)
        self.persist_cookie_info(driver, filename)

        time.sleep(50)
        driver.quit()

    def login_with_cookie(self, username = ''):
        # assert (username in self.dict_user_pass)
        chrome_options = Options()
    
        chrome_options.add_argument("window-size=1024,768")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')
   
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-browser-side-navigation')
        chrome_options.add_argument('enable-automation')
        chrome_options.add_argument('--disable-infobars')

        driver = webdriver.Chrome(options=chrome_options)
   
        wait = WebDriverWait(driver, 1)
    
        ##登录百度知道
        logurl = 'https://www.xiaohongshu.com'
    
        #登录前清楚所有cookie
        driver.delete_all_cookies()
        driver.get(logurl)
        time.sleep(2)
    
        filename = "%s_%s" % (self.name_selenium, username)
        f1 = open('data/%s.json' % (filename))
        cookie = f1.read()
        cookie = json.loads(cookie)
        for c in cookie:
            print("add :", c)
            driver.add_cookie(c)
        # # 刷新页面
        time.sleep(2)
        driver.refresh()

        time.sleep(50)
 



    

if __name__ == "__main__":
    obj_xiaohongshu = XiaohongshuSelenium()
    username = '18511400319'
    obj_xiaohongshu.login_with_password('18511400319')
