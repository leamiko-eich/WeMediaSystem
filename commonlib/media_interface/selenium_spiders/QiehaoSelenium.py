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
    def __init__(self, useHead=True):
        super().__init__()
        self.name_selenium = 'Qiehao'
        self.login_url = 'https://om.qq.com/'
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

        ## 临时使用扫码进行第1次登录解决
        driver.get(self.login_url)

        # driver.delete_all_cookies()

        time.sleep(60)
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

    def publish_article(self, title, content):
        driver: webdriver.Chrome = self.get_driver()
        self.login_url = 'https://om.qq.com/main/creation/article'
        driver.get(self.login_url)
        time.sleep(3)

        # 这部分等江峰解决，如何虚拟点击发布文章按钮。

        # 找到输入框元素
        input_title = driver.find_element(By.CSS_SELECTOR, '.omui-inputautogrowing__inner')
        input_title.clear()
        input_title.send_keys(title)
        time.sleep(2)

        # 输入正文内容
        # 使用 driver.find_element 查找文章正文内容的可编辑元素
        content_element = driver.find_element(By.CSS_SELECTOR, '.ProseMirror.ExEditor-basic')
        # 输入文章正文内容 清除内容
        content_element.clear()
        content_element.send_keys(content)

        driver.execute_script("window.scrollBy(0, 500);")  # 500为滚动的像素值
        # '是否单标题'
        single_title_input = driver.find_element(By.CSS_SELECTOR, 'label.omui-radio')
        single_title_input.click()
        time.sleep(4)
        if not self.useHead:
            print('测试不发布')
            time.sleep(2)
            driver.quit()

        # 添加封面图片
        img_elements = driver.find_elements(By.TAG_NAME, "img")
        if not img_elements:

            svg_element = driver.find_element(By.CSS_SELECTOR, 'i.omui-icon.omui-icon-plus')
            svg_element.click()
            time.sleep(4)
            #找到本地上传按钮
            local_upload_button = driver.find_element(By.XPATH, "//li[@class='omui-tab__label' and text()='本地上传']")
            local_upload_button.click()
            time.sleep(4)
            #点击上传图片的十字按钮
            upload_button = driver.find_element(By.XPATH, '//div[@class="omui-upload-image-trigger"]')
            # 点击上传按钮
            upload_button.click()
            time.sleep(4)

            # 输入文件路径到<input>元素
            input_element = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
            file_path = "C:/Users/chongqingwei/Desktop/1.jpg"  # 本地文件的路径
            input_element.send_keys(file_path)
            # 在上传文件后，按下ESC键以关闭文件选择窗口
            time.sleep(2)
            # 在上传文件后，按下ESC键以关闭文件选择窗口
            input_element.send_keys(Keys.ESCAPE)

            # pyautogui.press('esc')

            # 查找包含“确认”的按钮元素
            confirm_button = driver.find_element_by_xpath('//button[contains(text(), "确认")]')

            # 点击按钮
            confirm_button.click()
            # 上传完以后点击确定按钮
        else:
            pass

        # 使用Selenium的定位方法找到'发布'按钮
        publish_button = driver.find_element(By.XPATH,"//button[contains(@class, 'omui-button--primary') and .//span[text()='发布']]")

        # 点击按钮
        publish_button.click()


        time.sleep(2)

        driver.quit()

        
if __name__ == "__main__":
    obj_qiehao_selenium = QiehaoSelenium(useHead=False)
    title = "个人笔记 - 今天怎么样"
    content ="Good Good Study, Day Day Up. 是的"
    username = '251132021'
    # obj_qiehao_selenium.login_with_password(username)
    obj_qiehao_selenium.login_with_cookie(username, wait_time=5)
    obj_qiehao_selenium.publish_article(title, content)

    
    obj_qiehao_selenium.quit_driver()