#encoding=utf-8
from system_config import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time,sys
import os, json
from configparser import ConfigParser
from bs4 import NavigableString

class BaseSelenium(object):
    name_platform = 'base'
    def __init__(self, mode="debug", useHead=True, login_url='', name_selenium='base'):
        if not os.path.exists("data"):
            os.mkdir("data")

        self.name_selenium = name_selenium
        self.dict_user_pass = {}
        self.driver = None
        self.login_url = login_url
        self.is_linux = self.get_is_linux()
        self.useHead = useHead


        ##  內容canshu
        self.g_title = 'every day is a good day'
        self.g_content = 'record things list'
        self.g_gen_date_hour = ''
        self.g_format_content = ''
        self.g_is_publish_success = ''
        self.path_video = ""
        self.path_image = ""

    def get_content_fron_dict(self, dic_info={}):
        self.g_title = dic_info.get("g_title", "")
        self.g_content = dic_info.get("g_content", "")
        self.g_gen_date_hour = dic_info.get("g_gen_date_hour", "")
        self.g_format_content = dic_info.get("g_format_content", "")
        self.g_is_publish_success = dic_info.get("g_is_publish_success", False)

        self.path_win_video = dic_info.get("path_win_video", "")
        self.path_linux_video = dic_info.get("path_linux_video", "")
        self.path_win_image = dic_info.get("path_win_image", "")
        self.path_linux_image = dic_info.get("path_linux_image", "")
        if self.is_linux:
            self.path_video = self.path_linux_video
            self.path_image = self.path_linux_image
        else:
            self.path_video = self.path_win_video
            self.path_image = self.path_win_image


    def get_is_linux(self):
        is_linux = False
        if sys.platform.startswith('win'):
            # 当前系统是 Windows
            is_linux = False
            print("[当前系统] windows")
        elif sys.platform.startswith('linux'):
            # 当前系统是 Linux
            print("[当前系统] linux")
            is_linux = True
        else:
            # 其他操作系统
            print("其他操作系统")
        return is_linux


    def publish_article(self, article_title='', article_content='', flag_debug=True):
        pass
        
    def save_driver_html(self, driver: webdriver, file_name="1.html"):
        file_name = "htmls/%s" % file_name
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(driver.page_source)

    def save_element_html(self, element, file_name="1.html"):
        file_name = "htmls/%s" % file_name
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(element.get_attribute("outerHTML"))

    def save_soup_html(self, soup, file_name='1.html'):
        with open('htmls/%s'%(file_name), 'w', encoding='utf-8') as f:
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
        if not self.useHead:
            print("使用headless 模式")
            chrome_options.add_argument('--headless')  
            chrome_options.add_argument('--log-level=3')

        if self.is_linux:
            #WEB_DRIVER_PATH = '/usr/local/bin/chromedriver'
            WEB_DRIVER_PATH = 'chromedriver'
            #driver = webdriver.Chrome(options=chrome_options, executable_path=WEB_DRIVER_PATH)
            #driver = webdriver.Chrome(executable_path='chromedriver')
            WEB_DRIVER_PATH = "/usr/local/bin/chromedriver"
            service = Service(WEB_DRIVER_PATH)
            driver = webdriver.Chrome(service=service, options=chrome_options)

        else:
            driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
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
            # print("add :", c)
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

        self.time_wait(wait_time, 5)
        return driver

    def time_wait(self, wait_time=0, interval = 3):
        count = int(wait_time/interval)
        for i in range(1,count+1):
            print("\t 等待%d S, 当前 %d s" % (wait_time, i*interval))
            time.sleep(interval)


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

        if not self.useHead:
            print("使用headless 模式")
            chrome_options.add_argument('--headless')  
            chrome_options.add_argument('--log-level=3')
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
