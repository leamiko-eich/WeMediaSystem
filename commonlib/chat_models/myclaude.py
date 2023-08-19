#encoding=utf-8
from claude import claude_client
from claude import claude_wrapper
try:
    from .base_chat_model import BaseChatModel
except  Exception as e:
    from base_chat_model import BaseChatModel


import logging

class MyClaudeChat(BaseChatModel):

    def __init__(self, in_token=None) -> None:
        super().__init__()
        ## emai: yangjiangfengthu@gmail.com
        logging.info("当前使用的是Claude模型")
        # self.SESSION_KEY = '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'
        self.SESSION_KEY = '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'
        if in_token is not None:
            self.SESSION_KEY = in_token
        self.claude_obj = None
        self.conversation_uuid = '85ef912a-7ca3-40dd-b7b6-2008ead96a55'
        self.current_day = "20230111"
        self.random_time_flag = "111"


    def start_agent(self):
        print("key:", self.SESSION_KEY)
        client = claude_client.ClaudeClient(self.SESSION_KEY)
        print("client:", client)

        organizations = client.get_organizations()
        print("org:", organizations)
        # You can omit passing in the organization uuid and the wrapper will assume
        # you will use the first organization instead.
        claude_obj = claude_wrapper.ClaudeWrapper(client, organization_uuid=organizations[0]['uuid'])
    

        topic_title = "新对话_%s" % (self.random_time_flag)
        conversation_uuid = claude_obj.start_new_conversation("New Conversation", topic_title)
        # assert conversation_uuid is not None
        # conversation_uuid = claude_obj.start_new_conversation("23343", topic_title)
        logging.info("topic_title:%s conversation_uuid: %s" % (topic_title, conversation_uuid))
        self.conversation_uuid = conversation_uuid

        
        conversation = claude_obj.rename_conversation(topic_title, conversation_uuid = conversation_uuid)


        claude_obj.set_conversation_context(conversation_uuid)

        # failed_deletions = claude_obj.delete_all_conversations()
        # assert len(failed_deletions) == 0

        self.claude_obj = claude_obj


    def ask_by_promt_content(self, prompt, content):
        path_save="data/attach.txt"
        with open(path_save, 'w', encoding='utf-8') as f:
            f.write(content)
        self.ask(prompt, path_save, using_attach=True)
    
    def ask(self, prompt, attach_file=None, using_attach=False):
        if using_attach:
            # This generates an attachment in the right format
            attachment = self.claude_obj.get_attachment(attach_file)
            response = self.claude_obj.send_message(prompt, attachments=[attachment],
                                    conversation_uuid = self.conversation_uuid)
            logging.info("response:%s" % (response))
        else:
            response = self.claude_obj.send_message(prompt )

        self.answer_list.append(response['completion'])

        
        self.claude_obj.delete_conversation(self.conversation_uuid)

    def delete_all_conversation(self):
        failed_deletions = self.claude_obj.delete_all_conversations()
        assert len(failed_deletions) == 0

        
if __name__=="__main__":
    obj_myclaude = MyClaudeChat()
    obj_myclaude.start_agent()
    prompt = '帮忙写一篇关于财经的文章，500字'
    obj_myclaude.ask(prompt)
    ans = obj_myclaude.answer_list[-1]
    print("ans:", ans)
    obj_myclaude.delete_all_conversation()