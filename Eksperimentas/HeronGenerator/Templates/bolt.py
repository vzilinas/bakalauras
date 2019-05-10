# Import Bolt type from heronpy
from heronpy.api.bolt.bolt import Bolt
import helpers

# class that inherits from heron Bolt
class <%BoltName%>(Bolt):
    # Important : Define output field tags for the Bolt
    outputs = ["<%BoltOutputs%>"]
    count = 0
    total = 0
    lowers, highers = [], []
    mode_dict = {}
    temp_combination = {}

    def initialize(self, config, context):
        # A log context is provided in the context of the spout
        self.log("Initializing <%BoltName%>...")

    # Process incoming tuple and emit output
    def process(self, tup):
        self.logger.info("Incoming" + tup)
        input_dict = tup.values[0]
        self.logger.info("Caught raw data:" + input_dict)
        if <%Combined%>:
            temp_combination[input_dict['uniqueId']] = {input_dict['result'][tup.stream] : input_dict['result'][tup.stream]['last_value']}
            if !({<%CombinedCheck%>} <= set(temp_combination[input_dict['uniqueId']])):
                return
        input_value = <%InputValue%>
        total += input_value
        count += 1
        result = {
            "Mean" : helpers.calculate_mean(total, count),
            "Median" : helpers.calculate_median(input_value, lowers, highers),
            "Mode" : helpers.calculate_mode(input_value, mode_dict),
            "Sum" : total,
            "Count" : count,
            "last_value" : input_value 
        }
        input_dict['result']['<%BoltName%>'] = result
        self.emit([input_dict])
