#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Creating a queue using queue_declare is idempotent:
# we can run the command as many times as we like, and only one will be created.
channel.queue_declare(queue='hello')

# Receiving messages from the queue works by subscribing a callback function to a queue.
# Whenever we receive a message, this callback function is called by the Pika library.
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

# Tell RabbitMQ that this callback function should
# receive messages from our hello queue.
channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)

# A never-ending loop that waits for data and runs callbacks whenever necessary.
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()