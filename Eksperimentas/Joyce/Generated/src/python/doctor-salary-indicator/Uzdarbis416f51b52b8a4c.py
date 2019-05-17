# Import Bolt type from heronpy
from heronpy.api.bolt.bolt import Bolt
from heronpy.api.state.stateful_component import StatefulComponent
import msgpack
import redis
import helpers
import pickle
import json

# class that inherits from heron Bolt
class Uzdarbis416f51b52b8a4c(Bolt, StatefulComponent):
    # Important : Define output field tags for the Bolt
    outputs = ["Uzdarbis_416f51b5-2b8a-4cb0-9978-f713d5990c52", "unique_id"]

    def init_state(self, stateful_state):
        self.recovered_state = stateful_state
        self.logger.info("Checkpoint Snapshot recovered")

    def pre_save(self, checkpoint_id):
        self.logger.info("Checkpoint Snapshot %s" % (checkpoint_id))

    def initialize(self, config, context):
        # A log context is provided in the context of the spout
        self.log("Initializing Uzdarbis416f51b52b8a4c...")
        self.results = {
			'Gydytojas_2019' : {
			    'Count' : 135,
			    'Sum' : 125914.55,
			},
			'Programuotojas_2017' : {
			    'Count' : 141,
			    'Sum' : 141473.51,
			},
			'Filosofas_2019' : {
			    'Count' : 127,
			    'Sum' : 119069.38,
			},
			'Gydytojas_2017' : {
			    'Count' : 161,
			    'Sum' : 167278.72,
			},
			'Filosofas_2017' : {
			    'Count' : 119,
			    'Sum' : 114872.74,
			},
			'Programuotojas_2018' : {
			    'Count' : 133,
			    'Sum' : 135190.01,
			},
			'Programuotojas_2019' : {
			    'Count' : 122,
			    'Sum' : 121465.5,
			},
			'Gydytojas_2018' : {
			    'Count' : 128,
			    'Sum' : 124336.85,
			},
			'Filosofas_2018' : {
			    'Count' : 123,
			    'Sum' : 125692.41,
			},

        }
        self.temp_combination = {}
        self.redis_db = redis.Redis(host='localhost', port=6379, db=0)

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
            if not({'Atlyginimasc5df16a0679a', 'Atostoginiai49e661dd1d6'} <= set(self.temp_combination[input_dict['unique_id']])):
                return

        input_value = self.temp_combination[output_dict['unique_id']]['Atlyginimasc5df16a0679a']['last_value'] + self.temp_combination[output_dict['unique_id']]['Atostoginiai49e661dd1d6']['last_value']
        if output_dict['unique_id'] in self.temp_combination:
            self.temp_combination.pop(output_dict['unique_id'])

        if output_dict['primary_key'] in self.results:
            self.results[output_dict['primary_key']]['Sum'] += input_value
            self.results[output_dict['primary_key']]['Count'] += 1
        else:
            self.results[output_dict['primary_key']] = {}
            self.results[output_dict['primary_key']]['Sum'] = input_value
            self.results[output_dict['primary_key']]['Count'] = 1

        result = {
            "Mean" : helpers.calculate_mean(self.results[output_dict['primary_key']]['Sum'], self.results[output_dict['primary_key']]['Count']),
            "Sum" : self.results[output_dict['primary_key']]['Sum'],
            "Count" : self.results[output_dict['primary_key']]['Count'],
            "last_value" : input_value 
        }
        output_dict['result']['Uzdarbis416f51b52b8a4c'] = result
        self.emit([pickle.dumps(output_dict), output_dict['unique_id']])
        self.redis_db.sadd('doctor-salary-indicator:Uzdarbis416f51b52b8a4c:state_values', output_dict['primary_key'])
        self.redis_db.set('doctor-salary-indicator:Uzdarbis416f51b52b8a4c:' + output_dict['primary_key'], msgpack.packb(self.results[output_dict['primary_key']]))
        self.logger.info("Emited:" + json.dumps(output_dict))