#encoding=utf-8
from commonlib.message_queue import MsgConsumer, MsgProducer
from commonlib.schema import TaskInfo, GenerateArticle, PublicArticle, MsgInfo, ArtRequirements
from commonlib.media_interface.selenium_spiders import SeleniumManager

class GenerateContent(object):
    def __init__(self):
        self.msg_consumer = MsgConsumer(key_ex_queue_route="publish_hot_title")
        self.art_producer = MsgProducer(key_ex_queue_route="publish_article")




    def process_msg(self, json_data):
        msg_info  = MsgInfo(json_data)
        print("msg_info:", msg_info.convert_to_json())
        # self.platform_manage.call_platform(msg_info)

        art_requirements : ArtRequirements = msg_info.art_requirements

        title = art_requirements.question
        content = "今天的文章是关于: " + title



        list_platform  = ['Zhihu', "Douban"]
        list_platform  = ["Douban"]

        for platform in list_platform:
            msg_info = MsgInfo()
            msg_info.task_info.task_name = 'PublicArticle'
            msg_info.task_info.platform = platform
            msg_info.public_article.account_name = '18511400319'
            msg_info.public_article.platform = platform

            msg_info.generate_article.generate_title =  title
            msg_info.generate_article.generate_content = content
            msg_info.generate_article.format_content = '个人日记234234'


            json_msg = msg_info.convert_to_json()
            self.art_producer.produce_msg_list(msg_list=[json_msg])


    def loop_flow(self):
        pass

    def start_flow(self):
        self.msg_consumer.consumer_msg_list(self.process_msg, debug=False)