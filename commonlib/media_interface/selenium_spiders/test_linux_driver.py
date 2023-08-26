#encoding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
print(webdriver.__file__)
print(webdriver.__version__)

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('start-maximized')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--disable-browser-side-navigation')
chrome_options.add_argument('enable-automation')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('enable-features=NetworkServiceInProcess')

WEB_DRIVER_PATH = "/usr/local/bin/chromedriver "
service = Service(WEB_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)
