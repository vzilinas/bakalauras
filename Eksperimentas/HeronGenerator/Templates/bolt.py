# Import Bolt type from heronpy
from heronpy.api.bolt.bolt import Bolt

# PriceCalculationBolt class that inherits from heron Bolt
class <%BoltName%>(Bolt):
    # Important : Define output field tags for the Bolt
    outputs = ["<%BoltOutputs%>"]

    def initialize(self, config, context):
        # A log context is provided in the context of the spout
        self.log("Initializing <%BoltName%>, versionId <%VersionId%>...")

    # Process incoming tuple and emit output
    def process(self, tup):
        self.logger.info("Incoming" + tup)
        data = tup.values[0]
        self.logger.info("Caught raw data from spout:" + buy)

        <%BoltFunction%>

