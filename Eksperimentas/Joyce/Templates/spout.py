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
        self.logger.info("IndicatorId - <%IndicatorId%>")
        self.logger.info("IndicatorName - <%IndicatorName%>")
        self.logger.info("IndicatorVersion - <%IndicatorVersion%>")
        self.consumer = KafkaConsumer("<%KafkaQueue%>",  group_id='<%IndicatorName%>_group', bootstrap_servers="localhost:9092", value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    # Generate next tuple sequence for this spout
    def next_tuple(self):
        msg = next(self.consumer, {})
        if len(msg) != 0:
            input_dict = msg.value
            self.logger.info(input_dict)
            primary_key = <%PrimaryKey%>
            primary_key_array = [<%PrimaryKeyArray%>]
            <%SpoutFilteredDict%>
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