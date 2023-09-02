import json
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from collections import defaultdict
try:
    from .BaseSelenium import BaseSelenium
except Exception as e:
    from BaseSelenium import BaseSelenium

 
class Crawler(BaseSelenium):
    def __init__(self):
        self.logurl = 'https://baijiahao.baidu.com/'
        self.driver = None

    def get_options(self):
        chrome_options = Options()

        chrome_options.add_argument("window-size=1024,768")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.24 Safari/537.36')

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-browser-side-navigation')
        chrome_options.add_argument('enable-automation')
        chrome_options.add_argument('--disable-infobars')
        return chrome_options
   
    def login_with_password(self):
        chrome_options = self.get_chrome_options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.logurl)
        driver.maximize_window()
        time.sleep(10)
        driver.find_element(By.CSS_SELECTOR, value="[class='btnlogin--i1pF9']").click()
        driver.refresh()
        time.sleep(2)
        cookie = driver.get_cookies()
        print(cookie)
        jsonCookies = json.dumps(cookie)
        with open('data/%s.json' % (username), 'w') as f:
            print("写cookie")
            f.write(jsonCookies)
        time.sleep(10)

    def login_with_cookie(self, username = ''):

        chrome_options = self.get_chrome_options()
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 1)
    
        #登录前清楚所有cookie
        driver.delete_all_cookies()
        driver.get(self.logurl)
        time.sleep(2)
    
        f1 = open('data/%s_%s.json' % (self.name_selenium, username))
        cookie = f1.read()
        cookie = json.loads(cookie)
        for c in cookie:
            print("add :", c)
            driver.add_cookie(c)
        
        # 重新登陆
        driver.get(self.logurl)
        driver.maximize_window()
        time.sleep(3)
        self.driver = driver
        return driver
        

    def get_context(self, driver):
        # 刷新页面
        driver.refresh()
        time.sleep(2)
        driver.find_elements(By.CSS_SELECTOR, value="[class='all-btn']")[1].click()
        windows = driver.window_handles
        driver.switch_to.window(windows[1])
        time.sleep(10)
        context = defaultdict(list)
        hot_lost = driver.find_elements(By.CSS_SELECTOR, value="[class='client_pages_hotspotCenter_components_listItem']")
        for i, item_driver in enumerate(hot_lost):
            time.sleep(1)
            if i != 0 and i % 2 == 0:
                driver.execute_script("window.scrollBy(0,500)") # 一屏两条热点，后续可以考虑直接定位到元素可见的位置。
            item_driver.click()
            time.sleep(2)
            windows = driver.window_handles
            driver.switch_to.window(windows[2])
            time.sleep(1)
            # 获取热点信息
            title = driver.find_element(By.CLASS_NAME, value="client_pages_hotspotEvents_components_eventContentInfo").find_element(By.CLASS_NAME, value="content-info-title").get_attribute("innerText")
            text = driver.find_element(By.CSS_SELECTOR, value="[class='longWorldFold-content-wrap longWorldFold-font-style']").find_element(By.CLASS_NAME, value="longWorldFold-content").get_attribute("innerText")
            image = driver.find_element(By.CLASS_NAME, value="client_pages_hotspotEvents_components_eventContentInfo").find_element(By.CLASS_NAME, value="content-info-img-wrap").find_element(By.CLASS_NAME, value="content-info-img").get_attribute("src")
            status = driver.find_element(By.CLASS_NAME, value="content-info-status-wrap").find_element(By.CLASS_NAME, value="status-item").text
            date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 数据入库
            # =================== #
            # 关闭当前页面
            time.sleep(2)
            driver.close()
            driver.switch_to.window(windows[1])
            context[title] = [status, date_str, text, image]

            return context
        
    def public_article(self, article_title, article_content, author, abstract="经济的本质", context_label="财经"):
        self.driver.refresh()
        time.sleep(5)
        try:
            self.driver.find_element(By.CSS_SELECTOR, value="[class='client_pages_newHome_displayPopups_hundredfanilyhonor']").click()
        except Exception as e:
            print("没有锚框，开始发布内容")

        self.driver.find_element(By.CSS_SELECTOR, value="[class='cheetah-btn cheetah-btn-primary cheetah-public _2hCPbPjXJs5rEp0wGcWkgo publish-btn']").click()
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)") # 滑倒页面底部
        time.sleep(2)
        self.driver.execute_script("var q=document.documentElement.scrollTop=0")    # 回到页面顶部
        time.sleep(3)
        input_title = self.driver.find_element(By.CSS_SELECTOR, value="[class='cheetah-input cheetah-public _3WEh8QikwJ-aztLNNG_2Bt']")
        input_title.send_keys(article_title)
        time.sleep(3)

        self.driver.find_element(By.ID, value="edui33_state").click()
        time.sleep(3)
        img_input = self.driver.find_element(By.CSS_SELECTOR, value="[data-urlkey='news-点击-localUpload-pv/uv']")
        img_input.send_keys("F:/MyWorks/captain/imgs/R.jpg")
        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, value="[class='cheetah-btn cheetah-btn-primary cheetah-public _2hCPbPjXJs5rEp0wGcWkgo']").click()
        time.sleep(2)
        self.driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(2)


        print("切换到内部 -content")
        iframe_content = self.driver.find_element(By.ID, 'ueditor_0')
        self.driver.switch_to.frame(iframe_content)

        context_input = self.driver.find_element(By.CSS_SELECTOR, "body")
        context_input.send_keys(article_content)

        # 退出iframe
        self.driver.switch_to.default_content()

        # 页面滚动到特定元素出现：
        self.driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(3)

        # 选择单图
        self.driver.find_element(By.CSS_SELECTOR, value="[value='one']").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, value="[class='wrap-scale-DraggableTags']").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, value="[class='cheetah-ui-pro-base-image ']").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, value="[class='cheetah-btn cheetah-btn-primary cheetah-public _2hCPbPjXJs5rEp0wGcWkgo']").click()
        time.sleep(2)

        self.driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, value="[class='remove']").click()
        time.sleep(2)
        abstract_input = self.driver.find_element(By.CSS_SELECTOR, value="[class='cheetah-input cheetah-public _3WEh8QikwJ-aztLNNG_2Bt cheetah-ui-pro-countable-textbox-container-input']")
        abstract_input.send_keys(abstract)
        time.sleep(1)
        # 这里选择分类 不支持。
        # label_input = self.driver.find_element(By.CSS_SELECTOR, value="[class='cheetah-select-selection-search-input']")
        # label_input.send_keys(context_label)
        self.driver.find_element(By.CSS_SELECTOR, value="[class='cheetah-btn cheetah-btn-primary cheetah-btn-circle cheetah-btn-icon-only cheetah-public _2hCPbPjXJs5rEp0wGcWkgo always-blue']").click()
        time.sleep(2)
        try:
            # 当文档字数少于200字时，需要点弹窗。
            self.driver.find_element(By.CSS_SELECTOR, value="[class='cheetah-btn cheetah-btn-primary cheetah-public']").click()

        except Exception as e:
            pass

        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, value="[class='cheetah-btn cheetah-btn-primary cheetah-btn-circle cheetah-btn-icon-only cheetah-public _2hCPbPjXJs5rEp0wGcWkgo adapter-preview-center-70734']").click()
        print(article_content)

if __name__ == '__main__':
    ob_Crawler = Crawler()
    username = '18511400888'
    # ob_Crawler.login_with_password()
    driver = ob_Crawler.login_with_cookie(username)
    title = "房地产之后的下一个时代是什么？"
    context = "经济发展中的各个阶段通常都与特定的趋势和挑战相关。房地产过剩可能是一个阶段，但并不是所有国家都会经历完全相同的发展路径。下一个阶段将取决于多种因素，包括社会、技术和经济变化。"
    author = "麻辣烫不要辣" # article_title
    ob_Crawler.public_article(article_title=title, article_content=context, author=author)
