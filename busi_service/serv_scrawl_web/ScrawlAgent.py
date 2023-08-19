#encoding=utf-8
from commonlib.message_queue import MsgConsumer
from commonlib.schema import TaskInfo, GenerateArticle, PublicArticle, MsgInfo
from commonlib.media_interface.selenium_spiders import SeleniumManager

class ScrawlAgent(object):
    def __init__(self):
        self.msg_consumer = MsgConsumer(key_ex_queue_route="scrwal_author_link")

        self.platform_manage = SeleniumManager()
        self.platform_manage.init_platforms()

        

    def process_msg(self, json_data):
        msg_info  = MsgInfo(json_data)
        print("msg_info:", msg_info.convert_to_json())
        self.platform_manage.scrawl_platform(msg_info)

    def loop_flow(self):
        pass

    def start_flow(self):
        self.msg_consumer.consumer_msg_list(self.process_msg, debug=False)