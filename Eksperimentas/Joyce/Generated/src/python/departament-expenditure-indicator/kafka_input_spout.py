# Import spout type from heronpy
from heronpy.api.spout.spout import Spout
from heronpy.api.state.stateful_component import StatefulComponent
from kafka import KafkaConsumer
import uuid
import json
import pickle

# KafkaInputSpout class that inherits from heron Spout
class KafkaInputSpout(Spout, StatefulComponent):
    # Important : Define output field tags for the Spout
    outputs = ["SpoutOutput"]

    def init_state(self, stateful_state):
        self.recovered_state = stateful_state
        self.logger.info("Checkpoint Snapshot recovered")

    def pre_save(self, checkpoint_id):
        self.logger.info("Checkpoint Snapshot %s" % (checkpoint_id))
        
    # Spout initialization
    def initialize(self, config, context):
        # A log context is provided in the context of the spout
        self.logger.info("Initializing KafkaInputSpout")
        self.logger.info("IndicatorId - 32c24420-afbd-44fb-b045-ef72c48cb04e")
        self.logger.info("IndicatorName - departament-expenditure-indicator")
        self.logger.info("IndicatorVersion - 1-416f51b5-2b8a-4cb0-9978-f713d5990c52")
        self.consumer = KafkaConsumer("statistics-queue",  group_id='statistics-queue_group', bootstrap_servers="localhost:9092", value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    # Generate next tuple sequence for this spout
    def next_tuple(self):
        msg = next(self.consumer, {})
        if len(msg) != 0:
            input_dict = msg.value
            self.logger.info(input_dict)
            primary_key = str(input_dict['Department']) + '_' + str(input_dict['Year']) + '_' + str(input_dict['Month'])
            primary_key_array = [input_dict['Department'], input_dict['Year'], input_dict['Month']]
            if input_dict['Department'] != 'Administration':
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