#encoding=utf-8
try:
    from BaseSelenium import BaseSelenium
except Exception as e:
    from .BaseSelenium import BaseSelenium
import time,json
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ZhihuSelenium(BaseSelenium):
    name_platform = 'Zhihu'
    def __init__(self, useHead=True):
        super().__init__()
        self.name_selenium = 'Zhihu'
        self.login_url = 'https://www.zhihu.com'
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
        driver.get("https://www.zhihu.com")

        # driver.delete_all_cookies()

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

    # def login_with_cookie(self, username = ''):
    #
    #     chrome_options = self.get_chrome_options()
    #
    #     driver = webdriver.Chrome(options=chrome_options)
    #
    #     time.sleep(2)
    #     logurl = self.login_url
    #
    #     #登录前清楚所有cookie
    #     driver.delete_all_cookies()
    #     driver.get(logurl)
    #     time.sleep(2)
    #
    #     filename = "%s_%s" % (self.name_selenium, username)
    #     f1 = open('data/%s.json' % (filename))
    #     cookie = f1.read()
    #     cookie = json.loads(cookie)
    #     for c in cookie:
    #         driver.add_cookie(c)
    #     # # 刷新页面
    #     time.sleep(2)
    #     driver.refresh()
    #     time.sleep(2)
    #
    #     self.driver = driver

 


    def publish_article(self, article_title, article_content, flag_debug=False):

        driver: webdriver.Chrome = self.get_driver()
        self.login_url = 'https://zhuanlan.zhihu.com/write'
        driver.get(self.login_url)
        time.sleep(3)

        # button_write_article = driver.find_element(By.CSS_SELECTOR, 'button[title="写文章"]')
        # # self.save_element_html(button_write_article, 'button_write_article.html')
        # button_write_article.click()
        #
        # self.switch_to_new_windows(driver)

        
        input_title = driver.find_element(By.CLASS_NAME, 'Input')
        # self.save_element_html(input_title, 'input_title.html')
        input_title.send_keys(article_title)
        time.sleep(2)

        # input_content = driver.find_element(By.CLASS_NAME, 'public-DraftStyleDefault-block public-DraftStyleDefault-ltr')
        input_content = driver.find_element(By.CSS_SELECTOR, '.public-DraftStyleDefault-block.public-DraftStyleDefault-ltr')
        # self.save_element_html(input_content, 'input_content.html')
        input_content.send_keys(article_content)
        time.sleep(2)

        self.scroll_to_bottom(driver)

        # btn_add_topic = driver.find_element(By.CLASS_NAME, '.css-f7rzgf')
        # self.save_element_html(btn_add_topic, 'btn_add_topic.html')
        # btn_add_topic.click()
        # time.sleep(2)
# 
        # input_topic = driver.find_element(By.CSS_SELECTOR, '.css-nvm401.Input-wrapper.QZcfWkCJoarhIYxlM_sG')
        # self.save_element_html(input_topic, 'input_topic.html')
        # input_topic.send_keys('日记')
        # time.sleep(2)

        btn_publish = driver.find_element(By.CSS_SELECTOR, '.Button.css-d0uhtl.Button--primary.Button--blue')
        if flag_debug:
            print("测试环节，不发布")
        else:
            btn_publish.click()

    def publish_video(self, article_title, article_content, field = '娱乐',flag_debug=False):
        chrome_options = self.get_chrome_options()

        driver: webdriver.Chrome = self.get_driver()
        self.login_url = 'https://www.zhihu.com/zvideo/upload-video'
        driver.get(self.login_url)
        time.sleep(3)

        file_path = "C:/Users/chongqingwei/Desktop/test.mp4"  # 本地文件的路径
        file_input = driver.find_element(By.CSS_SELECTOR,'input[type="file"]')

        # Set the local file path for the input element
        file_input.send_keys(file_path)

        time.sleep(10)

        # input_content = driver.find_element(By.CLASS_NAME, 'public-DraftStyleDefault-block public-DraftStyleDefault-ltr')
        input_title = driver.find_element(By.XPATH,"//input[@placeholder='输入视频标题']")
        input_title.clear()
        # self.save_element_html(input_content, 'input_content.html')
        input_title.send_keys(article_title)
        time.sleep(2)

        # Find the video description input field by its placeholder attribute
        description_input = driver.find_element(By.XPATH,"//textarea[@placeholder='填写视频简介，让更多人找到你的视频']")

        # Clear the existing content in the description input field
        description_input.clear()
        description_input.send_keys(article_content)

        dropdown_button = driver.find_element(By.XPATH, "//button[contains(text(),'选择领域')]")

        # Click the dropdown button to open the options
        dropdown_button.click()
        field = "娱乐"
        option_xpath = f"//button[contains(text(), '{field}')]"
        option_element = driver.find_element(By.XPATH, option_xpath)
        option_element.click()

        self.scroll_to_bottom(driver)
        # Find the "绑定话题" button and click it
        bind_topic_button = driver.find_element(By.XPATH, "//button[contains(text(), '绑定话题')]")
        bind_topic_button.click()
        wait = WebDriverWait(driver, 5)

        # Input '娱乐' into the search field
        bind_topic_button.send_keys('娱乐')
        # Wait for the relevant topics to appear in the dropdown
        relevant_topics_xpath = "//div[@class='RelevantTopics']//div[contains(@class, 'TopicItem')]"
        wait.until(EC.visibility_of_all_elements_located((By.XPATH, relevant_topics_xpath)))

        # Select the first relevant topic (you can change the index as needed)
        relevant_topics = driver.find_elements(By.XPATH, relevant_topics_xpath)
        if len(relevant_topics) > 0:
            relevant_topics[0].click()

        # btn_add_topic = driver.find_element(By.CLASS_NAME, '.css-f7rzgf')
        # self.save_element_html(btn_add_topic, 'btn_add_topic.html')
        # btn_add_topic.click()
        # time.sleep(2)
        #
        # input_topic = driver.find_element(By.CSS_SELECTOR, '.css-nvm401.Input-wrapper.QZcfWkCJoarhIYxlM_sG')
        # self.save_element_html(input_topic, 'input_topic.html')
        # input_topic.send_keys('日记')
        # time.sleep(2)

        btn_publish = driver.find_element(By.CSS_SELECTOR, '.Button.css-d0uhtl.Button--primary.Button--blue')
        if flag_debug:
            print("测试环节，不发布")
        else:
            btn_publish.click()

    time.sleep(30)

    def crawl_by_author_link(self, url=None):
        assert(url is not None)
        # 发送GET请求
        response = requests.get(url)
        # print("response:", response)

        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(response.text, "html.parser")

        # 查找所有文章链接
        articles = soup.find_all("h2", class_="ContentItem-title")

        list_url_info = []

        for article in articles:

            title = article.get_text()
            raw_url = article.span.a['href']
            url = "http:%s"%(raw_url)

            dic_ret = {
                "title"  : title,   
                "original_link": url ,
                "post_date": ""
            }
            list_url_info.append(dic_ret)

        return list_url_info

        


    def parse_specific_article(self, url):
        dic_ret = {}
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        self.save_soup_html(soup, 'soup.html')

        
        ele_content =  soup.select_one("div.RichText.ztext.Post-RichText.css-1g0fqss")
        self.save_soup_html(ele_content, 'content.html')

        txt_content = self.get_texts_from_bs4(ele_content)
        txt_content = "\n".join(txt_content)

        div_time = soup.find_all("div", class_="ContentItem-time")
        post_date=None
        for div in div_time:
            text_time = div.get_text()
            text_time = text_time.split(" ")[1]
            post_date = text_time

        dic_ret ={
            "post_date" : post_date,
            "content": txt_content
        }
        return dic_ret
        
        
if __name__ == "__main__":
    obj_zhihu_selenium = ZhihuSelenium(useHead=True)
    title = "个人笔记 - 今天怎么样"
    content ="Good Good Study, Day Day Up. 是的"
    username = '251132021@qq.com'
    # obj_zhihu_selenium.login_with_password(username)
    obj_zhihu_selenium.login_with_cookie(username)
    # obj_zhihu_selenium.publish_article(title, content, flag_debug=True)
    obj_zhihu_selenium.publish_video(title, content, flag_debug=True)
    # obj_zhihu_selenium.quit_driver()
    #
    # url = "https://www.zhihu.com/people/jiafeimao/posts"
    #link_art_url = obj_zhihu_selenium.crawl_by_author_link(url)

    # art_url  ="http://zhuanlan.zhihu.com/p/574523304"
    #dic_ret = obj_zhihu_selenium.parse_specific_article(art_url)
    #print(dic_ret)

    # for dic_url  in link_art_url:
        # original_link = dic_url['original_link']
        # dic_ret = obj_zhihu_selenium.parse_specific_article(original_link)
        # print(dic_ret)