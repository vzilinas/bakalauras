# Import Bolt type from heronpy
from heronpy.api.bolt.bolt import Bolt
import helpers

# class that inherits from heron Bolt
class Atostoginiai49e661dd1d6(Bolt):
    # Important : Define output field tags for the Bolt
    outputs = ["Atostoginiai_49e661dd-1d6a-496e-bac5-22d4358145a9"]
    count = 0
    total = 0
    lowers, highers = [], []
    mode_dict = {}
    temp_combination = {}

    def initialize(self, config, context):
        # A log context is provided in the context of the spout
        self.log("Initializing Atostoginiai49e661dd1d6...")

    # Process incoming tuple and emit output
    def process(self, tup):
        self.logger.info("Incoming" + tup)
        input_dict = tup.values[0]
        self.logger.info("Caught raw data:" + input_dict)
        output_dict = {
                'primary_key' : input_dict['primary_key'],
                'primary_key_array' : input_dict['primary_key_array'],
                'unique_id' : input_dict['unique_id'],
                'result' : {}
            }
        if False:
            temp_combination[input_dict['unique_id']] = helpers.merge_two_dicts(temp_combination[input_dict['unique_id']], input_dict['result'])
            if !({'empty'} <= set(temp_combination[input_dict['unique_id']])):
                return
            else:
                output_dict['result'] = temp_combination[input_dict['unique_id']]
                temp_combination.pop(input_dict['unique_id'])
        input_value = input_dict['data']['Atostoginiai']
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
        output_dict['result']['Atostoginiai49e661dd1d6'] = result
        self.emit([output_dict])
