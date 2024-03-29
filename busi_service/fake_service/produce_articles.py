#encoding=utf-8
import os,sys
ROOTDIR_WeMediaSystem = os.getenv('ROOTDIR_WeMediaSystem')
os.chdir(ROOTDIR_WeMediaSystem)
sys.path.append(ROOTDIR_WeMediaSystem)

from commonlib.message_queue.MsgProducer import MsgProducer
from commonlib.schema import TaskInfo, GenerateArticle, PublicArticle, MsgInfo


class ProduceArticles(object):
    def __init__(self):
        curpaht = os.getcwd()
        print("curpaht:", curpaht)

        self.art_producer = MsgProducer(key_ex_queue_route="publish_article")

    def generat_fake_info(self):

        msg_info = MsgInfo()
        msg_info.task_info.task_name = 'PublicArticle'
        msg_info.task_info.platform = 'Zhihu'
        msg_info.public_article.account_name = '18511400319'
        msg_info.public_article.platform = 'Zhihu'

        msg_info.generate_article.generate_title = '个人日记234234324243234'
        msg_info.generate_article.generate_content = '个人日记12323213123123'
        msg_info.generate_article.format_content = '个人日记234234'



        return msg_info.convert_to_json()


    def start_flow(self):

        for i in range(1):
            one_msg = self.generat_fake_info()
            list_msg = [one_msg]

            self.art_producer.produce_msg_list(list_msg)

    
    
if __name__ == "__main__":
    obj_produce_articles = ProduceArticles()
    obj_produce_articles.start_flow()

