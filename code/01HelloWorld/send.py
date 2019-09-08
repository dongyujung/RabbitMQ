#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')    # Name of queue is 'hello'

# In RabbitMQ a message can never be sent directly to the queue,
# it always needs to go through an exchange.
# Name of exchange: ''
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

connection.close()