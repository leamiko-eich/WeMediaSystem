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
        self.login_url = 'https://www.facebook.com/home.php'
        # self.login_url = 'https://blog.csdn.net/'
        self.name_selenium = "facebook"
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
        driver.refresh()        # facebook访问完之后会自动弹出登录窗口
        # time.sleep(5)
        # driver.find_element(By.CSS_SELECTOR, value="[href='https://www.facebook.com/onthisday/?source=bookmark']").click()
        time.sleep(10)  # 等待登录
        cookie = driver.get_cookies()
        print(cookie)
        jsonCookies = json.dumps(cookie)
        with open('data/%s_%s.json' % (self.name_selenium, username), 'w') as f:
            print("写cookie")
            f.write(jsonCookies)
        time.sleep(5)

    def login_with_cookie(self, username = ''):

        chrome_options = self.get_chrome_options()
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 1)

        driver.maximize_window()
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
        time.sleep(3)
        driver.refresh()
        driver.get(self.login_url)
        time.sleep(3)
        self.driver = driver
        return driver

    def public_article(self, article_title, article_content, author, abstract="开发语言的区别", context_label="编程语言", font='简约', background_color = 1):
        """font 可以取值：[简约, 清逸, 闲适, 华丽, 标题]
        background_color 取值1~16
        """
        self.driver.refresh()
        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, value="[href='/stories/create/']").click()        # 点击快拍
        # 选择文字快拍
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, value="[class='x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1bhdf0j']").click()
        # 获取文本输入句柄
        time.sleep(2)
        context_input = self.driver.find_element(By.CSS_SELECTOR, value="[class='x1i10hfl xggy1nq x1s07b3s xjbqb8w x76ihet xwmqs3e x112ta8 xxxdfa6 x9f619 xzsf02u x78zum5 x1jchvi3 x1fcty0u x132q4wb xyorhqc xaqh0s9 x1a2a7pz x6ikm8r x10wlt62 x1pi30zi x1swvt13 xtt52l0 xh8yej3']")
        context_input.send_keys(article_content)
        # 设置字体
        time.sleep(2)
        self.driver.execute_script("document.getElementsByClassName('x6s0dn4 x78zum5 xl56j7k x1yrsyyn xsyo7zv x10b6aqq x16hj40l xn80e1m')[0].innerText='{}'".format(font))
        # 设置背景色
        time.sleep(1)
        self.driver.find_elements(By.CSS_SELECTOR, value="[class='x16wdlz0 x1guw455']")[background_color-1].click()

        # 发布按钮
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, value="[class='x1n2onr6 x1ja2u2z x78zum5 x2lah0s xl56j7k x6s0dn4 xozqiw3 x1q0g3np xi112ho x17zwfj4 x585lrc x1403ito x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xn6708d x1ye3gou xtvsq51 x1r1pt67']").click()

        print("内容发布成功。")

if __name__ == '__main__':
    ob_Crawler = Crawler()
    username = '18511400892'
    # username = '18511400319'
    # ob_Crawler.login_with_password()
    driver = ob_Crawler.login_with_cookie(username)
    article_title = "我和二哈的日常"
    article_content = "每天早上，当你醒来的时候，你会看到你的忠实伙伴——那只可爱的二哈，已经在床边等候，一双明亮的蓝色眼睛充满了期待。它似乎总是在早晨醒来之前就早早地准备好，等待着与你分享新的一天。"
    author = "那个少年和狗"
    ob_Crawler.public_article(article_title, article_content, author, abstract="开发语言的区别", context_label="编程语言")
