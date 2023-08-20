#encoding=utf-8
from BaseSelenium import BaseSelenium
import time,json
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

class QiehaoSelenium(BaseSelenium):
    name_platform = 'Qiehao'
    def __init__(self):
        super().__init__()
        self.name_selenium = 'Qiehao'
        self.login_url = 'https://om.qq.com/'

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

        ## 临时使用扫码进行第1次登录解决
        driver.get(self.login_url)

        # driver.delete_all_cookies()

        time.sleep(30)
        filename = "%s_%s" % (self.name_selenium, username)
        self.persist_cookie_info(driver, filename)

        time.sleep(60)
        driver.quit()

    def get_chrome_options(self):
        chrome_options = Options()
    
        chrome_options.add_argument("window-size=1024,768")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')
   
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument('start-maximized')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-browser-side-navigation')
        chrome_options.add_argument('enable-automation')
        chrome_options.add_argument('--disable-infobars')
        return chrome_options


 


    def publish_article(self, article_title, article_content):
        chrome_options = self.get_chrome_options()

        driver = self.driver


        button_write_article = driver.find_element(By.CSS_SELECTOR, 'button[title="写文章"]')
        self.save_element_html(button_write_article, 'button_write_article.html')
        button_write_article.click()

        self.switch_to_new_windows(driver)

        
        input_title = driver.find_element(By.CLASS_NAME, 'Input')
        self.save_element_html(input_title, 'input_title.html')
        input_title.send_keys(article_title)
        time.sleep(2)

        # input_content = driver.find_element(By.CLASS_NAME, 'public-DraftStyleDefault-block public-DraftStyleDefault-ltr')
        input_content = driver.find_element(By.CSS_SELECTOR, '.public-DraftStyleDefault-block.public-DraftStyleDefault-ltr')
        self.save_element_html(input_content, 'input_content.html')
        input_content.send_keys(article_content)
        time.sleep(2)

        self.scroll_to_bottom(driver)

        # btn_add_topic = driver.find_element(By.CLASS_NAME, '.css-f7rzgf')
        # self.save_element_html(btn_add_topic, 'btn_add_topic.html')
        # btn_add_topic.click()
        # time.sleep(2)
# 
        # input_topic = driver.find_element(By.CSS_SELECTOR, '.css-nvm401.Input-wrapper.QZcfWkCJoarhIYxlM_sG')
        # self.save_element_html(input_topic, 'input_topic.html')
        # input_topic.send_keys('日记')
        # time.sleep(2)

        btn_publish = driver.find_element(By.CSS_SELECTOR, '.Button.css-d0uhtl.Button--primary.Button--blue')
        btn_publish.click()



        

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
    obj_qiehao_selenium = QiehaoSelenium()
    title = "个人笔记 - 今天怎么样"
    content ="Good Good Study, Day Day Up. 是的"
    username = '251132021'
    # obj_qiehao_selenium.login_with_password(username)
    obj_qiehao_selenium.login_with_cookie(username, wait_time=360)
    # obj_qiehao_selenium.publish_article(title, content)

    
    obj_qiehao_selenium.quit_driver()