#encoding=utf-8
import rabbitpy
import time
import json
import signal
from .MsgConstDict import dic_ex_queue_route

is_interrupted = False
def signal_handler(sig, frame):
    print("接受到ctrl-c信号 -1")
    global is_interrupted
    is_interrupted = True

signal.signal(signal.SIGINT, signal_handler)

class MsgConsumer(object):
    def __init__(self, name_exchange='test_change', name_queue='test_queue', name_route_key='test_route_key', key_ex_queue_route=""):
        self.rabbit_url = 'amqp://admin2:ydl1qaw32@23.251.52.227:5672/%2F'

        self.name_exchange = name_exchange
        self.name_queue = name_queue
        self.route_key = name_route_key

        if key_ex_queue_route!="":
            assert key_ex_queue_route in dic_ex_queue_route
            kv = dic_ex_queue_route[key_ex_queue_route]
            self.name_exchange = kv["name_exchange"]
            self.name_queue = kv["name_queue"]
            self.route_key = kv["name_route_key"]

        print("key:%s ex:%s queue:%s route:%s"%(key_ex_queue_route, self.name_exchange, self.name_queue, self.route_key))


    # Callback function to process received messages
    def process_message(self, message, callback, debug=False):
        # Process the message as needed
        # message : rabbitpy.Message = message
        # print("mesg type:", type(message))
        # print("Received message type:%s  body:" % (message.content_type), message.body)
        # if message.content_type == 'application/json':
        dic_data = json.loads(message.body.decode())
        callback(dic_data)

        if debug: return

        # Acknowledge the message to remove it from the queue
        message.ack()
    
    def consumer_msg_list(self, callback=None, use_consumer=False, debug=False):
        #conn = rabbitpy.Connection('admin', '123456')
        with rabbitpy.Connection(self.rabbit_url) as conn:
            with conn.channel() as channel:

                queue = rabbitpy.Queue(channel, self.name_queue)

                if use_consumer:
                    for message in queue:
                        if is_interrupted:
                            print("接受到ctrl-c信号")
                            break
                        self.process_message(message, callback, debug=debug)
                        if debug: break

                else:
                    while len(queue)>0:
                        if is_interrupted:
                            print("接受到ctrl-c信号")
                            break
                        message = queue.get()
                        self.process_message(message, callback, debug=debug)
                        if debug: break

                        
    def func_call_back(self, dic_data):
        print(1111)
        print(dic_data)

    def test_call_back(self):
        self.consumer_msg_list(self.func_call_back, use_consumer= False, debug=True)
        # self.consumer_msg_list(self.func_call_back, use_consumer= False, debug=False)





        

    def start_flow(self):
        msg_list = ['msg_%d'%(i) for i in range(30)]
        self.test_call_back()

        # self.consumer_msg_list()
        

if __name__ == "__main__":
    obj_consumer = MsgConsumer( name_queue='QueueInsertDb')
    obj_consumer.start_flow()