#encoding=utf-8
try:
    from .BaseSelenium import BaseSelenium
except Exception as e:
    from BaseSelenium import BaseSelenium
import time,json
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

class DouyinSelenium(BaseSelenium):
    name_platform = 'Douyin'
    def __init__(self):
        super().__init__()
        self.name_selenium = 'Douyin'
        self.login_url = 'https://creator.douyin.com/'

        self.driver = None

    def output_cookies(self, cookies):
        for cookie in cookies:
            print(cookie)

    def login_with_password(self, username=''):
        print("111")
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


    def publish_video(self):
        path_video = 'H:/6-2.MP4'
        chrome_options = self.get_chrome_options()

        driver = self.driver
        print("type driver:", type(driver))
        driver : webdriver.Chrome = driver

        ## 打开图文发布界面
        url = 'https://creator.douyin.com/creator-micro/content/upload'

        driver.get(url)
        time.sleep(15)

        ele_box = driver.find_element(By.CLASS_NAME, 'container--1GAZf')
        self.save_element_html(ele_box)

        input_element = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        # 输入文件路径到<input>元素
        file_path = path_video
        input_element.send_keys(file_path)
        time.sleep(2)

        
        
        time.sleep(50)
        return


    def publish_article(self, article_title, article_content):
        chrome_options = self.get_chrome_options()

        driver = self.driver
        print("type driver:", type(driver))
        driver : webdriver.Chrome = driver

        ## 打开图文发布界面
        url = 'https://creator.douyin.com/creator-micro/content/upload?default-tab=3'
        driver.get(url)

        time.sleep(15)

        
        # 找到上传区域
        upload_div = driver.find_element(By.CSS_SELECTOR, "div.upload--nCmEF") 
        self.save_element_html(upload_div, 'upload_div.html')

        # 已有的 input 标签
        # input_element = upload_div.find_element(By.CLASS_NAME, "box-s0--2-vRb")
        # input_element = upload_div.find_element(By.CLASS_NAME, "info-desc--1WX-f")
        input_element = upload_div.find_element(By.CLASS_NAME, "desc--2WwkF")
        self.save_element_html(input_element,'input_element.html')

        # 将文件路径传给 input 的 value 属性
        path_image ="H:/2.jpeg"
        input_element.send_keys(path_image) 

        # 可以上传多张图片
        #input_element.send_keys("/path/to/image2.png")



        time.sleep(30)
        return 
        ## 点击投稿按钮
        button_write_article = driver.find_element(By.CLASS_NAME, 'header-upload-entry__text')
        self.save_element_html(button_write_article, 'button_write_article.html')
        button_write_article.click()

        

        
        
if __name__ == "__main__":
    douyin_selenium = DouyinSelenium()
    title = "个人笔记 - 今天怎么样"
    content ="Good Good Study, Day Day Up. 是的"
    username = '18511400319'
    # douyin_selenium.login_with_password(username)
    driver = douyin_selenium.login_with_cookie(username, wait_time=10)
    douyin_selenium.publish_article(title, content)