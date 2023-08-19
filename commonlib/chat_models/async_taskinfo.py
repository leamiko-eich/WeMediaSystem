#encoding=utf-8

# from mygpt.chat_models.async_taskinfo  import AsyncTaskInfo2

class AsyncTaskinfo(object):
    def __init__(self, dic_info = {}):
        self.task_row_id = dic_info.get("task_row_id", "")
        self.row_id = dic_info.get("row_id", "")
        self.task_status = dic_info.get("task_status", "")
        self.create_ts = dic_info.get("create_ts", "")
        self.create_dt_hour = dic_info.get("create_dt_hour", "")
        self.task_title = dic_info.get("task_title", "")
        self.prompt = dic_info.get("prompt", "")
        self.content = dic_info.get("content", "")
        self.md5_id = dic_info.get("md5_id", "")
        self.target_column = dic_info.get("target_column", "")
        self.art_title = dic_info.get("art_title", "")
        self.ai_response = dic_info.get("ai_response", "")
        self.target_status_column = dic_info.get("target_status_column", "")

    def set_ai_response(self, response):
        self.ai_response = response