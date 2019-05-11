# Import Bolt type from heronpy
from heronpy.api.bolt.bolt import Bolt
import helpers
import pickle
import json

# class that inherits from heron Bolt
class Uzdarbis416f51b52b8a4c(Bolt):
    # Important : Define output field tags for the Bolt
    outputs = ["Uzdarbis_416f51b5-2b8a-4cb0-9978-f713d5990c52"]


    def initialize(self, config, context):
        # A log context is provided in the context of the spout
        self.log("Initializing Uzdarbis416f51b52b8a4c...")
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
        if True:
            if input_dict['unique_id'] in self.temp_combination:
                self.temp_combination[input_dict['unique_id']] = helpers.merge_two_dicts(self.temp_combination[input_dict['unique_id']], input_dict['result'])
            else:
                self.temp_combination[input_dict['unique_id']] =  input_dict['result']
            if not({'Atlyginimas_c5df16a0-679a-4756-93da-df87b278efca', 'Atostoginiai_49e661dd-1d6a-496e-bac5-22d4358145a9'} <= set(self.temp_combination[input_dict['unique_id']])):
                return
            else:
                output_dict['result'] = self.temp_combination[input_dict['unique_id']]
                self.temp_combination.pop(input_dict['unique_id'])
            
        input_value = output_dict['result']['Atlyginimas_c5df16a0-679a-4756-93da-df87b278efca']['last_value'] + output_dict['result']['Atostoginiai_49e661dd-1d6a-496e-bac5-22d4358145a9']['last_value']
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
        output_dict['result']['Uzdarbis416f51b52b8a4c'] = result
        self.emit([pickle.dumps(output_dict)])
        self.logger.info("Emited:" + json.dumps(output_dict))