#encoding=utf-8
try:
    from .BaseSelenium import BaseSelenium
except Exception as e:
    from BaseSelenium import BaseSelenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time, json

class XiaohongshuSelenium(BaseSelenium):
    name_platform = 'Xiaohongshu'
    def __init__(self):
        super().__init__()
        self.name_selenium = 'Xiaohongshu'
        # self.login_url = 'https://www.xiaohongshu.com'
        self.login_url = 'https://creator.xiaohongshu.com'

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
        self.login_url = 'https://mp.toutiao.com/profile_v4/graphic/publish?from=toutiao_pc'
        driver.get(self.login_url)
        time.sleep(3)

        # 这部分等江峰解决，如何虚拟点击发布文章按钮。

        input_title = driver.find_element(By.CSS_SELECTOR, 'div.publish-editor-title-inner textarea')
        input_title.send_keys(title)
        time.sleep(2)

        # 输入正文内容
        div_element = driver.find_element(By.CSS_SELECTOR, 'div.ProseMirror')
        div_element.send_keys(content)
        time.sleep(4)
        driver.execute_script("window.scrollBy(0, 500);")  # 500为滚动的像素值
        # '是否单标题'
        single_title_input = driver.find_element(By.CSS_SELECTOR, 'div.byte-radio-inner ')
        single_title_input.click()
        time.sleep(4)

        # 添加封面图片
        svg_element = driver.find_element(By.CSS_SELECTOR, 'svg.add-icon.byte-icon.byte-icon-plus')
        svg_element.click()
        time.sleep(4)

        input_element = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        # 输入文件路径到<input>元素
        file_path = "C:/Users/chongqingwei/Desktop/1.jpg"  # 本地文件的路径
        input_element.send_keys(file_path)
        time.sleep(2)
        # 上传完以后点击确定按钮
        button_element = driver.find_element(By.CSS_SELECTOR, 'button[data-e2e="imageUploadConfirm-btn"]')
        button_element.click()
        time.sleep(2)

        # 定位到预览并发布按钮的元素
        preview_publish_button = driver.find_element(By.XPATH, '//button[contains(span, "预览并发布")]')

        preview_publish_button.click()
        time.sleep(2)
        # 定位到确认发布按钮的元素
        confirm_publish_button = driver.find_element(By.XPATH, '//button[contains(span, "确认发布")]')
        # 点击确认发布按钮
        confirm_publish_button.click()
        time.sleep(2)
        driver.quit()



    

if __name__ == "__main__":
    obj_xiaohongshu = XiaohongshuSelenium()
    title = "个人笔记 - 今天怎么样"
    content ="Good Good Study, Day Day Up. 是的"
    username = '18710090164'
    # obj_xiaohongshu.login_with_password('18710090164')
    obj_xiaohongshu.login_with_cookie(username, wait_time=3)
    obj_xiaohongshu.publish_article(title, content)
