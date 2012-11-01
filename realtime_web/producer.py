#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pika
import logging
logging.basicConfig()


message = ' '.join(sys.argv[1:]) or "info: Hello World!"

cred = pika.PlainCredentials('guest', 'guest')
param = pika.ConnectionParameters(
    host='localhost',
    port=5672,
    virtual_host='/',
    credentials=cred
)

connection = pika.BlockingConnection(param)
channel = connection.channel()

#channel.exchange_declare(exchange='message', exchange_type='fanout ')
channel.basic_publish(exchange='message', routing_key='example.text', body=message)
connection.close()
