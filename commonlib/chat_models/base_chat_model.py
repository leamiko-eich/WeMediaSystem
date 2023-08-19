#encoding=utf-8
class BaseChatModel(object):
    def __init__(self) -> None:
        self.answer_list = []

    def start_agent(self):
        pass
    
    def ask(self, prompt):
        pass

    def ask_by_promt_content(self, prompt, content):
        pass