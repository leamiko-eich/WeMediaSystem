#encoding=utf-8
from system_config import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

class BaseSelenium(object):
    def __init__(self, mode="debug"):

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

            
    def quit_driver(self):
        time.sleep(10)
        self.driver.quit()
