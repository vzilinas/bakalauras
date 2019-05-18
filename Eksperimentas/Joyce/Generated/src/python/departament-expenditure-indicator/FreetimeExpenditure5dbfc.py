# Import Bolt type from heronpy
from heronpy.api.bolt.bolt import Bolt
from heronpy.api.state.stateful_component import StatefulComponent
import msgpack
import redis
import helpers
import pickle
import json

# class that inherits from heron Bolt
class FreetimeExpenditure5dbfc(Bolt, StatefulComponent):
    # Important : Define output field tags for the Bolt
    outputs = ["FreetimeExpenditure_5dbfcf52-bbce-4ec6-ad31-1cf0812b3106", "unique_id"]

    def init_state(self, stateful_state):
        self.recovered_state = stateful_state
        self.logger.info("Checkpoint Snapshot recovered")

    def pre_save(self, checkpoint_id):
        self.logger.info("Checkpoint Snapshot %s" % (checkpoint_id))

    def initialize(self, config, context):
        # A log context is provided in the context of the spout
        self.log("Initializing FreetimeExpenditure5dbfc...")
        self.results = {

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
            if not({'TembuildingSpending65c89', 'PizzaFridayExpense117af4', 'TeamSize58f7d6476c1e45'} <= set(self.temp_combination[input_dict['unique_id']])):
                return

        input_value = (self.temp_combination[output_dict['unique_id']]['TembuildingSpending65c89']['last_value'] / self.temp_combination[output_dict['unique_id']]['TeamSize58f7d6476c1e45']['last_value']) + self.temp_combination[output_dict['unique_id']]['PizzaFridayExpense117af4']['last_value']
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
        output_dict['result']['FreetimeExpenditure5dbfc'] = result
        self.emit([pickle.dumps(output_dict), output_dict['unique_id']])
        self.redis_db.sadd('departament-expenditure-indicator:FreetimeExpenditure5dbfc:state_values', output_dict['primary_key'])
        self.redis_db.set('departament-expenditure-indicator:FreetimeExpenditure5dbfc:' + output_dict['primary_key'], msgpack.packb(self.results[output_dict['primary_key']]))
        self.logger.info("Emited:" + json.dumps(output_dict))