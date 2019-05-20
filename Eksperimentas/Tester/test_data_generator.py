from kafka import KafkaProducer
import time
import json
import string

producer = KafkaProducer(bootstrap_servers='192.168.0.100:9092')
with open('departament-expenditure-indicator-data.json') as json_file:  
    data = json.load(json_file)
    while True:
        for x in data:
            time.sleep(.001)
            json_data = json.dumps(x).encode('utf-8')
            print(json_data)
            producer.send('statistics-queue', json_data)
        print("rotation done")