# Import Bolt type from heronpy
from heronpy.api.bolt.bolt import Bolt
import helpers
import pickle
import json

# class that inherits from heron Bolt
class IsmestasMaistasd05508c3(Bolt):
    # Important : Define output field tags for the Bolt
    outputs = ["IsmestasMaistas_d05508c3-0549-499d-bc01-7c25fd2b3e85"]


    def initialize(self, config, context):
        # A log context is provided in the context of the spout
        self.log("Initializing IsmestasMaistasd05508c3...")
        self.results = {}
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
        if False:
            if output_dict['unique_id'] in self.temp_combination:
                self.temp_combination[output_dict['unique_id']] = helpers.merge_two_dicts(self.temp_combination[output_dict['unique_id']], input_dict['result'])
            else:
                self.temp_combination[output_dict['unique_id']] = input_dict['result']
            if not({'empty'} <= set(self.temp_combination[input_dict['unique_id']])):
                return

        self.temp_combination.pop(output_dict['unique_id'])
        input_value = input_dict['data']['IsmestasMaistas']

        if output_dict['primary_key'] in self.results:
            self.results['primary_key']['total'] += input_value
            self.results['primary_key']['count'] += 1
        else:
            self.results['primary_key'] = {}
            self.results['primary_key']['total'] = input_value
            self.results['primary_key']['count'] = 1

        result = {
            "Mean" : helpers.calculate_mean(self.results['primary_key']['total'], self.results['primary_key']['count']),
            "Sum" : self.results['primary_key']['total'],
            "Count" : self.results['primary_key']['count'],
            "last_value" : input_value 
        }
        output_dict['result']['IsmestasMaistasd05508c3'] = result
        self.emit([pickle.dumps(output_dict)])
        self.logger.info("Emited:" + json.dumps(output_dict))