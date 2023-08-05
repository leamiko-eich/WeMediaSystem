from typing import Any
import copy
import pickle


class Article:
    def __init__(self, user='', author='', website='', category='', title='',  url='', create_date='', art_content=''):
        self.user = user
        self.author = author
        self.website = website
        self.category = category
        self.title = title
        self.url = url
        self.create_date = create_date
        self.art_content = art_content
        self.art_abstract = ""
        self.art_outline = ""
        self.recall_seg = ""

        self.status_code_ask_gpt = 200

        self.title_seg_list = []

    def set_title_seg_list(self, seg_list):
        self.title_seg_list = seg_list

    def set_recall_seg(self, recall_seg):
        self.recall_seg = recall_seg    

    def set_status_code_ask_gpt(self, status_code_ask_gpt):
        self.status_code_ask_gpt = status_code_ask_gpt

    def set_art_abstract(self, art_abstract):
        self.art_abstract = art_abstract

    def set_art_outline(self, art_outline):
        self.art_outline = art_outline

    def __str__(self):
        return f"{self.user}\t{self.author}\t{self.title}\t{self.url}"


class UserConfig(object):
    def __init__(self, user="", author="", website="", category="", subscribe_url="", crawl_date="", dbname='', row_id=''):
        self.user = user 
        self.author = author 
        self.website = website
        self.category = category
        self.subscribe_url = subscribe_url
        self.crawl_date = crawl_date
        self.new_scrawl_date = '1970-01-01 01'
        self.dbname = dbname
        self.row_id = row_id

    def set_new_scrawl_date(self, new_scrawl_date):
        self.new_scrawl_date = new_scrawl_date

    def parse_from_post_dict(self, post_dict):
        self.user = post_dict["user"]
        self.author = post_dict["author_name"]
        self.website = post_dict["website"]
        self.category = post_dict["category"]
        self.subscribe_url = post_dict["subscribe_url"]
        self.crawl_date = "2023-01-01"

    def __str__(self):
        return "%s\t%s\t%s\t%s\t%s\t" \
            "%s\t%s\t%s" % (self.user, self.author, self.website, self.category,  self.subscribe_url,
                               self.crawl_date, self.dbname, self.row_id)



class HotPointArticle(object):
    def __init__(self, dic_info={}):
        self.row_id = dic_info.get("row_id", "")
        self.hot_day = dic_info.get("日期", "")
        if self.hot_day =="":
            self.hot_day = dic_info.get("hot_day", "")
        self.hot_art_title = dic_info.get("title", "")
        if self.hot_art_title =="":
            self.hot_art_title = dic_info.get("hot_art_title", "")
        self.art_content=  dic_info.get("art_content", "")
        self.web_author = dic_info.get("web_author", "")
        self.ori_link = dic_info.get("链接", "")
        if self.ori_link =="":
            self.ori_link = dic_info.get("ori_link", "")

        self.origin_source = dic_info.get("来源", "")
        self.hot_category = dic_info.get("category", "")
        self.hot_seg_list = dic_info.get("seg_list", "")    
        self.human_seg = dic_info.get("human_seg", "")

    def convert_to_dict(self):
        dic_info = {
            "row_id": self.row_id,
            "hot_day": self.hot_day,
            "hot_art_title": self.hot_art_title,
            "web_author": self.web_author,
            "ori_link": self.ori_link,
            "human_seg": self.human_seg,
        }
        return dic_info

class RecallArticleLine(object):
    def __init__(self, dic_info = {}):
        self.art_title = dic_info.get("art_title", "")
        self.art_content = dic_info.get("art_content", "")
        self.web_author = dic_info.get("web_author", "")
        self.recall_seg = dic_info.get("recall_seg", "")
        self.ori_link = dic_info.get("ori_link", "")
        self.row_id = dic_info.get("row_id", "")



    def convert_to_dict(self):
        dic_info = {
            "art_title": self.art_title,
            "art_content": self.art_content,
            "web_author": self.web_author,
            "recall_seg": self.recall_seg,
            "ori_link": self.ori_link,
            "row_id": self.row_id,
        }
        return dic_info

        
class AiTaskInfo(object):
    def __init__(self, dic_info={}) -> None:
        self.task_title = dic_info.get("task_title", "")

        ## read
        self.prompt = dic_info.get("prompt", "")
        self.content = dic_info.get("content", "")
        self.create_dt_hour = dic_info.get("create_dt_hour", "")
        self.ai_response = dic_info.get("ai_response", "")

        ## write
        self.target_column = dic_info.get("target_column", "")
        self.target_status_column = dic_info.get("target_status_column", "")

    def set_ai_response(self, ai_response):
        self.ai_response = ai_response

    
    def convert_to_dict(self):
        dic_info = {
            "task_title": self.task_title,
            "prompt": self.prompt,
            "content": self.content,
            "create_dt_hour": self.create_dt_hour,
            "target_column": self.target_column,
            "target_status_column": self.target_status_column,
            "ai_response": self.ai_response,
        }
        return dic_info
        


        
class MessageProto(object):
    def __init__(self, dic_info={}):
        ## proto
        self.task_name = dic_info.get("task_name", "")
        
        ## body
        self.hot_point_art = HotPointArticle( dic_info.get("hot_point_art", {}) )
        self.recall_art = RecallArticleLine( dic_info.get("recall_art", {}) )
        self.ai_task_info = AiTaskInfo( dic_info.get("ai_task_info", {}) )

    def get_task_name(self):
        return self.task_name

    def set_task_name(self, task_name):
        self.task_name = task_name

    def set_recall_art(self, recall_art):
        self.recall_art = copy.deepcopy(recall_art)

    def set_hot_point_art(self, hot_point_art):
        self.hot_point_art = copy.deepcopy(hot_point_art)

    def set_ai_task_info(self, ai_task_info):
        self.ai_task_info = copy.deepcopy(ai_task_info)

    def convert_to_dict(self):
        dic_info = {
            "task_name": self.task_name,
            "hot_point_art": self.hot_point_art.convert_to_dict(),
            "recall_art": self.recall_art.convert_to_dict(),
            "ai_task_info": self.ai_task_info.convert_to_dict(),
        }

        return dic_info


        
