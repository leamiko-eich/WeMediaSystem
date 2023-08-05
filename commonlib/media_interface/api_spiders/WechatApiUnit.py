#encoding=utf-8
import requests
from bs4 import BeautifulSoup
import time
import random
from  lxml import etree
try:
    from BaseApiUnit import BaseApiUnit
except Exception as e:
    from scrawl.clean_api_unit.BaseApiUnit import BaseApiUnit

class WechatApiUnit(BaseApiUnit):
    def __init__(self):
        self.session  = requests.Session()


    def parse_one_page2(self, html_text):
        soup = BeautifulSoup(html_text, "html.parser")

        root = etree.HTML(str(soup))
        content = root.xpath('//div[@class="rich_media_content"]')

        print("\n parse_one_page2")
        print(len(content))

        all_text = content.get_text()
        print(all_text)
        print("\n\n")
    
    def parse_one_page(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
        }
        response = self.session.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        # print(response.text)
        with open("2.html", "w", encoding='utf-8') as f:
            f.write(response.text)

        # self.parse_one_page2(response.text)

        soup = BeautifulSoup(response.text, "html.parser")
        # with open('we2.html', 'w', encoding='utf-8') as f:
            # f.write(soup.prettify())
        root = etree.HTML(str(soup))
        content = root.xpath('//div[@class="rich_media_wrp"]')[0]
        self.save_ele_as_html(content, "we.html")


        title = content.xpath('.//h1[@class="rich_media_title"]')[0]
        self.save_ele_as_html(title, "title.html")
        title_text = title.text.strip().strip('\n')
        print("title:",title_text)

        # media_name = content.xpath('.//span[@class="rich_media_meta_nickname"]')[0]
        # media_name = content.xpath('//*[@id="profileBt"]')[0]
        media_name = content.xpath('//*[@id="js_name"]')[0]
        self.save_ele_as_html(media_name, "media.html")
        media_text = media_name.text.strip().strip('\n')
        print("media:", media_text)

        # publish_time = content.xpath('//*[@id="publish_time"]')[0]
        # self.save_ele_as_html(publish_time, "publish_time.html")
        # publish_time = publish_time.text.strip().strip('\n')
        # print("media:", publish_time)


        
        def get_text(element):
            text = element.text or ''
            for child in element:
                text += get_text(child)
            return text

        # Get all the text from the element and its children
        all_text = get_text(content)

        dic_info = {
            "recall_seg": "wechat_search",
            "ori_link": url,
            'art_title': title_text,
            "web_author": media_text,
            # "publish_time": publish_time,
            "art_content": all_text
        }
        # all_text = content.text_content()
        # print(all_text)
        # print("\n\n")
        return dic_info
        try:
            js_content = content[0].xpath('.//div[@id="js_content"]')
        except Exception as e:
            print("解析文章失败", e)
            return "No js_content"
        p_list = js_content[0].xpath('.//p')
        list_content = []
        for nid, p_ele in enumerate(p_list):
            list_txt = p_ele.xpath('.//text()')
            if len(list_txt) == 0:
                continue
            # print(nid, p_ele.xpath('.//text()'), ','.join(list_txt))
            list_content.append(','.join(list_txt))
        return "\n".join(list_content)



        # soup = BeautifulSoup(response.text, 'html.parser')
        # root = etree.HTML(str(soup))
        # titles = root.xpath('//td[@class="title"]')
    
    

if __name__ == "__main__":
    obj_wechat_unit = WechatApiUnit()
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1690546710&ver=4678&signature=btvhR34vGsH06Eg8kNn6yX2NAFtt1u0JE75Hi*L1sTA--AFc-zxAIJQ6dBpfAxj6Gfed2LJVnMdzS3-Y7hRZOrKoVS4t6IrjKyKShZj0AQYhhsKUFUjounx1bM25gL7m&new=1'
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1690546710&ver=4678&signature=AnY8LPtJCM*K0aNQxrufg6TOoM-gDCMg5CZTTmL4iu1okZBS1koyfoR0pwhqW*WvI7qjSu9S420pLsrDhL4rqtQ849PRrLi5ABgCKSCq5B-A7rr8L*x5Ze1AfBxlthrK&new=1'
    # url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1690546710&ver=4678&signature=AnY8LPtJCM*K0aNQxrufg6TOoM-gDCMg5CZTTmL4iu1okZBS1koyfoR0pwhqW*WvI7qjSu9S420pLsrDhL4rqtQ849PRrLi5ABgCKSCq5B-A7rr8L*x5Ze1AfBxlthrK&new=1'
    url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1690607872&ver=4679&signature=FEjSfrsYpYoaOQVp249bJFV7soR0Rpi4t0QdWVTHRpEpIOz99o2XJ7XAQvq8HvvS4qCUAiAivYRgfEJfQPRBZXJV453isBlR69816dBhbj01lmmHhqWBFyLdo8pf2mAF&new=1'
    content = obj_wechat_unit.parse_one_page(url)
    # print(content)