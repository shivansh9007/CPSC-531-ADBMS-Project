#!/usr/bin/env python

import sys
from random import choice
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Producer
import numpy as np             
from sys import argv, exit
from time import time,sleep,ctime
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    args = parser.parse_args()

    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])

    producer = Producer(config)

   
    def delivery_callback(err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        else:
            print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
                topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))

    topic = "energy_consumption"
   
    mockUserId = [{
        'userId':12345434,
        'location':'Pune'
    },{
        'userId':30000045,
        'location': 'Fullerton'


    },
    {
        'userId':37648475,
        'location':'Los Angeles'
    },]
    maxUsagePer30Secs = .15
    count = 0
    #time = 1667260800
    #while time<1669852800:
    while True:
        for a in mockUserId:
            usage = np.random.uniform(0,maxUsagePer30Secs)
            msg = f'{int(time())},{a["userId"]},{usage},{a["location"]}'
            print(msg)
            producer.produce(topic, msg,str(a["userId"]), callback=delivery_callback)
            count += 1
            producer.poll(10000)
            producer.flush()

 