# Import Bolt type from heronpy
from heronpy.api.bolt.bolt import Bolt
from kafka import KafkaProducer
import json

# class that inherits from heron Bolt
class EmitterBolt(Bolt):
    # Important : Define output field tags for the Bolt
    outputs = ["KafkaLog"]

    def initialize(self, config, context):
        # A log context is provided in the context of the spout
        self.log("Initializing EmitterBolt...")
        self.producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'), 
                                        bootstrap_servers='localhost:9092')

    # Process incoming tuple and emit output
    def process(self, tup):
        self.logger.info("Incoming" + tup)
        input_dict = tup.values[0]
        self.logger.info("Caught raw data:" + input_dict)
        producer.send("<%IndicatorName%>", input_dict)
