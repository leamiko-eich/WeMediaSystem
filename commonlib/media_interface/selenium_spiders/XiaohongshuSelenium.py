#encoding=utf-8
try:
    from .BaseSelenium import BaseSelenium
except Exception as e:
    from BaseSelenium import BaseSelenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time, json

class XiaohongshuSelenium(BaseSelenium):
    name_platform = 'Xiaohongshu'
    def __init__(self):
        super().__init__()
        self.name_selenium = 'Xiaohongshu'
        # self.login_url = 'https://www.xiaohongshu.com'
        self.login_url = 'https://creator.xiaohongshu.com'

    def login_with_password(self, username=''):
        print("username: %s" % (username))
        url = self.login_url
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("window-size=1024,768")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')
#    
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-browser-side-navigation')
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # chrome_options.add_argument('enable-automation')
        driver = webdriver.Chrome(options=chrome_options)
        # driver = webdriver.Firefox(options=chrome_options)

        # options = Options()
        # options.set_preference('profile',  r'C:\Users\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\3opi7avg.default-release')

        # driver = webdriver.Firefox(options=options)


        driver.get(url)
        print(" 登录")
        time.sleep(30)

        print(" out cookie")
        filename = "%s_%s" % (self.name_selenium, username)
        self.persist_cookie_info(driver, filename)
        print(" cooie over")

        time.sleep(50)
        driver.quit()


    def publish_article(self, article_title, article_content):
        driver = self.driver
        print("type driver:", type(driver))
        driver : webdriver.Chrome = driver
 

        time.sleep(30)
        return



    

if __name__ == "__main__":
    obj_xiaohongshu = XiaohongshuSelenium()
    title = "个人笔记 - 今天怎么样"
    content ="Good Good Study, Day Day Up. 是的"
    username = '18710090164'
    obj_xiaohongshu.login_with_password('18710090164')
    obj_xiaohongshu.login_with_cookie(username, wait_time=5)
    obj_xiaohongshu.publish_article(title, content)
