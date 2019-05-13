from kafka import KafkaProducer
import time
import json
import string

producer = KafkaProducer(bootstrap_servers='localhost:9092')

with open('doctor-salary-indicator-data.json') as json_file:  
    data = json.load(json_file)
    for x in data:
        time.sleep(.100)
        json_data = json.dumps(x).encode('utf-8')
        print(json_data)
        producer.send('statistics-queue', json_data)
	