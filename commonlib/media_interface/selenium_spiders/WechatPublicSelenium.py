#encoding=utf-8
#encoding=utf-8
__package__ == 'selenium_spiders'
try:
    from BaseSelenium import BaseSelenium
except Exception as e:
    from .BaseSelenium import BaseSelenium

import time,json
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

class WechatPublicSelenium(BaseSelenium):
    def __init__(self):
        super().__init__()
        self.name_selenium = 'WechatPublic'
        self.login_url = 'https://mp.weixin.qq.com/'

    def login_with_password(self, username=''):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("window-size=1024,768")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')
   
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-browser-side-navigation')
        chrome_options.add_argument('enable-automation')

        driver = webdriver.Chrome(options=chrome_options)

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
          "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
        driver.get(self.login_url)

        time.sleep(30)
        filename = "%s_%s" % (self.name_selenium, username)
        self.persist_cookie_info(driver, filename)

        time.sleep(30)
        driver.quit()

    def public_article(self, title, content, author='John'):
        driver : webdriver.Chrome = self.get_driver()
        driver.get(self.login_url)

        time.sleep(3)
        menu = driver.find_element(By.CLASS_NAME, "new-creation__menu-content")
        print("menu:", menu)
        self.save_element_html(menu, 'menu.html')
        menu.click()


        ## 切换窗口
        all_handles = driver.window_handles
        driver.switch_to.window(all_handles[-1])

        input_title = driver.find_element(By.ID, 'title')
        driver.execute_script("arguments[0].value = 'aaaaa%s'" % (title), input_title)
        # input_title.send_keys(title)
        time.sleep(2)

        input_author = driver.find_element(By.ID, 'author')
        input_author.send_keys(author)
        time.sleep(2)

        # input_content = driver.find_element(By.CLASS_NAME, 'rich_media_content')
        input_content = driver.find_element(By.ID, 'ueditor_0')
        self.save_element_html(input_content, 'body.html')
        # input_content.send_keys(content)
        driver.execute_script("arguments[0].value = 'bbbb%s'" % (content), input_content)
        time.sleep(2)

        
        # 获取iframe
        # iframe = driver.find_element_by_id("ueditor_0")

        # 执行js插入内容 
        js = '''
        var iframe = document.getElementById('ueditor_0');
        var doc = iframe.contentDocument;  
        var p1 = doc.createElement('p');
        p1.textContent = 'Paragraph 1';
        var p2 = doc.createElement('p');
        p2.textContent = 'Hello world';
        doc.body.appendChild(p1);
        doc.body.appendChild(p2);
        '''
        driver.execute_script(js)

        time.sleep(2)

        js = '''
        var iframe = document.getElementById('ueditor_0');
        var doc = iframe.contentDocument;  
        var p1 = doc.createElement('p');
        p1.textContent = 'Paragraph 3';
        var p2 = doc.createElement('p');
        p2.textContent = 'Hello world222';
        doc.body.appendChild(p1);
        doc.body.appendChild(p2);
        '''
        # driver.execute_script(js)
        # time.sleep(2)

        # 构造图片元素

        # 插入图片 
        insert_img = '''
        var img = document.createElement('img');
        img.src = 'https://5b0988e595225.cdn.sohucs.com/images/20200307/2fcefe1c46904239aedb0b0e0af2a611.jpeg';
        img.width = 200;

        var iframe = document.getElementById('ueditor_0');
        var doc = iframe.contentDocument;
        doc.body.appendChild(img);
        '''

        driver.execute_script(insert_img) # 再插入到文档中

        self.save_driver_html(driver, 'driver.html')

        # body_input = driver.find_element(By.CSS_SELECTOR, '.view.rich_media_content.autoTypeSetting24psection')
        #body_input = input_content.find_element(By.CSS_SELECTOR, '.view.rich_media_content.autoTypeSetting24psection')
        #self.save_element_html(body_input, 'body_input.html')

        # driver.execute_script("var body_input=document.querySelector('.view.rich_media_content.autoTypeSetting24psection'); body_input.innerHTML = 'aaaa%s'" % (content))

        # time.sleep(10)


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
        for i in range(int(document_height/150)):
            print("往下滑动 %d" % (i))
            driver.execute_script("window.scrollTo(0, {0})".format(i*150))
            time.sleep(1)

        


        flag_charu_fengmian = True
        if flag_charu_fengmian:
            ## 选择图片按钮

            
            # 找到封面区域元素
            # cover_area = driver.find_element_by_class_name('js_cover_btn_area')
            cover_area = driver.find_element(By.ID, 'js_cover_area')
            self.save_element_html(cover_area, 'pic_select_before.html')

            # 移动到元素上,显示按钮
            actions = ActionChains(driver)  
            actions.move_to_element(cover_area)
            time.sleep(1)
            actions.perform()
            time.sleep(1)
            cover_area = driver.find_element(By.ID, 'js_cover_area')
            self.save_element_html(cover_area, 'pic_select_after.html')

            # pic_select = driver.find_element(By.ID, 'js_cover_area')
            # print("pic_select:", pic_select)
            # self.save_element_html(pic_select, 'pic_select.html')
            # pic_select.click()

            time.sleep(10)

            ## 选择从正文选择图片
            toolbar_select = driver.find_element(By.CLASS_NAME, 'pop-opr__group')
            print("toolbar_select:", toolbar_select)
            self.save_element_html(toolbar_select, 'toolbar_select.html')

            time.sleep(10)

            ## 选择从正文选择图片
            zhengwen_select = toolbar_select.find_element(By.CLASS_NAME, 'pop-opr__button')
            self.save_element_html(zhengwen_select, 'zhengwen_select.html')
            zhengwen_select.click()
            time.sleep(3)
        

        
        time.sleep(50)
        driver.quit()


        
if __name__ == '__main__':
    obj_wechat_public = WechatPublicSelenium()
    username = '18511400319'
    # obj_wechat_public.login_with_password(username)

    obj_wechat_public.login_with_cookie(username)
    obj_wechat_public.public_article('title', 'content')
