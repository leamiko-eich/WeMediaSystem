#encoding=utf-8
from system_config import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import os, json
from configparser import ConfigParser
from bs4 import NavigableString

class BaseSelenium(object):
    name_platform = 'base'
    def __init__(self, mode="debug"):
        if not os.path.exists("data"):
            os.mkdir("data")

        self.name_selenium = 'base'
        self.dict_user_pass = {}
        self.driver = None
        self.login_url = ''

        chrome_options = webdriver.ChromeOptions()
        #path_driver = "H:\driver\chromedriver.exe"
        #chrome_options.binary_location = path_driver
        if mode=="online":
            chrome_options.add_argument('--headless')  
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')

        if is_linux:
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('start-maximized')
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument('--disable-browser-side-navigation')
            chrome_options.add_argument('enable-automation')
            chrome_options.add_argument('--disable-infobars')
            chrome_options.add_argument('enable-features=NetworkServiceInProcess')
            WEB_DRIVER_PATH = '/usr/bin/chromedriver'
            driver = webdriver.Chrome(options=chrome_options, executable_path=WEB_DRIVER_PATH)
        else:
            print("使用profile 1")
            # chrome_options.add_argument("user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\google\\Chrome\\User Data\\Profile 1")
            # driver = webdriver.Chrome(options=chrome_options)

        # self.driver = driver

    def publish_article(self, article_title='', article_content=''):
        pass
        
    def save_driver_html(self, driver: webdriver, file_name="1.html"):
        file_name = "data/%s" % file_name
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(driver.page_source)

    def save_element_html(self, element, file_name="1.html"):
        file_name = "data/%s" % file_name
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(element.get_attribute("outerHTML"))

    def save_soup_html(self, soup, file_name='1.html'):
        with open('data/%s'%(file_name), 'w', encoding='utf-8') as f:
            f.write(soup.prettify())

    def set_driver(self, driver):
        self.driver = driver

    def get_driver(self):
        assert(self.driver is not None)
        return self.driver

    def get_texts_from_bs4(self, element):
        texts = []
        for child in element.children:
            if isinstance(child, NavigableString):
                texts.append(child.string)
            else:
                texts.extend(self.get_texts_from_bs4(child))
        return texts


    def login_with_cookie(self, username = '', wait_time=0):
        chrome_options = webdriver.ChromeOptions()
    
        chrome_options.add_argument("window-size=1024,1168")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')
   
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument('start-maximized')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-browser-side-navigation')
        chrome_options.add_argument('enable-automation')
        chrome_options.add_argument('--disable-infobars')
        if self.name_platform == 'Xiaohongshu':
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        elif self.name_platform == 'Qiehao':
            ## 暂时关掉SSL报错，需要处理
            print("关闭SLS报错")
            chrome_options.add_argument("--supress-connection-errors")

        driver = webdriver.Chrome(options=chrome_options)
   
        time.sleep(2)
        print("login_url:%s" % (self.login_url))
        logurl = self.login_url
    
        #登录前清楚所有cookie
        driver.delete_all_cookies()
        driver.get(logurl)
        time.sleep(2)


        print("等待-加载cookie")    
        filename = "%s_%s" % (self.name_selenium, username)
        f1 = open('data/%s.json' % (filename))
        cookie = f1.read()
        cookie = json.loads(cookie)

        ## 使用字典记录 key= domain + name
        dic_cookie = {}
        for c in cookie: 
            key = "%s_%s" % (c['domain'], c['name'])
            dic_cookie[key] = c


        ## 首次记载cookie
        for c in cookie:
            print("add :", c)
            driver.add_cookie(c)
        # # 刷新页面
        time.sleep(2)
        driver.get(logurl)
        time.sleep(3)
        # driver.refresh()          ## 直接使用refresh，会丢失参数
        print("cookie-加载完毕")

        
        ## 多次检验cookie, 增加缺失字段
        # for cnt in range(1,5):
            # print("\n ============> 第%d次 检查cookie" % (cnt))
            # new_cookie = self.persist_cookie_info(driver, '第%d次cookie'%(cnt), cnt)
            # new_dict_cookie = {}
            # for new_c in new_cookie:
                # key = "%s_%s" % (new_c['domain'], new_c['name'])
                # if key in new_dict_cookie:
                    # print("\t Duplicate key:%s" % (key))
                # new_dict_cookie[key] = new_c
            # for key in dic_cookie:
                # value = dic_cookie[key]
                # if key not in new_dict_cookie:
                    # print("\t Missing key:%s" % (key), "add ",  value)
                    # list_str = []
                    # for t_k, t_v in value.items():
                        # list_str.append("%s=%s" % (t_k, t_v))
                    # print("\t \t add %s" %  ("; ".join(list_str)) )
                    # ret = driver.add_cookie(dic_cookie[key])
                    # print("\t \t add ret:", ret)
                # else:
                    # if new_dict_cookie[key]['value'] != dic_cookie[key]['value']:
                        # print("\t NotEqual key:%s" % (key) )
                # print("\t 【修改完等地10")
                # time.sleep(10)
# 
            # print("\t 刷新cookie, 等待7S")
            # time.sleep(2)
            # driver.get(logurl)
            # time.sleep(120)

        self.set_driver(driver)

        for i in range(wait_time):
            print("\t 等待%d S, 当前 %d s" % (wait_time, i))
            time.sleep(1)
        return driver


    def login_with_password(self, username=''):
        pass

    def persist_cookie_info(self, driver, filename, cnt=0):
        ### 获取cookie
        print("\t[第%d次] 获取->保存cookie" % (cnt))

        cookie = driver.get_cookies()
        jsonCookies = json.dumps(cookie)
        with open('data/%s.json' % (filename), 'w') as f:
            f.write(jsonCookies)
        print("\t[第%d次] cookie-保存完毕" % (cnt))
        return cookie

    def load_user_pass(self, path_config = 'config/user_pass.ini', section_name = "baidu"):
        config = ConfigParser()
        config.read( path_config, encoding="utf-8")

        section_dict = dict(config.items(section_name))
        print("dict:", section_dict)
        self.dict_user_pass = section_dict
        return section_dict

            
    def quit_driver(self):
        time.sleep(10)
        self.driver.quit()

    def get_chrome_options(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("window-size=1024,768")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')
   
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument('start-maximized')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-browser-side-navigation')
        # chrome_options.add_argument('enable-automation')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        if self.name_platform == 'Xiaohongshu':
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        return chrome_options

        
    def switch_to_new_windows(self, driver):
        all_handles = driver.window_handles
        driver.switch_to.window(all_handles[-1])

        time.sleep(4)


    def scroll_to_bottom(self, driver):
        document_height = driver.execute_script("return document.body.scrollHeight")
        for i in range(int(document_height/150)):
            print("往下滑动 %d" % (i))
            driver.execute_script("window.scrollTo(0, {0})".format(i*150))
            time.sleep(1)

            
    ## 爬虫基类接口
    def crawl_by_author_link(self, url=None):
        ## 根据作者订阅链接，获取文章链接
        pass

    def parse_specific_article(self, url):
        ## 根据文章链接，获取内容
        pass