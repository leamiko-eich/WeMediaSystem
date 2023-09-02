#encoding=utf-8
try:
    from .BaseSelenium import BaseSelenium
except Exception as e:
    from BaseSelenium import BaseSelenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, json

class PinterestSelenium(BaseSelenium):
    name_platform = 'Pinterest'
    def __init__(self, useHead=True):
        super().__init__()
        self.name_selenium = 'Pinterest'
        # self.login_url = 'https://www.Pinterest.com'
        self.login_url = 'https://www.pinterest.com/'
        self.useHead = useHead

    def login_with_password(self, username=''):
        print("username: %s" % (username))
        url = self.login_url
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("window-size=1024,768")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')
#    
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-browser-side-navigation')
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # chrome_options.add_argument('enable-automation')
        driver = webdriver.Chrome(options=chrome_options)
        # driver = webdriver.Firefox(options=chrome_options)

        # options = Options()
        # options.set_preference('profile',  r'C:\Users\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\3opi7avg.default-release')

        # driver = webdriver.Firefox(options=options)


        driver.get(url)
        print(" 登录")
        time.sleep(30)

        print(" out cookie")
        filename = "%s_%s" % (self.name_selenium, username)
        self.persist_cookie_info(driver, filename)
        print(" cooie over")

        time.sleep(50)
        driver.quit()

    def publish_article(self, title, content):
        driver: webdriver.Chrome = self.get_driver()
        self.login_url = 'https://www.pinterest.com/idea-pin-builder/'
        driver.get(self.login_url)
        time.sleep(3)

        # 找到"新建"按钮并点击它
        new_button = driver.find_element(By.XPATH,'//div[text()="新建"]')
        new_button.click()
        time.sleep(3)

        # 输入文件路径到<input>元素
        input_element = driver.find_element(By.ID, 'storyboard-upload-input')

        file_path = "C:/Users/chongqingwei/Desktop/1.jpg"  # 本地文件的路径
        if not self.useHead:
            file_path = "/home/lengxiao/WeMediaSystem/commonlib/media_interface/selenium_spiders/images/2.jpeg"  # 本地文件的路径
        input_element.send_keys(file_path)
        time.sleep(2)

        # 输入标题
        input_title = driver.find_element(By.ID, 'storyboard-selector-title')
        input_title.clear()
        input_title.send_keys(title)
        time.sleep(2)
        # driver.execute_script("window.scrollBy(0, 150);")  # 500为滚动的像素值
        # 输入正文内容
        content_field = driver.find_element(By.CSS_SELECTOR, '.DraftEditor-editorContainer [contenteditable="true"]')
        content_field.click()
        # 模拟按键输入
        content_field.send_keys(Keys.CONTROL + "a")  # 选择所有文本
        content_field.send_keys(Keys.DELETE)  # 删除选中的文本
        content_field.send_keys(content)  # 输入你的内容
        time.sleep(4)
        if not self.useHead:
            print('测试不发布')
            time.sleep(2)
            driver.quit()
            return
        # Click the "发布" button
        publish_button = driver.find_element(By.XPATH,'//div[text()="发布"]')
        publish_button.click()

        time.sleep(2)
        driver.quit()



    

if __name__ == "__main__":
    obj_Pinterest = PinterestSelenium(useHead=False)
    title = "个人笔记 - 今天怎么样"
    content ="Good Good Study, Day Day Up. 是的"
    username = 'chongqingwei1@outlook.com'
    # obj_Pinterest.login_with_password(username)
    obj_Pinterest.login_with_cookie(username, wait_time=3)
    obj_Pinterest.publish_article(title, content)
