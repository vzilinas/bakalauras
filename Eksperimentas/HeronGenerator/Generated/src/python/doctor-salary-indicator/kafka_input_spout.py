# Import spout type from heronpy
from heronpy.api.spout.spout import Spout
from kafka import KafkaConsumer
import uuid
import json
import pickle

# KafkaInputSpout class that inherits from heron Spout
class KafkaInputSpout(Spout):
    # Important : Define output field tags for the Spout
    outputs = ["SpoutOutput"]

    # Spout initialization
    def initialize(self, config, context):
        # A log context is provided in the context of the spout
        self.logger.info("Initializing KafkaInputSpout")
        self.logger.info("IndicatorId - 32c24420-afbd-44fb-b045-ef72c48cb04e")
        self.logger.info("IndicatorName - doctor-salary-indicator")
        self.logger.info("IndicatorVersion - 1-416f51b5-2b8a-4cb0-9978-f713d5990c52")
        self.consumer = KafkaConsumer("statistics-queue", bootstrap_servers="localhost:9092", value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    # Generate next tuple sequence for this spout
    def next_tuple(self):
        msg = next(self.consumer, {})
        if len(msg) != 0:
            input_dict = msg.value
            self.logger.info(input_dict)
            primary_key = str(input_dict['Sritis']) + '_' + str(input_dict['Metai'])
            primary_key_array = [input_dict['Sritis'], input_dict['Metai']]
            if input_dict['SutartiesTipas'] == 'TERMINUOTA' or input_dict['SutartiesTipas'] == 'LAIKINOJI':
                output_dict = {
                    "data" : input_dict,
                    "primary_key" : primary_key,
                    "primary_key_array" : primary_key_array,
                    "unique_id" : str(uuid.uuid4())
                }
                output_data = pickle.dumps(output_dict)  
                self.emit([output_data])
                self.logger.info("Emit success!:")

    def ack(self, tup_id):
        self.logger.info("Ackquired!")