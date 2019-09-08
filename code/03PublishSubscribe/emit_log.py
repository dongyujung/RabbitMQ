#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Exchange
channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:])

# Set up exchange
channel.basic_publish(
    exchange='logs',
    routing_key='',
    body=message
)
print(" [x] Sent %r" % message)

connection.close()