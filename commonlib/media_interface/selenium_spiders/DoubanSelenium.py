#encoding=utf-8
try:
    from .BaseSelenium import BaseSelenium
except Exception as e:
    from BaseSelenium import BaseSelenium
import time,json
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DoubanSelenium(BaseSelenium):
    name_platform = 'Douban'
    def __init__(self, useHead=True):
        super().__init__()
        self.name_selenium = 'Douban'
        self.login_url = 'https://accounts.douban.com/passport/login'
        self.login_url = 'https://douban.com'
        self.useHead = useHead

        self.driver = None

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

        driver.delete_all_cookies()
        ## 临时使用扫码进行第1次登录解决
        driver.get(self.login_url)


        time.sleep(30)
        filename = "%s_%s" % (self.name_selenium, username)
        self.persist_cookie_info(driver, filename)

        time.sleep(30)
        driver.quit()



    def publish_article(self, article_title, article_content, flag_debug=False):
        chrome_options = self.get_chrome_options()

        driver: webdriver.Chrome = self.driver

        url_create = 'https://www.douban.com/note/create'
        driver.get(url_create)
        time.sleep(3)

        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'editor-input')))
        
        print("输入标题")
        input_title = driver.find_element(By.CLASS_NAME, 'editor-input')
        self.save_element_html(input_title, 'input_title.html')
        input_title.send_keys(article_title)
        time.sleep(2)

        print("输入内容")
        input_content = driver.find_element(By.CSS_SELECTOR, '.notranslate.public-DraftEditor-content')
        self.save_element_html(input_content, 'input_content.html')
        input_content.send_keys(article_content)
        time.sleep(2)


        btn_publish = driver.find_element(By.CLASS_NAME, 'editor-extra-button-submit')
        btn_publish.click()
        time.sleep(2)

        box_publish = driver.find_element(By.CLASS_NAME, 'editor-popup-setting-submit')
        self.save_element_html(box_publish,'box_publish.html')

        final_pub_btn = box_publish.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        self.save_element_html(final_pub_btn,'final_pub_bnt.html')
        if flag_debug:
            print("测试，不发布")
        else:
            final_pub_btn.click()

        
        self.time_wait(5, 5)
        
        
if __name__ == "__main__":
    import sys
    flag_debug = True
    if len(sys.argv)>1:
        debug = sys.argv[1]
        if debug=="1": 
            flag_debug = False
        
    obj_douban = DoubanSelenium(useHead=False)
    title = "个人笔记 - 今天怎么样"
    content ="Good Good Study, Day Day Up. 是的"
    username = '18511400319'
    # obj_douban.login_with_password(username)
    driver = obj_douban.login_with_cookie(username, wait_time=5)
    obj_douban.publish_article(title, content, flag_debug=flag_debug)
    obj_douban.quit_driver()