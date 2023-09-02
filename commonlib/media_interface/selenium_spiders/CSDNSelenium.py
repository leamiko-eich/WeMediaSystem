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
from selenium.webdriver.common.keys import Keys

try:
    from .BaseSelenium import BaseSelenium
except Exception as e:
    from BaseSelenium import BaseSelenium

 
class Crawler(BaseSelenium):
    def __init__(self):
        self.login_url = 'https://blog.csdn.net/'
        self.name_selenium = "CSDN"
        super().__init__(login_url=self.login_url, name_selenium=self.name_selenium)


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
        driver.get(self.login_url)
        driver.maximize_window()
        time.sleep(10)
        driver.find_element(By.CSS_SELECTOR, value="[class='toolbar-btn-loginfun']").click()
        time.sleep(3)
        cookie = driver.get_cookies()
        print(cookie)
        jsonCookies = json.dumps(cookie)
        with open('data/%s_%s.json' % (self.name_selenium, username), 'w') as f:
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
        driver.get(self.login_url)
        time.sleep(2)
    
        f1 = open('data/%s_%s.json' % (self.name_selenium, username))
        cookie = f1.read()
        cookie = json.loads(cookie)
        for c in cookie:
            print("add :", c)
            driver.add_cookie(c)
        
        # 重新登陆
        driver.get(self.login_url)
        driver.maximize_window()
        time.sleep(3)
        self.driver = driver
        return driver
    
       
    def public_article(self, article_title, article_content, author, abstract="开发语言的区别", context_label="编程语言"):
        self.driver.refresh()
        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, value="[class='toolbar-btn toolbar-btn-write toolbar-btn-write-new csdn-toolbar-fl toolbar-subMenu-box']").click()
        time.sleep(3)
        # 清除样式提示
        self.driver.find_element(By.CSS_SELECTOR, value="[class='editor__inner markdown-highlighting']").clear()
        # 标题
        title_input = self.driver.find_element(By.CSS_SELECTOR, value="[class='editor__inner markdown-highlighting']")
        title_input.send_keys('#' + article_title + Keys.ENTER)
        time.sleep(1)
        context_input = self.driver.find_element(By.CSS_SELECTOR, value="[class='editor__inner markdown-highlighting']")
        context_input.send_keys(article_content)
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, value="[class='btn btn-publish']").click()
        time.sleep(1)
        # 选择文章标签
        self.driver.find_element(By.CSS_SELECTOR, value="[class='tag__btn-tag']").click()
        time.sleep(1)
        # 自定义标签
        self.driver.find_element(By.CSS_SELECTOR, value="[class='el-input__inner']").send_keys(context_label + Keys.ENTER)
        # 关闭标签选项
        self.driver.find_element(By.CSS_SELECTOR, value="[class='modal__close-button button']").click()
        time.sleep(1)
        # 封面图片
        cov_img = self.driver.find_element(By.CSS_SELECTOR, value="[class='el-upload__input']")
        cov_img.send_keys("F:/MyWorks/captain/imgs/R.jpg")
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, value="[class='el-textarea__inner']").send_keys(abstract)
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, value="[class='button btn-b-red ml16']").click()
        time.sleep(1)

        print("内容发布成功。")


if __name__ == '__main__':
    ob_Crawler = Crawler()
    username = '18511400889'
    # ob_Crawler.load_user_pass()
    # ob_Crawler.login_with_password()
    driver = ob_Crawler.login_with_cookie(username)
    title = "Java和js是什么关系？"
    context = "Java和JavaScript（JS）是两种不同的编程语言，它们之间存在一些相似之处，但也有许多区别。这些相似性主要是因为它们的名字相似，但它们的用途、语法和生态系统都有很大的差异。"
    author = "麻辣烫不要辣" # article_title
    ob_Crawler.public_article(article_title=title, article_content=context, author=author)

