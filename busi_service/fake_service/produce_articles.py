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
        msg_info.public_article.account_name = '18511400319'
        msg_info.public_article.platform = 'zhihu'

        msg_info.generate_article.generate_title = '个人日记'
        msg_info.generate_article.format_content = '个人日记'

        return msg_info


    def start_flow(self):
        pass

    
    
if __name__ == "__main__":
    obj_produce_articles = ProduceArticles()
    obj_produce_articles.start_flow()

