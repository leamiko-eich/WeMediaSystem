import openai
import random
import time
import logging

from chat_models.base_chat_model import BaseChatModel


def total_counts(response):    
    
    #计算本次任务花了多少钱和多少tokens：
    tokens_nums = int(response['usage']['total_tokens']) #计算一下token的消耗
    price = 0.002/1000 #根据openai的美元报价算出的token美元单价
    人民币花费 = '{:.5f}'.format(price * tokens_nums * 7.5)
    合计内容 = f'本次对话共消耗了{tokens_nums}个token，花了{人民币花费}元（人民币）'
    # print(合计内容)

    return float(人民币花费)

class GptChat(BaseChatModel):
    def __init__(self, in_token = None, conversation_list=[]) -> None:
        super().__init__()
        logging.info("当前使用的是GPT-3.5-turbo模型")
        # 初始化对话列表，可以加入一个key为system的字典，有助于形成更加个性化的回答
        # self.conversation_list = []  # 初始化对话列表
        self.costs_list = [] # 初始化聊天开销列表
        self.answer_list = []
        self.input_token = in_token

        self.total_cost = 0
        self.wait_time = 15
        
            
    # 打印对话
    def show_conversation(self,msg_list):
        for msg in msg_list[-2:]:
            if msg['role'] == 'user': # 如果是用户的话
                #print(f"\U0001f47b: {msg['content']}\n")
                pass
            else: # 如果是机器人的话
                message = msg['content']
                print(f"\U0001f47D: {message}\n")                
            print()

    # 调用chatgpt，并计算开销
    def ask(self,prompt):
        init_content = "你是一个文案高手"
        self.conversation_list = [{'role':'system','content': init_content}]

        self.conversation_list.append({"role":"user","content":prompt})
        # openai.api_key = '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'
        # openai.api_key = "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"
        openai.api_key = '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'
        if self.input_token is not None:
            openai.api_key = self.input_token
        logging.info("本次使用token:%s " % (openai.api_key))
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=self.conversation_list)
        answer = response.choices[0].message['content']
        # 下面这一步是把chatGPT的回答也添加到对话列表中，这样下一次问问题的时候就能形成上下文了
        # self.conversation_list.append({"role":"assistant","content":answer})

        self.answer_list.append(answer)

        monney = total_counts(response)
        self.costs_list.append(monney)
        self.total_cost += monney

        logging.info("[gpt等待 %s 秒]" % (self.wait_time))
        time.sleep(self.wait_time)

        
class Chat(GptChat):
    def __init__(self, conversation_list=[]) -> None:
        super().__init__(conversation_list)



        
def main():
    
    talk = Chat()
    print()

    count = 0
    count_limit = eval(input("你想要对话的次数是多少呢？\n(请输入数字即可)"))		
    while count<count_limit: #上下文token数量是有极限的，理论上只能支持有限轮次的对话，况且，钱花光了也就不能用了。。。
        if count<1: 
            words = input("请问有什么可以帮助你的呢？\n(请输入您的需求或问题)：")
        else:
            words = input("您还可以继续与我交流，请您继续说：\n(请输入您的需求或问题)：")
        print()
        talk.ask(words)
        count += 1
    
    print(f'本轮聊天合计花费{sum(talk.costs_list)}元人民币。')

if __name__ == "__main__":
    main()
    # obj_chat
