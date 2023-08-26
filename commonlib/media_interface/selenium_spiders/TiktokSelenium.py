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

class TiktokSelenium(BaseSelenium):
    name_platform = 'Tiktok'
    def __init__(self, useHead=True):
        super().__init__()
        self.name_selenium = 'Tiktok'
        self.login_url = 'https://www.tiktok.com/'

        self.driver = None
        self.useHead = useHead


    def login_with_password(self, username='', wait_time=50):
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


        time.sleep(wait_time)
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

    def publish_video(self, flag_debug=False):
        ## input参数
        path_video = self.path_video
        title_video  ='今天说点什么'

        url_upload = 'https://www.tiktok.com/upload?lang=zh-CN'

        ## output
        driver = self.driver
        driver : webdriver.Chrome = driver

        print("第1次刷新upload")
        driver.get(url_upload)
        time.sleep(5)

        print("第2次刷新upload")
        driver.get(url_upload)
        time.sleep(10)
        self.save_driver_html(driver, 'tiktok_upload.html')

        ## 先获取iframe元素
        iframe = driver.find_element(By.CSS_SELECTOR, "iframe")
        self.save_element_html(iframe, 'iframe_before.html')
        time.sleep(10)

        # 切换到iframe 内部 
        print("切换到内部")
        driver.switch_to.frame(iframe)

        # 等待iframe加载完成
        time.sleep(5) 
        self.save_driver_html(driver, 'iframe_innder.html')

        ## 找到上传按钮
        div_container = driver.find_element(By.CSS_SELECTOR, '.jsx-4163898440.upload-container')
        self.save_element_html(div_container, 'div_container.html')

        file_input = div_container.find_element(By.XPATH, "//input[@type='file' and @accept='video/*']")
        self.save_element_html(file_input, 'file_input.html')

        ## Upload 按钮
        file_path = path_video
        file_input.send_keys(file_path)
        print("\t 等待视频加载完毕， 30 S")
        time.sleep(30)
        self.save_driver_html(driver, 'tic_info_after.html')
        # time.sleep(120)



        ## 上传视频
        print("开始上传视频")

        
        ## 预约发布
        print("预约发布")
        div_schedule = driver.find_element(By.CSS_SELECTOR, '.jsx-3471246984.scheduled-container')
        btn_schedule = div_schedule.find_element(By.ID, 'tux-3')
        btn_schedule.click()
        time.sleep(5)

        ## 填写title
        print("修改title")
        div_title_container = driver.find_element(By.CSS_SELECTOR, '.jsx-1768246377.container')
        div_editor = div_title_container.find_element(By.CSS_SELECTOR, '.DraftEditor-editorContainer')
        # div_editor.send_keys("hhhh")
        time.sleep(5)

        
        ## 发布
        btn_submit = driver.find_element(By.CSS_SELECTOR, '.jsx-3366794632.btn-post')       
        if flag_debug:
            print("点击发布，测试模式")
            self.time_wait(30, 5)
        else:
            btn_submit.click()


        

    def publish_article(self, article_title, article_content):
        chrome_options = self.get_chrome_options()

        driver = self.driver
        print("type driver:", type(driver))
        driver : webdriver.Chrome = driver
        time.sleep(30)
        return
        
        
if __name__ == "__main__":
    import sys
    flag_debug = True
    if len(sys.argv)>1:
        debug = sys.argv[1]
        if debug=="1": 
            flag_debug = False

    tiktok_selenium = TiktokSelenium(useHead=False)
    title = "diary - how about today"
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
    tiktok_selenium.get_content_fron_dict(dic_info)
    # tiktok_selenium.login_with_password(username, wait_time=100)
    driver = tiktok_selenium.login_with_cookie(username, wait_time=10)
    # tiktok_selenium.publish_article(title, content)

    tiktok_selenium.publish_video(flag_debug=flag_debug)

    
    tiktok_selenium.quit_driver()