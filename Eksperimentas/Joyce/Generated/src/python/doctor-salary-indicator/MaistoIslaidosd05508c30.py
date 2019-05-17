# Import Bolt type from heronpy
from heronpy.api.bolt.bolt import Bolt
from heronpy.api.state.stateful_component import StatefulComponent
import helpers
import pickle
import json

# class that inherits from heron Bolt
class MaistoIslaidosd05508c30(Bolt, StatefulComponent):
    # Important : Define output field tags for the Bolt
    outputs = ["MaistoIslaidos_d05508c3-0549-499d-bc01-7c25fd2b3e95", "unique_id"]

    def init_state(self, stateful_state):
        self.recovered_state = stateful_state
        self.logger.info("Checkpoint Snapshot recovered")

    def pre_save(self, checkpoint_id):
        self.logger.info("Checkpoint Snapshot %s" % (checkpoint_id))

    def initialize(self, config, context):
        # A log context is provided in the context of the spout
        self.log("Initializing MaistoIslaidosd05508c30...")
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
        if True:
            if output_dict['unique_id'] in self.temp_combination:
                self.temp_combination[output_dict['unique_id']] = helpers.merge_two_dicts(self.temp_combination[output_dict['unique_id']], input_dict['result'])
            else:
                self.temp_combination[output_dict['unique_id']] = input_dict['result']
            if not({'SuvalgytasMaistasd05508c', 'IsmestasMaistasd05508c3'} <= set(self.temp_combination[input_dict['unique_id']])):
                return

        input_value = (self.temp_combination[output_dict['unique_id']]['SuvalgytasMaistasd05508c']['last_value'] * 0.9) + self.temp_combination[output_dict['unique_id']]['IsmestasMaistasd05508c3']['last_value']
        if output_dict['unique_id'] in self.temp_combination:
            self.temp_combination.pop(output_dict['unique_id'])

        if output_dict['primary_key'] in self.results:
            self.results[output_dict['primary_key']]['total'] += input_value
            self.results[output_dict['primary_key']]['count'] += 1
        else:
            self.results[output_dict['primary_key']] = {}
            self.results[output_dict['primary_key']]['total'] = input_value
            self.results[output_dict['primary_key']]['count'] = 1

        result = {
            "Mean" : helpers.calculate_mean(self.results[output_dict['primary_key']]['total'], self.results[output_dict['primary_key']]['count']),
            "Sum" : self.results[output_dict['primary_key']]['total'],
            "Count" : self.results[output_dict['primary_key']]['count'],
            "last_value" : input_value 
        }
        output_dict['result']['MaistoIslaidosd05508c30'] = result
        self.emit([pickle.dumps(output_dict), output_dict['unique_id']])
        self.logger.info("Emited:" + json.dumps(output_dict))