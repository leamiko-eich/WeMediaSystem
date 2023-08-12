import json
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
try:
    from .BaseSelenium import BaseSelenium
except Exception as e:
    from BaseSelenium import BaseSelenium

 
 
class Crawler(BaseSelenium):
    def __init__(self):
        pass

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
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')
   
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
        ##登录百度知道
        logurl = 'https://zhidao.baidu.com/'
        #登录前清楚所有cookie
        driver.delete_all_cookies()
        driver.get(logurl)
        ##登录前打印cookie
        print(driver.get_cookies())
     
        ##点击登录按钮
        # driver.find_element_by_xpath('//*[@id="userbar-login"]').click()
        driver.find_element(By.ID, "userbar-login").click()
        # driver.find_element_by_id("userbar-login").click()
        time.sleep(2)
        ##首次尝试的 默认进入扫码登录的界面
        try:
        #   footerULoginBtn = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__footerULoginBtn"]')
          footerULoginBtn = driver.find_element(By.ID, "TANGRAM__PSP_11__changePwdCodeItem")
          footerULoginBtn.click() #切换到用户名和密码登录
          footerULoginBtn_not_exist = False
          print("切换到用户名和密码登录")
        except:
          print("Error 账户密码登录按钮不存在")
          footerULoginBtn_not_exist = True
    
     
        ## 用户名跟密码的设置并点击提交
        user = driver.find_element(By.ID, "TANGRAM__PSP_11__userName")
        user.clear()
        pwd = driver.find_element(By.ID, "TANGRAM__PSP_11__password")
        pwd.clear()
        submit = driver.find_element(By.ID, "TANGRAM__PSP_11__submit")
        user.send_keys(username)
        time.sleep(3)
        pwd.send_keys(password)
        time.sleep(3)
    
        submit.click()
        print("等待拖动-发送验证码")
        time.sleep(30)
    
        if 3>10:
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
     

        time.sleep(60)
        return

    def login_with_cookie(self, username = ''):
        # assert (username in self.dict_user_pass)
        chrome_options = Options()
    
        chrome_options.add_argument("window-size=1024,768")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')
   
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-browser-side-navigation')
        chrome_options.add_argument('enable-automation')
        chrome_options.add_argument('--disable-infobars')

        driver = webdriver.Chrome(options=chrome_options)
   
        wait = WebDriverWait(driver, 1)
    
        ##登录百度知道
    
        #登录前清楚所有cookie
        driver.delete_all_cookies()
        driver.get(self.logurl)
        time.sleep(2)
    
        f1 = open('data/%s.json' % (username))
        cookie = f1.read()
        cookie = json.loads(cookie)
        for c in cookie:
            print("add :", c)
            driver.add_cookie(c)
        # # 刷新页面
        time.sleep(2)
        driver.refresh()


        return driver

    def test_js(self, driver):
        driver.get("http://www.baidu.com")
        driver.execute_script('document.getElementById("kw").value = "test"')
        time.sleep(2)
        driver.execute_script('document.getElementById("su").click()')
        time.sleep(2)
 

        
if __name__ == '__main__':
    ob_Crawler = Crawler()
    # username = '18335948033'
    username = '18511400319'
 
    # ob_Crawler.gather()
    # ob_Crawler.load_user_pass()
    # ob_Crawler.login_with_password(username)
    driver = ob_Crawler.login_with_cookie(username)
    ob_Crawler.test_js(driver)