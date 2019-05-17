# Import Bolt type from heronpy
from heronpy.api.bolt.bolt import Bolt
from heronpy.api.state.stateful_component import StatefulComponent
import msgpack
import redis
import helpers
import pickle
import json

# class that inherits from heron Bolt
class LoterijosLaimejimaid0550(Bolt, StatefulComponent):
    # Important : Define output field tags for the Bolt
    outputs = ["LoterijosLaimejimai_d05508c3-0549-499d-be01-7c25fd2b3e95", "unique_id"]

    def init_state(self, stateful_state):
        self.recovered_state = stateful_state
        self.logger.info("Checkpoint Snapshot recovered")

    def pre_save(self, checkpoint_id):
        self.logger.info("Checkpoint Snapshot %s" % (checkpoint_id))

    def initialize(self, config, context):
        # A log context is provided in the context of the spout
        self.log("Initializing LoterijosLaimejimaid0550...")
        self.results = {
			'Gydytojas_2019' : {
			    'Count' : 134,
			    'Sum' : 68861.69,
			},
			'Programuotojas_2017' : {
			    'Count' : 141,
			    'Sum' : 71702.85,
			},
			'Filosofas_2019' : {
			    'Count' : 125,
			    'Sum' : 73096.76,
			},
			'Gydytojas_2017' : {
			    'Count' : 158,
			    'Sum' : 72783.2,
			},
			'Filosofas_2017' : {
			    'Count' : 119,
			    'Sum' : 57530.49,
			},
			'Programuotojas_2018' : {
			    'Count' : 132,
			    'Sum' : 70283.03,
			},
			'Programuotojas_2019' : {
			    'Count' : 122,
			    'Sum' : 59188.4,
			},
			'Gydytojas_2018' : {
			    'Count' : 127,
			    'Sum' : 67228.87,
			},
			'Filosofas_2018' : {
			    'Count' : 123,
			    'Sum' : 63681.02,
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
        if False:
            if output_dict['unique_id'] in self.temp_combination:
                self.temp_combination[output_dict['unique_id']] = helpers.merge_two_dicts(self.temp_combination[output_dict['unique_id']], input_dict['result'])
            else:
                self.temp_combination[output_dict['unique_id']] = input_dict['result']
            if not({'empty'} <= set(self.temp_combination[input_dict['unique_id']])):
                return

        input_value = input_dict['data']['LoterijosLaimejimai']
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
        output_dict['result']['LoterijosLaimejimaid0550'] = result
        self.emit([pickle.dumps(output_dict), output_dict['unique_id']])
        self.redis_db.sadd('doctor-salary-indicator:LoterijosLaimejimaid0550:state_values', output_dict['primary_key'])
        self.redis_db.set('doctor-salary-indicator:LoterijosLaimejimaid0550:' + output_dict['primary_key'], msgpack.packb(self.results[output_dict['primary_key']]))
        self.logger.info("Emited:" + json.dumps(output_dict))