#encoding=utf-8

class MsgInfo(object):
    def __init__(self, dic_info={}):
        self.task_info = TaskInfo(dic_info.get("task_info", {}))
        self.target_author = TargetAuthor(dic_info.get("target_author", {}))
        self.generate_article = GenerateArticle(dic_info.get("generate_article", {}))
        self.public_article = PublicArticle(dic_info.get("public_article", {}))

    def convert_to_json(self):
        dic_info = {
            "task_info": self.task_info.convert_to_json(),
            "target_author": self.target_author.convert_to_json(),
            "generate_article": self.generate_article.convert_to_json(),
            "public_article": self.public_article.convert_to_json()
        }
        return dic_info

class TargetAuthor(object):
    def __init__(self, dic_info = {}):
        self.platform = dic_info.get("platform", "")
        self.content_category = dic_info.get('content_category', "")
        self.author = dic_info.get('author', "")
        self.is_scrawl = dic_info.get('is_scrawl', False)
        self.last_scrawl_time = dic_info.get('last_scrawl_time', "")
        self.subscribe_link = dic_info.get('subscribe_link', "")
        self.is_scrawl_success = dic_info.get('is_scrawl_success', False)
        self.fail_reason = dic_info.get('fail_reason', "")

    def convert_to_json(self):
        dic_info = {
            "platform": self.platform,
            "content_category": self.content_category,
            "author": self.author,
            "is_scrawl": self.is_scrawl,
            "last_scrawl_time": self.last_scrawl_time,
            "subscribe_link": self.subscribe_link,
            "is_scrawl_success": self.is_scrawl_success,
            "fail_reason": self.fail_reason
            
        }
        return dic_info



class TaskInfo(object):
    def __init__(self, dic_info):
        self.task_name = dic_info.get("task_name", "")
        self.platform = dic_info.get("platform", "")

    def convert_to_json(self):
        dic_info = {
            "task_name": self.task_name,
            "platform": self.platform
        }
        return dic_info

class GenerateArticle(object):
    def __init__(self, dic_info={}):
        self.generate_title = dic_info.get("generate_title", "")
        self.generate_content = dic_info.get("generate_content", "")
        self.gen_date_hour = dic_info.get("gen_date_hour", "")
        self.format_content = dic_info.get("format_content", "")
        self.is_publish_success = dic_info.get("is_publish_success", False)


    def convert_to_json(self):
        dic_info = {
            "generate_title": self.generate_title,    
            "generate_content": self.generate_content,
            "gen_date_hour": self.gen_date_hour,
            "format_content": self.format_content,
            "is_publish_success": self.is_publish_success
        }
        return dic_info

class PublicArticle(object):
    def __init__(self, dic_info={}):
        self.account_name = dic_info.get('account_name', '') 
        self.platform = dic_info.get('platform', '')

    def convert_to_json(self):
        dic_info = {
            "account_name": self.account_name,
            "platform": self.platform,
        }
        return dic_info
