#encoding=utf-8
from system_config import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from configparser import ConfigParser

class BaseSelenium(object):
    def __init__(self, mode="debug"):
        if not os.path.exists("data"):
            os.mkdir("data")

        self.dict_user_pass = {}

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
                #
        #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        # driver = webdriver.Chrome()
            WEB_DRIVER_PATH = '/usr/bin/chromedriver'
            driver = webdriver.Chrome(options=chrome_options, executable_path=WEB_DRIVER_PATH)
        else:
            # chrome_options.add_argument("user-data-dir=C:\\Users\\你用户名\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")
            print("使用profile 1")
            chrome_options.add_argument("user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\google\\Chrome\\User Data\\Profile 1")
            driver = webdriver.Chrome(options=chrome_options)

        self.driver = driver

        
    def save_driver_html(self, driver: webdriver, file_name="1.html"):
        file_name = "data/%s" % file_name
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(driver.page_source)

    def save_element_html(self, element, file_name="1.html"):
        file_name = "data/%s" % file_name
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(element.get_attribute("outerHTML"))


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
