#encoding=utf-8
from BaseSelenium import BaseSelenium
import time
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# class ZhihuSelenium(BaseSelenium):
class ZhihuSelenium(object):
    def __init__(self):
        # super().__init__()
        pass

    def use_firefox(self):

        # options.headless = True

        options = Options()
        # options.set_preference('profile', r'H:\3opi7avg.default-release')
        options.set_preference('profile',  r'C:\Users\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\3opi7avg.default-release')

        driver = webdriver.Firefox(options=options)

        # profile = FirefoxProfile(r'C:\path\to\my_profile')
        # driver = webdriver.Firefox(options=options, firefox_profile=profile) 
        driver.get("https://www.zhihu.com")

        time.sleep(60)
        driver.quit()

    def output_cookies(self, cookies):
        for cookie in cookies:
            print(cookie)

    def get_cookies(self):
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\google\\Chrome\\User Data\\Profile 1")

        driver = webdriver.Chrome(options=options)
        driver.get("https://www.zhihu.com")

        browser = driver

        cookieBefore = browser.get_cookies()
        self.output_cookies(cookieBefore)

        browser.delete_all_cookies()

        print("\n\n aafter")
        newCookie = browser.get_cookies()
        self.output_cookies(newCookie)

        print("等待登录 10s")
        time.sleep(10)

        print("\n\n 登录后")
        newCookie = browser.get_cookies()
        self.output_cookies(newCookie)


        time.sleep(30)
        driver.quit()


    def publish_article(self, article_title, article_content):

        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\google\\Chrome\\User Data\\Profile 1")

        driver = webdriver.Chrome(options=options)
        driver.get("https://www.zhihu.com")

        time.sleep(30)
        return
        # Click the "写文章" button
        write_article_button = self.driver.find_element_by_xpath("//button[@class='Button WriteIndex-articleButton Button--primary Button--blue']")
        write_article_button.click()
        
        # Input the article title
        title_input = self.driver.find_element_by_xpath("//input[@class='Input WriteIndex-titleInput']")
        title_input.send_keys(article_title)
        
        # Input the article content
        content_input = self.driver.find_element_by_xpath("//div[@class='public-DraftEditor-content']")
        content_input.send_keys(article_content)
        
        # Click the "发布" button
        publish_button = self.driver.find_element_by_xpath("//button[@class='Button PublishPanel-submitButton Button--primary Button--blue']")
        publish_button.click( )
        
        
if __name__ == "__main__":
    obj_zhihu_selenium = ZhihuSelenium()
    title = "1111"
    content ="2222"
    # obj_zhihu_selenium.publish_article(title, content)
    # obj_zhihu_selenium.use_firefox()
    obj_zhihu_selenium.get_cookies()