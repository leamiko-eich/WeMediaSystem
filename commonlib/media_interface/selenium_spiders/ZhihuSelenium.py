#encoding=utf-8
from BaseSelenium import BaseSelenium
import time,json
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

class ZhihuSelenium(BaseSelenium):
    def __init__(self):
        super().__init__()
        self.name_selenium = 'Zhihu'
        self.login_url = 'https://www.zhihu.com'

    def use_firefox(self):

        # options.headless = True

        options = Options()
        options.set_preference('profile',  r'C:\Users\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\3opi7avg.default-release')

        driver = webdriver.Firefox(options=options)

        # profile = FirefoxProfile(r'C:\path\to\my_profile')
        # driver = webdriver.Firefox(options=options, firefox_profile=profile) 
        driver.get("https://www.zhihu.com")

        time.sleep(60)
        driver.quit()

    def output_cookies(self, cookies):
        for cookie in cookies:
            print(cookie)

    def login_with_password(self, username=''):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("window-size=1024,768")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')
   
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-browser-side-navigation')
        chrome_options.add_argument('enable-automation')

        # options = webdriver.ChromeOptions()
        # options = self.get_chrome_options( )

        driver = webdriver.Chrome(options=chrome_options)

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
          "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })

        ## 临时使用扫码进行第1次登录解决
        driver.get("https://www.zhihu.com")

        # driver.delete_all_cookies()

        time.sleep(30)
        filename = "%s_%s" % (self.name_selenium, username)
        self.persist_cookie_info(driver, filename)

        time.sleep(30)
        driver.quit()

    def login_with_cookie(self, username = ''):
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
   
        time.sleep(2)
        logurl = self.login_url
    
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
 


    def publish_article(self, article_title, article_content):


        driver = webdriver.Chrome(options=options)
        driver.get("https://www.zhihu.com")

        time.sleep(30)
        return
        # Click the "写文章" button
        write_article_button = self.driver.find_element_by_xpath("//button[@class='Button WriteIndex-articleButton Button--primary Button--blue']")
        write_article_button.click()
        
        # Input the article title
        title_input = self.driver.find_element_by_xpath("//input[@class='Input WriteIndex-titleInput']")
        title_input.send_keys(article_title)
        
        # Input the article content
        content_input = self.driver.find_element_by_xpath("//div[@class='public-DraftEditor-content']")
        content_input.send_keys(article_content)
        
        # Click the "发布" button
        publish_button = self.driver.find_element_by_xpath("//button[@class='Button PublishPanel-submitButton Button--primary Button--blue']")
        publish_button.click( )
        
        
if __name__ == "__main__":
    obj_zhihu_selenium = ZhihuSelenium()
    title = "1111"
    content ="2222"
    username = '18511400319'
    # obj_zhihu_selenium.login_with_password(username)
    obj_zhihu_selenium.login_with_cookie(username)