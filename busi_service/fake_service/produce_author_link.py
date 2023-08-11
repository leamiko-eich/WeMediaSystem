#encoding=utf-8
import os,sys
ROOTDIR_WeMediaSystem = os.getenv('ROOTDIR_WeMediaSystem')
os.chdir(ROOTDIR_WeMediaSystem)
sys.path.append(ROOTDIR_WeMediaSystem)

from commonlib.message_queue.MsgProducer import MsgProducer
from commonlib.schema import TaskInfo, GenerateArticle, PublicArticle, MsgInfo, TargetAuthor


class ProduceAuthorLink(object):
    def __init__(self):
        curpaht = os.getcwd()
        print("curpaht:", curpaht)

        self.art_producer = MsgProducer(key_ex_queue_route="scrwal_author_link")

    def generat_fake_info(self):

        msg_info = MsgInfo()
        msg_info.task_info.task_name = 'ScrwalAuthorLink'

        msg_info.target_author.author = '黛西呜呜'
        msg_info.target_author.subscribe_link = 'https://www.zhihu.com/people/dxww/posts'
        msg_info.target_author.platform = 'Zhihu'



        return msg_info.convert_to_json()


    def start_flow(self):

        for i in range(1):
            one_msg = self.generat_fake_info()
            list_msg = [one_msg]

            self.art_producer.produce_msg_list(list_msg)

    
    
if __name__ == "__main__":
    obj_produce_articles = ProduceAuthorLink()
    obj_produce_articles.start_flow()

