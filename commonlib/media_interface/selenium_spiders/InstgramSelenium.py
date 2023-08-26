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

class InstgramSelenium(BaseSelenium):
    name_platform = 'Instgram'
    def __init__(self):
        super().__init__()
        self.name_selenium = 'Instgram'
        self.login_url = 'https://www.instagram.com/'

        self.driver = None

    def output_cookies(self, cookies):
        for cookie in cookies:
            print(cookie)

    def login_with_password(self, username=''):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("window-size=1024,1124")
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


        time.sleep(50)
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


    def publish_article(self, article_title, article_content):
        chrome_options = self.get_chrome_options()

        driver = self.driver
        print("type driver:", type(driver))
        driver : webdriver.Chrome = driver

        url_publish = 'https://www.instagram.com/?hl=zh-cn'
        driver.get(url_publish)
        time.sleep(5)

        self.save_driver_html(driver, 'instgram_login.html')

        ## 点击-以后再说
        print("跳过-以后再说")
        button_next = driver.find_element(By.XPATH, "//button[text()='以后再说']")
        button_next.click()
        time.sleep(5)
        self.save_driver_html(driver, 'instgram_create_1.html')

        ## 点击创建
        print("点击创建")
        # div_new_post = driver.find_element(By.XPATH, "//div[svg[@aria-label='新帖子']]")
        # div_new_post = driver.find_element(By.XPATH, "//svg[@aria-label='新帖子']")
        div_new_post = driver.find_element(By.CSS_SELECTOR, "svg[aria-label='新帖子']")
        self.save_element_html(div_new_post, 'div_new_post.html')
        div_new_post.click()
        time.sleep(5)
        self.save_driver_html(driver, 'instgram_create_2.html')

        ## 点击上传
        div_container = driver.find_element(By.CSS_SELECTOR, '.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe')
        self.save_element_html(div_container, 'instgram_div_container.html')

        input_img_video = div_container.find_element(By.CSS_SELECTOR, 'input[class="\_ac69"]')
        self.save_element_html(input_img_video, 'instgram_input_img_video.html')
        # path_video = 'H:/6-2.MP4'
        path_video = 'H:/2.jpeg'
        input_img_video.send_keys(path_video)
        print("\t 等待视频加载完毕， 10 S")
        time.sleep(10)
        self.save_driver_html(driver, 'instgram_create_3.html')

        ## 点击继续
        print("点击-继续")
        div_dialog = driver.find_element(By.CSS_SELECTOR, '.x1ja2u2z.x1afcbsf.x1a2a7pz.x6ikm8r.x10wlt62.x71s49j.x6s0dn4.x78zum5.xdt5ytf.xl56j7k.x1n2onr6')
        self.save_element_html(div_dialog, 'instgram_div_dialog.html')

        div_continue = div_dialog.find_element(By.CSS_SELECTOR, '._ac7b._ac7d')
        self.save_element_html(div_continue, 'instgram_div_continue.html')

        div_continue_button = div_continue.find_element(By.XPATH, "//div[text()='继续']")
        self.save_element_html(div_continue_button, 'instgram_div_continue_button.html')
        div_continue_button.click()
        time.sleep(10)

        ## 编辑-继续
        print("点击-编辑-继续")
        self.save_driver_html(driver, 'instgram_create_4.html')
        div_editor = driver.find_element(By.CSS_SELECTOR, ".x1cy8zhl.x9f619.x78zum5.xl56j7k.x2lwn1j.xeuugli.x47corl")
        self.save_element_html(div_editor, 'instgram_div_editor.html')

        div_continue_button = div_editor.find_element(By.XPATH, "//div[text()='继续']")
        self.save_element_html(div_continue_button, 'instgram_div_continue_button.html')
        div_continue_button.click()
        time.sleep(10)

        ## 点击分享
        print("点击-分享")
        self.save_driver_html(driver, 'instgram_create_5.html')
        div_share = driver.find_element(By.CSS_SELECTOR, ".x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe")
        self.save_element_html(div_share, 'instgram_div_share.html')    

        

        div_title = driver.find_element(By.CSS_SELECTOR, "div[aria-label='输入说明文字...']")
        self.save_element_html(div_title, 'instgram_div_title.html')

        article_title = "test 111"
        div_title.send_keys(article_title)
        


        # div_continue_button = div_share.find_element(By.XPATH, "//div[text()='分享']")
        # self.save_element_html(div_continue_button, 'instgram_div_continue_button.html')
        # div_continue_button.click()






        

        time.sleep(120)
        return
        
        
if __name__ == "__main__":
    instgram_selenium = InstgramSelenium()
    title = "个人笔记 - 今天怎么样"
    content ="Good Good Study, Day Day Up. 是的"
    username = '18511400319'
    # instgram_selenium.login_with_password(username)
    driver = instgram_selenium.login_with_cookie(username, wait_time=1)
    instgram_selenium.publish_article(title, content)
    instgram_selenium.quit_driver()