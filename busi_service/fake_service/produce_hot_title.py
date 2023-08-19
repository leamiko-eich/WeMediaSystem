#encoding=utf-8
import os,sys
ROOTDIR_WeMediaSystem = os.getenv('ROOTDIR_WeMediaSystem')
os.chdir(ROOTDIR_WeMediaSystem)
sys.path.append(ROOTDIR_WeMediaSystem)

from commonlib.message_queue.MsgProducer import MsgProducer
from commonlib.schema import TaskInfo, GenerateArticle, PublicArticle, MsgInfo

import random

class ProduceHotTitle(object):
    def __init__(self):
        curpaht = os.getcwd()
        print("curpaht:", curpaht)

        self.art_producer = MsgProducer(key_ex_queue_route="publish_hot_title")

        path_fake_title = 'busi_service/fake_service/data/question.txt'
        self.list_fake_title = []
        with open(path_fake_title, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                self.list_fake_title.append(line)

    def generat_fake_info(self):

        randInt = random.randint(0, len(self.list_fake_title)-1)
        fake_title = self.list_fake_title[randInt]
        print("fake_title:", fake_title)

        msg_info = MsgInfo()
        msg_info.task_info.task_name = 'PublicHotTitle'
        msg_info.art_requirements.question = fake_title




        return msg_info.convert_to_json()


    def start_flow(self):

        for i in range(1):
            one_msg = self.generat_fake_info()
            list_msg = [one_msg]

            self.art_producer.produce_msg_list(list_msg)

    
    
if __name__ == "__main__":
    obj_produce_articles = ProduceHotTitle()
    obj_produce_articles.start_flow()

