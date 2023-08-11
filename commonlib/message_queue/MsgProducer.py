#encoding=utf-8
import rabbitpy
import json
import pickle
try:
    from .MsgConstDict import dic_ex_queue_route
except Exception as e:
    from mygpt.async_chat_system.MsgConstDict import dic_ex_queue_route 


class MsgProducer(object):
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

    
    def produce_msg_list(self, msg_list=[]):
        #conn = rabbitpy.Connection('admin', '123456')
        with rabbitpy.Connection(self.rabbit_url) as conn:
            with conn.channel() as channel:
                exchange = rabbitpy.Exchange(channel, self.name_exchange)
                exchange.declare()

                queue = rabbitpy.Queue(channel, self.name_queue)
                queue.declare()
                queue.bind(exchange, self.route_key)

                for nid,msg_info in enumerate(msg_list):
                    message = rabbitpy.Message(channel, msg_info
                                               )
                    message.publish(exchange, self.route_key)

                    # print("id:", message.properties['message_id'], message.body)


        

    def start_flow(self):
        msg_list = ['msg_%d'%(i) for i in range(30)]

        dic_tmp = {"name": "123"}
        msg_list = []
        for i in range(5):
            msg_list.append( json.dumps(dic_tmp))

        self.produce_msg_list(msg_list)
        

if __name__ == "__main__":
    obj_producer = MsgProducer()

    obj_producer = MsgProducer(name_exchange="ExRecallArt", name_queue="QueueInsertDb", name_route_key="RouteRecall2Insert")
    obj_producer.start_flow()