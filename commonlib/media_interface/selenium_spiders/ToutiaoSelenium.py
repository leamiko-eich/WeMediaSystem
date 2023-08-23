import json
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from BaseSelenium import BaseSelenium
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC


class Crawler(BaseSelenium):
    def __init__(self):
        super().__init__()
        self.name_selenium = 'ToutiaoPublic'
        self.login_url = 'https://www.toutiao.com/'
        # pass

    def save_element_html(self, element, file_name="1.html"):
        file_name = "data/%s" % file_name
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(element.get_attribute("outerHTML"))

    def login_with_password(self, username=''):
        assert (username in self.dict_user_pass)
        password = self.dict_user_pass[username]
        print("username: %s, password: %s" % (username, password))
        chrome_options = Options()
        chrome_options.add_argument("window-size=1024,768")
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-browser-side-navigation')
        chrome_options.add_argument('enable-automation')
        chrome_options.add_argument('--disable-infobars')

        # driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='C:\devtool\Anaconda\Scripts\chromedriver')
        # driver = webdriver.Chrome(chrome_options=chrome_options)
        driver = webdriver.Chrome(options=chrome_options)

        # options = webdriver.ChromeOptions()
        # options.add_argument("user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\google\\Chrome\\User Data\\Profile 1")

        wait = WebDriverWait(driver, 1)
        ##登录头条
        login_url = self.login_url
        # 登录前清楚所有cookie
        driver.delete_all_cookies()
        driver.get(login_url)
        ##登录前打印cookie
        print(driver.get_cookies())

        ##点击登录按钮
        # driver.find_element_by_xpath('//*[@id="userbar-login"]').click()
        time.sleep(2)
        login_button = driver.find_elements(By.CLASS_NAME, "login-button")
        login_button[1].click()
        print('登录点击按钮成功')
        # driver.find_element_by_id("userbar-login").click()
        time.sleep(2)
        ##首次尝试的 默认进入扫码登录的界面
        try:
            #   footerULoginBtn = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__footerULoginBtn"]')
            footerULoginBtn = driver.find_elements(By.CLASS_NAME, "web-login-other-login-method__list__item")
            footerULoginBtn[3].click()  # 切换到用户名和密码登录
            footerULoginBtn_not_exist = False
            print("切换到用户名和密码登录")
        except:
            print("Error 账户密码登录按钮不存在")
            footerULoginBtn_not_exist = True

        ## 用户名跟密码的设置并点击提交
        user = driver.find_element(By.CLASS_NAME, "web-login-normal-input__input")
        user.clear()
        pwd = driver.find_element(By.CLASS_NAME, "web-login-button-input__input")
        pwd.clear()
        submit = driver.find_element(By.CLASS_NAME, "web-login-button")
        is_submit_agree = driver.find_element(By.CLASS_NAME, "web-login-confirm-info__checkbox")

        user.send_keys(username)
        time.sleep(3)
        pwd.send_keys(password)
        time.sleep(3)
        is_submit_agree.click()
        time.sleep(3)
        submit.click()
        print("等待拖动-发送验证码")
        time.sleep(30)

        if 3 > 10:
            ## 发送手机验证码 验证
            ##点击发送按钮
            ###是否需要输入手机验证码
            driver.find_element(By.ID, "TANGRAM__45__button_send_mobile").click()
            time.sleep(10)
            ##使用shell交互式,接受验证码
            message = input("Tell me the captcha: ")
            message = message.strip("\n").strip(" ")
            print("message:", message)
            message = "123"
            ##输入验证码
            captcha = driver.find_element(By.ID, "TANGRAM__45__input_label_vcode")
            print("captcha:", captcha)
            self.save_element_html(captcha, "captcha.html")
            time.sleep(1)
            print("手动输入验证码")
            # captcha.send_keys(message)
            time.sleep(15)
            ##点击提交
            driver.find_element(By.ID, "TANGRAM__45__button_submit").click()
            time.sleep(3)
            # except Exception as e:
            #   print("输入手机号错误", e)
            #   time.sleep(1)

        ### 获取cookie
        cookie = driver.get_cookies()
        print(cookie)
        jsonCookies = json.dumps(cookie)
        with open('data/%s.json' % (username), 'w') as f:
            print("写cookie")
            f.write(jsonCookies)
        time.sleep(30)
        driver.quit()
        return

    # def login_with_cookie(self, username = ''):
    #     # assert (username in self.dict_user_pass)
    #     chrome_options = Options()
    #
    #     chrome_options.add_argument("window-size=1024,768")
    #     chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')
    #
    #     chrome_options.add_argument('--no-sandbox')
    #     chrome_options.add_argument('--disable-dev-shm-usage')
    #     chrome_options.add_argument('start-maximized')
    #     chrome_options.add_argument("--disable-extensions")
    #     chrome_options.add_argument('--disable-browser-side-navigation')
    #     chrome_options.add_argument('enable-automation')
    #     chrome_options.add_argument('--disable-infobars')
    #
    #     driver = webdriver.Chrome(options=chrome_options)
    #
    #     wait = WebDriverWait(driver, 1)
    #
    #     ##登录百度知道
    #     logurl = 'https://www.toutiao.com/'
    #
    #     #登录前清楚所有cookie
    #     driver.delete_all_cookies()
    #     driver.get(logurl)
    #     time.sleep(2)
    #
    #     f1 = open('data/%s.json' % (username))
    #     cookie = f1.read()
    #     cookie = json.loads(cookie)
    #     for c in cookie:
    #         print("add :", c)
    #         driver.add_cookie(c)
    #     # # 刷新页面
    #     time.sleep(2)
    #     driver.refresh()
    #
    #     time.sleep(50)
    def search(self, url):
        logurl = url
        driver: webdriver.Chrome = self.get_driver()
        driver.get(logurl)
        time.sleep(3)
        # 使用 class 名称定位多个元素
        class_name = "title"

        # 查找并获取所有符合条件的元素
        elements = driver.find_elements(By.CLASS_NAME, class_name)
        article_links = []
        for element in elements:
            href_link = element.get_attribute("href")
            if 'article' in href_link:
                article_links.append(href_link)
        author_articles = []
        # 遍历每个元素的链接并访问
        for article_link in article_links[:1]:
            try:
                # 点击文章链接
                driver.get(article_link)
                # 切换到新打开的窗口（如果有的话）
                driver.switch_to.window(driver.window_handles[-1])
                # 等待页面加载完成（可以根据需要调整等待时间）
                driver.implicitly_wait(10)
                article_context = {}
                # link_element = driver.find_elements(By.CLASS_NAME, class_name)[index]  # 重新查找元素
                article_context['article_url'] = href_link

                # 获取文章内容
                title = driver.find_element(By.XPATH, '//h1').text
                publish_time = driver.find_element(By.CSS_SELECTOR, '.article-meta span:nth-child(2)').text
                author = driver.find_element(By.CSS_SELECTOR, '.article-meta a').text
                content_elements = driver.find_elements(By.CSS_SELECTOR, '.tt-article-content p')

                # 提取文章内容文本
                content = '\n'.join(element.text for element in content_elements)

                # 打印获取的信息
                print('标题:', title)
                print('发表时间:', publish_time)
                print('作者:', author)
                print('内容:', content)
                article_context['article_title'] = title
                article_context['article_publish_time'] = publish_time
                article_context['article_author'] = author
                article_context['article_content'] = content
                author_articles.append(article_context)
            except StaleElementReferenceException:
                print("元素已过期，无法再使用")
            except Exception as e:
                print("发生其他异常:", str(e))
            finally:
                # 关闭当前窗口并切换回原来的窗口
                # driver.close()
                driver.switch_to.window(driver.window_handles[0])
            # link = element.get_attribute("href")
            # driver.execute_script("window.open('" + link + "', '_blank');")
        driver.quit()
        return author_articles

    def publish_article(self, title, content, author='Lengxiao'):
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
        #'是否单标题'
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
        #上传完以后点击确定按钮
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




if __name__ == '__main__':
    http_name = 'www.toutiao.com'
    ob_Crawler = Crawler()
    # username = '18335948033'
    username = '18710090164'
    toutiao_url = 'https://www.toutiao.com/c/user/token/MS4wLjABAAAAUZKG_KuaxVrOMiwDd3QXX0ZB3Nh4bcv7AFs9ZFpJQMo/?'
    # ob_Crawler.gather()
    ob_Crawler.load_user_pass(section_name='toutiao')
    # ob_Crawler.login_with_password(username)
    ob_Crawler.login_with_cookie(username)
    author_articles = ob_Crawler.search(toutiao_url)
    title = author_articles[0]['article_title']
    content = author_articles[0]['article_content']
    author = 'Lengxiao'
    ob_Crawler.load_user_pass(section_name='toutiao')
    # ob_Crawler.login_with_password(username)
    ob_Crawler.login_with_cookie(username)
    ob_Crawler.publish_article(title=title, content=content, author=author)
