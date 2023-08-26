#encoding=utf-8
import time
import os

from BaseSelenium import BaseSelenium
from selenium import webdriver
from selenium.webdriver.common.by import By
class LocalTestSelenium(BaseSelenium):
    def __init__(self):
        super().__init__()  
        pass

    def test_html(self, path_local_html):
        chrome_options = self.get_chrome_options()

        driver = webdriver.Chrome(options=chrome_options)

        # driver.get("file:///" + path_local_html)
        # dir_path = "/i/BaiduYunDownload/06code/WeMediaSystem/commonlib/media_interface/selenium_spiders"
        current_dir = os.path.dirname(os.path.realpath(__file__)) 
        html_file_path = os.path.join(current_dir, '1.html')
        driver.get("file://" + html_file_path)

        ## Start
        div_continue = driver.find_element(By.CSS_SELECTOR, '._ac7b._ac7d')
        self.save_element_html(div_continue, 'instgram_div_continue.html')

        div_continue_button = div_continue.find_element(By.XPATH, "//div[text()='继续']")
        self.save_element_html(div_continue_button, 'instgram_div_continue_button.html')
        
        time.sleep(60)
        driver.quit()


    
if __name__ == '__main__':
    obj_local_selenium = LocalTestSelenium()
    path_local_html = "data/instgram_div_dialog.html"

    obj_local_selenium.test_html(path_local_html)
