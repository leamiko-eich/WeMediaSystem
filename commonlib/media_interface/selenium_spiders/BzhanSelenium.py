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

class BzhanSelenium(BaseSelenium):
    name_platform = 'Bzhan'
    def __init__(self, useHead=True):
        super().__init__()
        self.name_selenium = 'Bzhan'
        self.login_url = 'https://accounts.douban.com/passport/login'
        self.login_url = 'https://www.bilibili.com/'

        self.driver = None
        self.useHead = useHead

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


    def publish_article(self, article_title, article_content, flag_debug=True):

        driver = self.driver
        print("type driver:", type(driver))
        driver : webdriver.Chrome = driver

        print("进入文章专栏界面")
        url_publish_article = 'https://member.bilibili.com/platform/upload/text/edit'
        driver.get(url_publish_article)
        time.sleep(5)

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
        if flag_debug:
            print("debug模式，不提交")
        else:
            bnt_final_submit.click()
        time.sleep(2)

        ## 切回到主页面
        driver.switch_to.default_content()
        self.save_driver_html(driver, 'main_default.html')
        

        
        
if __name__ == "__main__":
    import sys
    flag_debug = True
    if len(sys.argv)>1:
        debug = sys.argv[1]
        if debug=="1": 
            flag_debug = False

    # bzhan_selenium = BzhanSelenium(useHead=False)
    bzhan_selenium = BzhanSelenium(useHead=True)
    title = "个人笔记 - 今天怎么样"
    content ="Good Good Study, Day Day Up. 是的"
    username = '18511400319'
    dic_info = {
        "c_title": title,
        "c_content": content,
        "path_win_video" : 'H:/3.mp4',
        "path_linux_video" : '/home/jeff/code/WeMediaSystem/commonlib/media_interface/selenium_spiders/images/3.mp4',
        "path_win_image" : 'H:/2.jpeg',
        "path_linux_image" : '/home/jeff/code/WeMediaSystem/commonlib/media_interface/selenium_spiders/images/2.jpeg'
    }
    bzhan_selenium.get_content_fron_dict(dic_info)
    # bzhan_selenium.login_with_password(username)
    driver = bzhan_selenium.login_with_cookie(username)
    bzhan_selenium.publish_article(title, content, flag_debug=flag_debug)
    bzhan_selenium.quit_driver()