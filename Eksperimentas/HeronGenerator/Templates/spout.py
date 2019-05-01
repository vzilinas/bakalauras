# Import spout type from heronpy
from heronpy.api.spout.spout import Spout
from kafka import KafkaConsumer

# KafkaInputSpout class that inherits from heron Spout
class KafkaInputSpout(Spout):
    # Important : Define output field tags for the Spout
    outputs = ["<%SpoutOutputs%>"]

    # Spout initialization
    def initialize(self, config, context):
        # A log context is provided in the context of the spout
        self.logger.info("Initializing KafkaInputSpout, versionId - <%VersionId%>")
        self.consumer = KafkaConsumer("<%KafkaQueue%>", bootstrap_servers="localhost:9092")

    # Generate next tuple sequence for this spout
    def next_tuple(self):
        for msg in self.consumer:
            message = msg.value
            self.logger.info([message])
            self.emit([message])
            self.logger.info("Emit success!")

    def ack(self, tup_id):
        self.logger.info("Ackquired!")