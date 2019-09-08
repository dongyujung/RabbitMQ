#!/usr/bin/env python
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

# Receiving messages from the queue works by subscribing a callback function to a queue.
# Whenever we receive a message, this callback function is called by the Pika library.
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

# Don't dispatch a new message to a worker until it has processed and acknowledged the previous one.
channel.basic_qos(prefetch_count=1)

# receive messages from queue.
channel.basic_consume(queue='task_queue',
                      on_message_callback=callback)

# A never-ending loop that waits for data and runs callbacks whenever necessary.
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()