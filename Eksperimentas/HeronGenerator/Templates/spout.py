# Import spout type from heronpy
from heronpy.api.spout.spout import Spout
from kafka import KafkaConsumer

# KafkaInputSpout class that inherits from heron Spout
class KafkaInputSpout(Spout):
    # Important : Define output field tags for the Spout
    outputs = ["SpoutOutput"]

    # Spout initialization
    def initialize(self, config, context):
        # A log context is provided in the context of the spout
        self.logger.info("Initializing KafkaInputSpout")
        self.logger.info("IndicatorId - <%IndicatorId%>")
        self.logger.info("IndicatorName - <%IndicatorName%>")
        self.logger.info("IndicatorVersion - <%IndicatorVersion%>")
        self.consumer = KafkaConsumer("<%KafkaQueue%>", bootstrap_servers="localhost:9092")

    # Generate next tuple sequence for this spout
    def next_tuple(self):
        for msg in self.consumer:
            input_dict = msg.value
            self.logger.info(input_dict)
            
            <%SpoutFilteredDict%>
                ouput_dict = {}
                ouput_dict["data"] = input_dict
                ouput_dict["result"] = {}
                self.emit([ouput_dict])

            self.logger.info("Emit success!")

    def ack(self, tup_id):
        self.logger.info("Ackquired!")