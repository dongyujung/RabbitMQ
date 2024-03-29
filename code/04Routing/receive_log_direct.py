#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# Let the server choose a random queue name
# by supplying empty queue parameter
# Once consumer connection is closed, the queue should be deleted: exclusive=True
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Binding
severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')

# Whenever we receive a message,
# this callback function is called by the Pika library.
def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

# Receive messages from queue.
channel.basic_consume(queue=queue_name,
                      on_message_callback=callback,
                      auto_ack=True)

channel.start_consuming()