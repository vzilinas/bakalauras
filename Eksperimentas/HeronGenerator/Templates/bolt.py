# Import Bolt type from heronpy
from heronpy.api.bolt.bolt import Bolt
import helpers
import pickle
import json

# class that inherits from heron Bolt
class <%BoltName%>(Bolt):
    # Important : Define output field tags for the Bolt
    outputs = ["<%BoltOutputs%>"]


    def initialize(self, config, context):
        # A log context is provided in the context of the spout
        self.log("Initializing <%BoltName%>...")
        self.count = 0
        self.total = 0
        self.lowers, self.highers = [], []
        self.mode_dict = {}
        self.temp_combination = {}

    # Process incoming tuple and emit output
    def process(self, tup):
        self.logger.info("Incoming")
        input_dict = pickle.loads(tup.values[0])
        self.logger.info("Caught raw data:" + json.dumps(input_dict))
        output_dict = {
                'primary_key' : input_dict['primary_key'],
                'primary_key_array' : input_dict['primary_key_array'],
                'unique_id' : input_dict['unique_id'],
                'result' : {}
            }
        if <%Combined%>:
            if input_dict['unique_id'] in self.temp_combination:
                self.temp_combination[input_dict['unique_id']] = helpers.merge_two_dicts(self.temp_combination[input_dict['unique_id']], input_dict['result'])
            else:
                self.temp_combination[input_dict['unique_id']] =  input_dict['result']
            if not({<%CombinedCheck%>} <= set(self.temp_combination[input_dict['unique_id']])):
                return
            else:
                output_dict['result'] = self.temp_combination[input_dict['unique_id']]
                self.temp_combination.pop(input_dict['unique_id'])
            
        input_value = <%InputValue%>
        self.total += input_value
        self.count += 1
        result = {
            "Mean" : helpers.calculate_mean(self.total, self.count),
            "Median" : helpers.calculate_median(input_value, self.lowers, self.highers),
            "Mode" : helpers.calculate_mode(input_value, self.mode_dict),
            "Sum" : self.total,
            "Count" : self.count,
            "last_value" : input_value 
        }
        output_dict['result']['<%BoltName%>'] = result
        self.emit([pickle.dumps(output_dict)])
        self.logger.info("Emited:" + json.dumps(output_dict))