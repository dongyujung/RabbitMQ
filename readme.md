# Asynchronous Messaging with RabbitMQ  

### Reference  
https://www.rabbitmq.com/tutorials  

## Introduction  

RabbitMQ is a message broker: it accepts and forwards messages.   

- A **producer**: a user application that sends messages.  
- A **queue**: a buffer that stores messages.    
- A **consumer**: a user application that receives messages.     

You may wish to see what queues RabbitMQ has and how many messages are in them. You can do it (as a privileged user) using the rabbitmqctl tool:

```
sudo rabbitmqctl list_queues
```
On Windows, omit the sudo:
```
rabbitmqctl.bat list_queues
```

## Work Queues  

Distribute time-consuming tasks among multiple workers.  
Avoid doing a resource-intensive task immediately and having to wait for it to complete.  
We encapsulate a task as a message and send it to the queue.  
A worker process running in the background will pop the tasks and eventually execute the job. When you run many workers the tasks will be shared between them.  
= Task Queues  

#### Round-robin dispatching
One of the advantages of using a Task Queue is the ability to easily **parallelise** work. If we are building up a backlog of work, we can just add more workers and that way, scale easily.  

By default, RabbitMQ will **send each message to the next consumer**, in sequence. On average every consumer will get the same number of messages. This way of distributing messages is called round-robin.  

#### Message acknowledgement  
Once RabbitMQ delivers message to the consumer it immediately marks it for deletion. In this case, if you kill a worker we will lose the message it was just processing. But we don't want to lose any tasks. If a worker dies, we'd like the task to be delivered to another worker.  

An **ack(nowledgement)** is sent back by the consumer to tell RabbitMQ that a particular message had been received, processed and that RabbitMQ is free to delete it.    

If a consumer dies without sending an ack, RabbitMQ will will re-queue it. If there are other consumers online at the same time, it will then quickly redeliver it to another consumer.   

Manual message acknowledgements are turned on by default via `auto_ack=False`.  

#### Message durability  

Two things are required to make sure that messages aren't lost: we need to mark **both the queue and messages as durable**.  

```
channel.queue_declare(queue='task_queue', durable=True)

channel.basic_publish(exchange='',
                      routing_key="task_queue",
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
```

#### Fair Dispatch  

Instead of blindly dispatching every n-th message to the n-th consumer, don't dispatch a new message to a worker until it has processed and acknowledged the previous one.  

```
channel.basic_qos(prefetch_count=1)
```

## Publish / Subscribe  

Deliver a message to multiple consumers/queues.  

The core idea in the messaging model in RabbitMQ is that the producer never sends any messages directly to a queue. Instead, the producer can only send messages to an **exchange**.  

#### Exchange  
The producer can only send messages to an exchange.  
One side: receives messages from producers.    
Other side: push messages to queues.  

Exchange types: direct, topic, headers, fanout.  

fanout: broadcasts all the messages it receives to all the queues it knows.  

#### Temporary queues  

- Let the server choose a random queue name, and create a fresh, empty queue.  
- Once the consumer connection is closed, the queue should be deleted.  

#### Bindings  

The relationship between exchange and a queue is called a binding.    

#### Direct Exchange  

Match `Binding key of Queue` - `Routing key of Message`      

#### Multiple Bindings  

It is perfectly legal to bind multiple queues with the same binding key.    













