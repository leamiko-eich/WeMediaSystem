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

    def public_article(self, title, content, author='Lengxiao'):
        print('here is good!')
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
        time.sleep(2)

        #'是否单标题'
        single_title =  driver.find_element(By.CLASS_NAME,'byte-radio-inner checked')
        single_title.click()
        time.sleep(2)
        # 'byte-radio-inner checked'
        # input_content = driver.find_element(By.CLASS_NAME, 'rich_media_content')
        input_content = driver.find_element(By.ID, 'ueditor_0')
        print("input_content: ", input_content)
        self.save_element_html(input_content, 'body.html')
        input_content.send_keys(content)
        time.sleep(2)

        ## 正文插入图片
        button_image = driver.find_element(By.CLASS_NAME, 'tpl_item')
        self.save_element_html(button_image, 'button_image.html')
        button_image.click()
        time.sleep(2)

        ## 本地图片annual
        button_image_db = driver.find_elements(By.CLASS_NAME, 'tpl_dropdown_menu_item')[0]
        self.save_element_html(button_image_db, 'button_image_db.html')
        button_image_db.click()
        time.sleep(2)

        ## 本地选择图片
        image_path = "H:\\1.jpg"
        upload_input = button_image_db.find_element(By.NAME, 'file')
        self.save_element_html(upload_input, 'upload.html')
        # driver.execute_script("document.getElementsByName('file')[0].value = '%s'" % (image_path))
        upload_input.send_keys(image_path)
        time.sleep(3)

        print("关闭窗口", len(driver.window_handles))
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1]).close()

        time.sleep(3)

        flag_use_tupianku = False

        if flag_use_tupianku:
            ## 图片库选择
            button_image_db = driver.find_elements(By.CLASS_NAME, 'tpl_dropdown_menu_item')[1]
            self.save_element_html(button_image_db, 'button_image_db.html')
            button_image_db.click()
            time.sleep(2)

            ## 选择第1张图片
            button_first_image = driver.find_element(By.CLASS_NAME, 'weui-desktop-img-picker__item')
            if button_first_image.is_displayed():
                print("button kejian")
            else:
                print("button no kejian")
            self.save_element_html(button_first_image, 'button_first_image.html')
            button_first_image.click()
            time.sleep(2)

            # dialog = driver.find_element(By.CLASS_NAME, 'weui-desktop-dialog')
            # print("dialog:", dialog)
            # self.save_element_html(dialog, 'dialog.html')
            # driver.switch_to.frame(dialog)
            # time.sleep(3)

            button_dialog = driver.find_element(By.CLASS_NAME, 'weui-desktop-dialog__ft')
            self.save_element_html(button_dialog)
            if button_dialog.is_displayed():
                print("dialog kejian")
            else:
                print("dialog  00 kejian")
            time.sleep(2)

            ## 确认
            button_make_sure = driver.find_element(By.CLASS_NAME, 'weui-desktop-btn_wrp')
            # button_make_sure = button_make_sure.find_element(By.CLASS_NAME, 'weui-desktop-btn')
            print("button_make_sure:", button_make_sure)
            if button_make_sure.is_displayed():
                print("1元素可见")
            else:
                print("2元素no可见")
            self.save_element_html(button_make_sure, 'button_make_sure.html')
            time.sleep(2)
            # driver.execute_script("arguments[0].click();", button_make_sure)
            # ret = driver.execute_script("$(arguments[0]).click()", button_make_sure)
            # driver.execute_script("arguments[0].scrollIntoView();", button_make_sure)
            print("修改display属性")
            driver.execute_script("arguments[0].style.display = 'block';", button_make_sure)
            time.sleep(30)
            time.sleep(2)
            if button_make_sure.is_displayed():
                print("元素可见")
            else:
                print("元素no可见")
            ret = button_make_sure.click()
            print("ret:", ret)
            time.sleep(2)

        document_height = driver.execute_script("return document.body.scrollHeight")
        for i in range(int(document_height / 150)):
            print("往下滑动 %d" % (i))
            driver.execute_script("window.scrollTo(0, {0})".format(i * 150))
            time.sleep(1)

        flag_charu_fengmian = False
        if flag_charu_fengmian:
            ## 选择图片按钮
            pic_select = driver.find_element(By.ID, 'js_cover_area')
            print("pic_select:", pic_select)
            self.save_element_html(pic_select, 'pic_select.html')
            pic_select.click()

            ## 选择从正文选择图片
            toolbar_select = driver.find_element(By.CLASS_NAME, 'pop-opr__group')
            print("toolbar_select:", toolbar_select)
            self.save_element_html(toolbar_select, 'toolbar_select.html')

            ## 选择从正文选择图片
            zhengwen_select = toolbar_select.find_element(By.CLASS_NAME, 'pop-opr__button')
            self.save_element_html(zhengwen_select, 'zhengwen_select.html')
            zhengwen_select.click()
            time.sleep(3)

        time.sleep(50)
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
    ob_Crawler.public_article(title=title, content=content, author=author)
