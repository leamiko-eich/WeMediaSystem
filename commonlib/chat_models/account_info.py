#encoding=utf-8

class AccountInfo(object):
    def __init__(self, dic_info={}):
        self.row_id = dic_info.get('row_id', '')
        self.account = dic_info.get("account", "")
        self.platform = dic_info.get("platform", "")
        self.token = dic_info.get("token", "")
        self.status = dic_info.get("status", "")

        self.total_cnt = dic_info.get("total_cnt", 0)
        if self.total_cnt == "":
            self.total_cnt = 0
        else:
            self.total_cnt = int(self.total_cnt)

        self.total_succ_cnt = dic_info.get("total_succ_cnt", 0)
        if self.total_succ_cnt == "":
            self.total_succ_cnt = 0
        else:
            self.total_succ_cnt = int(self.total_succ_cnt)

        self.total_fail_cnt = dic_info.get("total_fail_cnt", 0)
        if self.total_fail_cnt == "":
            self.total_fail_cnt = 0
        else:
            self.total_fail_cnt = int(self.total_fail_cnt)  

        self.today_succ_cnt = dic_info.get("today_succ_cnt", 0)
        if self.today_succ_cnt == "":
            self.today_succ_cnt = 0
        else:
            self.today_succ_cnt = int(self.today_succ_cnt)  

        self.today_fail_cnt = dic_info.get("today_fail_cnt", 0)
        if self.today_fail_cnt == "":
            self.today_fail_cnt = 0
        else:
            self.today_fail_cnt = int(self.today_fail_cnt)
        self.last_call_time = dic_info.get("last_call_time", "")

        self.statuscode_call_chatmodel = 0
        self.last_status = ""
        self.error_msg = ""

        self.chat_model = None
        self.ai_response = ""

    def set_ai_response(self, response):
        self.ai_response = response

    def set_last_status(self, status):
        self.last_status = status

    def set_status_code_call_chatmodel(self, status):
        self.statuscode_call_chatmodel = status

    def set_error_msg(self, msg):   
        self.error_msg = msg

    def set_chat_model(self, chat_model):
        self.chat_model = chat_model

    def __str__(self):
        return "row_id:%s platform:%s token:%s" % (self.row_id, self.platform, self.token)  
