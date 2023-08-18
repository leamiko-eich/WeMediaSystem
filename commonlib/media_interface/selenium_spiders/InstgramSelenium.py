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


        ## 点击投稿按钮
        button_write_article = driver.find_element(By.CLASS_NAME, 'header-upload-entry__text')
        self.save_element_html(button_write_article, 'button_write_article.html')
        button_write_article.click()

        
        ## 切换到新窗口
        print("prev url:",  driver.current_url)
        self.switch_to_new_windows(driver)
        print("after url:",  driver.current_url)
        self.save_driver_html(driver, 'driver.html')


        nav_bar = driver.find_element(By.CLASS_NAME, "upload-nav")  

        # 根据链接文本内容定位到"专栏投稿"链接
        column_link = nav_bar.find_element(By.LINK_TEXT, "专栏投稿")
        column_link.click()
        time.sleep(2)

        self.save_driver_html(driver, 'driver.html')

        
        ## 寻找输入的iframe
        iframe_box = driver.find_element(By.ID, 'edit-article-box')
        self.save_element_html(iframe_box, 'iframe_box.html')
        time.sleep(2)

        ## 先获取iframe元素
        iframe = iframe_box.find_element(By.CSS_SELECTOR, "iframe")
        self.save_element_html(iframe, 'iframe_before.html')

        # 切换到iframe 内部 
        print("切换到内部")
        driver.switch_to.frame(iframe)

        # 等待iframe加载完成
        time.sleep(5) 
        self.save_driver_html(driver, 'iframe_innder.html')

        ## 输入标题
        input_title = driver.find_element(By.CSS_SELECTOR, '.ui-input-textarea.article-title')
        self.save_element_html(input_title, 'input_title.html')
        textarea = input_title.find_element(By.CSS_SELECTOR, 'textarea')
        textarea.send_keys(article_title)
        time.sleep(2)

        ## 输入内容- 获取iframe
        # iframe_content = driver.find_element(By.CSS_SELECTOR, '.notranslate.public-DraftEditor-content')
        iframe_content = driver.find_element(By.ID, 'ueditor_0')
        self.save_element_html(iframe_content, 'iframe_content_outer.html')
        # iframe_content.send_keys(content)
        # driver.execute_script("arguments[0].value = '%s'" % (article_content), iframe_content)

        print("切换到内部 -content")
        driver.switch_to.frame(iframe_content)
        time.sleep(5)
        self.save_driver_html(driver, 'iframe_content_inner.html')


        ## 寻找插入框
        body_content = driver.find_element(By.CSS_SELECTOR, "body")
        self.save_element_html(body_content, 'body_content.html')

        # body_content.clear()
        body_content.send_keys(article_content)
        time.sleep(3)


        ## 切回到ifram1
        driver.switch_to.parent_frame()  
        self.save_driver_html(driver, 'main_iframe1.html')
        time.sleep(2)

        ## 最后提交按钮
        bnt_final_submit = driver.find_element(By.CSS_SELECTOR, '.ui-btn.blue-radius')
        self.save_element_html(bnt_final_submit, 'bnt_final_submit.html')
        bnt_final_submit.click()
        time.sleep(2)

        ## 切回到主页面
        driver.switch_to.default_content()
        self.save_driver_html(driver, 'main_default.html')
        

        time.sleep(60)
        return

        time.sleep(15)

        

        # iframe_content = driver.find_element(By.CLASS_NAME, 'public-DraftStyleDefault-block public-DraftStyleDefault-ltr')


        btn_publish = driver.find_element(By.CLASS_NAME, 'editor-extra-button-submit')
        btn_publish.click()
        time.sleep(2)

        box_publish = driver.find_element(By.CLASS_NAME, 'editor-popup-setting-submit')
        self.save_element_html(box_publish,'box_publish.html')

        final_pub_btn = box_publish.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        self.save_element_html(final_pub_btn,'final_pub_bnt.html')
        final_pub_btn.click()



        

        time.sleep(30)
        return
        
        
if __name__ == "__main__":
    instgram_selenium = InstgramSelenium()
    title = "个人笔记 - 今天怎么样"
    content ="Good Good Study, Day Day Up. 是的"
    username = '18511400319'
    # instgram_selenium.login_with_password(username)
    driver = instgram_selenium.login_with_cookie(username, wait_time=30)
    # instgram_selenium.publish_article(title, content)