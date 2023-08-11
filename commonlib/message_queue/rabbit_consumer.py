#encoding=utf-8
import rabbitpy
# url = 'amqp://admin:123456@localhost:5672/%2F'
#url = 'amqp://admin:123456@23.251.52.227:5672/%2F'
url = 'amqp://admin2:ydl1qaw32@23.251.52.227:5672/%2F'
#conn = rabbitpy.Connection('admin', '123456')
conn = rabbitpy.Connection(url)

channel = conn.channel()

queue = rabbitpy.Queue(channel, 'example')
import time


while len(queue)>0:
    message = queue.get()
    time.sleep(2)

    print("message:", message.properties['message_id'], message.body)

    message.ack()

