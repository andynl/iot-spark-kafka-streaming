#!/usr/bin/python3

from kafka import KafkaProducer
from sys import argv
import numpy as np
from time import time, sleep
import json

DEVICE_PROFILES = {
    "jkt": {'temp': (51.3, 17.7), 'humd': (77.4, 18.7), 'pres': (1019.9, 9.5) },
    "bdg": {'temp': (49.5, 19.3), 'humd': (33.0, 13.9), 'pres': (1012.0, 41.3) },
    "jog": {'temp': (63.9, 11.7), 'humd': (62.8, 21.8), 'pres': (1015.9, 11.3) },
}

if len(argv) != 2 or argv[1] not in DEVICE_PROFILES.keys():
    print("Please provide a valid device name:")
    for key in DEVICE_PROFILES.keys():
        print(f" * {key}")
    print(f"\nformat: {argv[0]} DEVICE_NAME")
    exit(1)
        
profile_name = argv[1]
profile = DEVICE_PROFILES[profile_name]

producer = KafkaProducer(bootstrap_servers='localhost:9092')

count = 1

while True:
    temp = np.random.normal(profile['temp'][0], profile['temp'][1])
    humd = np.random.normal(profile['humd'][0], profile['humd'][1])
    pres = np.random.normal(profile['pres'][0], profile['pres'][1])

    data = {
        "time": time(),
        "device": profile_name,
        "temp": temp,
        "humd": humd,
        "pres": pres
    }
    
    producer.send('sensors', json.dumps(data).encode('utf-8'))
    print(f'sending data to kafka, #{count}')

    count += 1
    sleep(.5)