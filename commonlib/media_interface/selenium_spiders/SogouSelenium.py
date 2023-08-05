#encoding=utf-8
from system_config import is_linux, root_directory
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import sys
try:
    from BaseSelenium import BaseSelenium
    flag_simple_test = True
except:
    from scrawl.selenium.BaseSelenium import BaseSelenium
    flag_simple_test = False

import configparser
import os



class SogouSelenium(BaseSelenium):
    def __init__(self, mode="debug"):
        super().__init__(mode=mode)
        self.config = configparser.ConfigParser()

        if flag_simple_test:
            self.config.read("config/sogou_search.ini", encoding="utf-8")
        else:
            self.config.read("%s/scrawl/selenium/config/sogou_search.ini" % (root_directory), encoding="utf-8")

        self.num_search_article = self.config.getint("KeywordSearch", "num_search_article")
        self.timewait_one_article = self.config.getint("KeywordSearch", "timewait_one_article")

    def debug_info(self, driver, flag_name=""):
        print("\n ==============flag_name:", flag_name)
        print("title:", driver.title)
        print("current_url:", driver.current_url)
        print("cookie:", driver.get_cookies())

    def tackle_search_page(self, target_url=''):

        driver = self.driver
        ret = driver.get(target_url)
        title = driver.title


        ## 寻找文章链接-点击
        # id_name = "sogou_vr_11002601_box_0"
        max_num = self.num_search_article
        list_article_url = []

        main_window = driver.current_window_handle
        for nid in range(max_num):
            # id_name = "sogou_vr_11002601_title_0"

            logging.info("==> 处理文章nid:%d" % (nid))

            try:
                targetLocator = (By.ID, "sogou_vr_11002601_title_%d" % (nid))
                WebDriverWait(driver, 3).until(EC.presence_of_element_located(targetLocator))
            except TimeoutException:
                logging.info("找不到元素 keyword:%s TimeoutException" % ( str(nid)))
                self.save_driver_html(driver, "timeout.html")
                return list_article_url

            self.save_driver_html(driver, "init_%d.html" % (nid))
            id_name = "sogou_vr_11002601_title_%d" % (nid)
            article_button = driver.find_element(By.ID, id_name)
            self.save_element_html(article_button, "button.html")
            article_button.click()



            time.sleep(1)
            all_handles = driver.window_handles
            driver.switch_to.window(all_handles[-1])

            targetLocator = (By.ID, "activity-detail")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(targetLocator))
            logging.info("\t\t 获取到url:", driver.current_url)
            list_article_url.append(driver.current_url)
            time.sleep(self.timewait_one_article)

            self.save_driver_html(driver, "page_%d.html" % (nid))
            driver.close()

            driver.switch_to.window(main_window)

        return list_article_url



    def start_search(self, keyword = '中国'):
        driver = self.driver

        logging.info("打开首页  keyword:%s" % (keyword))
        target_url = "https://weixin.sogou.com/"
        ret = driver.get(target_url)
        title = driver.title


        is_error = False
        try:
            targetLocator = (By.ID, "query")       ## 包含热词榜单
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(targetLocator))
        except TimeoutException:
            logging.info("\t 找不到元素 keyword:%s TimeoutException" % (keyword))
            self.save_driver_html(driver, "timeout.html")
            is_error = True
        finally:
            pass

        if is_error:
            driver.close()
            return []

        logging.info("\t 输入关键字:%s" % (keyword))
        box_input = driver.find_element(By.ID, "query")
        box_input.send_keys(keyword)
        time.sleep(3)
        self.save_driver_html(driver, "1.html")


        logging.info("\t 定位-搜索文章-点击")
        click_box = driver.find_element(By.CLASS_NAME, "enter-input")
        click_box.click()

        logging.info("\t 等待获取-> 搜索url")

        try:
            targetLocator = (By.ID, "hotword")       ## 包含热词榜单
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(targetLocator))
        except TimeoutException as e:
            logging.info("\t 找不到元素 keyword:%s TimeoutException" % (keyword))
            self.save_driver_html(driver, "timeout.html")
            return []


        search_url = driver.current_url
        logging.info("\t > 搜索url:%s" %(search_url))

        list_article_url = self.tackle_search_page(target_url=search_url)
        return list_article_url


if __name__ == "__main__":
    mode = 'debug'
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    obj_driver = SogouSelenium(mode=mode)
    keywordk = "罗刹海市"
    # keywordk = "外交部长秦刚"
    list_article = obj_driver.start_search(keyword=keywordk)
    for art_url in list_article:
        print(art_url)

    #target_url = 'https://weixin.sogou.com/weixin?ie=utf8&s_from=input&_sug_=y&_sug_type_=&type=2&query=%E7%BD%97%E5%88%B9%E6%B5%B7%E5%B8%82'
    #obj_driver.tackle_search_page(target_url=target_url)
    # obj_driver.quit_driver()
