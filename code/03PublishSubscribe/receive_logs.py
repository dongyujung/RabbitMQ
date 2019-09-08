#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Let the server choose a random queue name
# by supplying empty queue parameter
# Once consumer connection is closed, the queue should be deleted: exclusive=True
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Binding
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

# Whenever we receive a message,
# this callback function is called by the Pika library.
def callback(ch, method, properties, body):
    print(" [x] %r" % body)

# Receive messages from queue.
channel.basic_consume(queue=queue_name,
                      on_message_callback=callback,
                      auto_ack=True)

channel.start_consuming()