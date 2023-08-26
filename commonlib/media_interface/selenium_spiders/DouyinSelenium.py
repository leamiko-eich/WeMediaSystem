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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DouyinSelenium(BaseSelenium):
    name_platform = 'Douyin'
    def __init__(self, useHead=True):
        super().__init__()
        self.name_selenium = 'Douyin'
        self.login_url = 'https://creator.douyin.com/'

        self.driver = None
        self.useHead = useHead

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



    def publish_video(self, flag_debug=True):
        ## 输入参数
        path_video = self.path_video
        title_video  ='今天说点什么'


        driver = self.driver
        print("type driver:", type(driver))
        driver : webdriver.Chrome = driver

        ## 打开视频发布界面
        print("打开视频发布界面, 加载时间长")
        url = 'https://creator.douyin.com/creator-micro/content/upload'
        driver.get(url)

        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "container--1GAZf")))
        # time.sleep(15)

        ## 寻找视频输入窗口
        print("输入视频")
        ele_box = driver.find_element(By.CLASS_NAME, 'container--1GAZf')
        self.save_element_html(ele_box)
        input_element = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        # 输入文件路径到<input>元素
        file_path = path_video
        input_element.send_keys(file_path)
        print("\t 等待视频加载完毕， 20 S")
        time.sleep(20)

        ## 视频标题
        ele_title = driver.find_element(By.CSS_SELECTOR, '.zone-container.editor-kit-container.editor.editor-comp-publish.notranslate.chrome')
        self.save_element_html(ele_title, 'ele_tilte.html')
        ele_title.send_keys(title_video)
        time.sleep(2)

        self.scroll_to_bottom(driver)

        
        ## 选择定时发布
        ele_dingshi_div = driver.find_element(By.CLASS_NAME, "container--2urnP")
        check_dingshi =  ele_dingshi_div.find_element(By.CSS_SELECTOR, ".radio--4Gpx6.one-line--2rHu9")
        check_dingshi.click()
        time.sleep(2)


        
        ## 发布按钮 
        publish_btn = driver.find_element(By.XPATH, '//button[text()="发布"]')
        self.save_element_html(publish_btn, 'publish_bnt.html')
        if flag_debug:
            print("调试模式，不发布")
            self.time_wait(50, 5)
        else:
            publish_btn.click()
        


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

        

        
        
if __name__ == "__main__":
    import sys
    flag_debug = True
    if len(sys.argv)>1:
        debug = sys.argv[1]
        if debug=="1": 
            flag_debug = False

    douyin_selenium = DouyinSelenium(useHead=False)
    # douyin_selenium = DouyinSelenium(useHead=True)
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
    douyin_selenium.get_content_fron_dict(dic_info)
    # douyin_selenium.login_with_password(username)
    driver = douyin_selenium.login_with_cookie(username, wait_time=10)
    # douyin_selenium.publish_article(title, content)
    douyin_selenium.publish_video(flag_debug=flag_debug)
    douyin_selenium.quit_driver()