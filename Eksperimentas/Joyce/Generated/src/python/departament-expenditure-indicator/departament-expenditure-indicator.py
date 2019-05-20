# Import Grouping and TopologyBuilder from heronpy
from heronpy.api.stream import Grouping
from heronpy.api.topology import TopologyBuilder
import heronpy.api.api_constants as constants

# Import the defined Bolts and Spouts
from kafka_input_spout import KafkaInputSpout
from FreetimeExpenditure5dbfc import FreetimeExpenditure5dbfc
from TembuildingSpending65c89 import TembuildingSpending65c89
from PizzaFridayExpense117af4 import PizzaFridayExpense117af4
from TeamSize58f7d6476c1e45 import TeamSize58f7d6476c1e45
from BuisnessTripExpensesd055 import BuisnessTripExpensesd055
from BuisnessTripLivingCosta7 import BuisnessTripLivingCosta7
from BuisnessTripTravelCost25 import BuisnessTripTravelCost25
from BuisnessTripDailyAllowanc import BuisnessTripDailyAllowanc
from OfficeNeedsExpenses595da import OfficeNeedsExpenses595da
from EquipmentExpenses0a185e3 import EquipmentExpenses0a185e3
from MandatoryEquipmentExpense import MandatoryEquipmentExpense
from OptionalEquipmentExpense import OptionalEquipmentExpense
from WorkingPlaceCost98026c71 import WorkingPlaceCost98026c71

# from emitter_bolt import EmitterBolt
# from report_aggregation_bolt import ReportAggregationBolt

if __name__ == '__main__':
    # Define the topology name.
    builder = TopologyBuilder("departament-expenditure-indicator")

    # Start with the random sentence generator, create a reference and define a parallelism hint with par attribute
    kafka_input_spout = builder.add_spout("kafka_input_spout", KafkaInputSpout, par=10)

    tembuildingspending65c89_bolt = builder.add_bolt('tembuildingspending65c89', TembuildingSpending65c89, par=10, inputs = {kafka_input_spout : Grouping.SHUFFLE})
    pizzafridayexpense117af4_bolt = builder.add_bolt('pizzafridayexpense117af4', PizzaFridayExpense117af4, par=10, inputs = {kafka_input_spout : Grouping.SHUFFLE})
    teamsize58f7d6476c1e45_bolt = builder.add_bolt('teamsize58f7d6476c1e45', TeamSize58f7d6476c1e45, par=10, inputs = {kafka_input_spout : Grouping.SHUFFLE})
    freetimeexpenditure5dbfc_bolt = builder.add_bolt('freetimeexpenditure5dbfc', FreetimeExpenditure5dbfc, par=5, inputs = {tembuildingspending65c89_bolt : Grouping.fields('unique_id'), pizzafridayexpense117af4_bolt : Grouping.fields('unique_id'), teamsize58f7d6476c1e45_bolt : Grouping.fields('unique_id')})
    buisnesstriplivingcosta7_bolt = builder.add_bolt('buisnesstriplivingcosta7', BuisnessTripLivingCosta7, par=10, inputs = {kafka_input_spout : Grouping.SHUFFLE})
    buisnesstriptravelcost25_bolt = builder.add_bolt('buisnesstriptravelcost25', BuisnessTripTravelCost25, par=10, inputs = {kafka_input_spout : Grouping.SHUFFLE})
    buisnesstripdailyallowanc_bolt = builder.add_bolt('buisnesstripdailyallowanc', BuisnessTripDailyAllowanc, par=10, inputs = {kafka_input_spout : Grouping.SHUFFLE})
    buisnesstripexpensesd055_bolt = builder.add_bolt('buisnesstripexpensesd055', BuisnessTripExpensesd055, par=5, inputs = {buisnesstriplivingcosta7_bolt : Grouping.fields('unique_id'), buisnesstriptravelcost25_bolt : Grouping.fields('unique_id'), buisnesstripdailyallowanc_bolt : Grouping.fields('unique_id')})
    mandatoryequipmentexpense_bolt = builder.add_bolt('mandatoryequipmentexpense', MandatoryEquipmentExpense, par=10, inputs = {kafka_input_spout : Grouping.SHUFFLE})
    optionalequipmentexpense_bolt = builder.add_bolt('optionalequipmentexpense', OptionalEquipmentExpense, par=10, inputs = {kafka_input_spout : Grouping.SHUFFLE})
    equipmentexpenses0a185e3_bolt = builder.add_bolt('equipmentexpenses0a185e3', EquipmentExpenses0a185e3, par=5, inputs = {mandatoryequipmentexpense_bolt : Grouping.fields('unique_id'), optionalequipmentexpense_bolt : Grouping.fields('unique_id')})
    workingplacecost98026c71_bolt = builder.add_bolt('workingplacecost98026c71', WorkingPlaceCost98026c71, par=10, inputs = {kafka_input_spout : Grouping.SHUFFLE})
    officeneedsexpenses595da_bolt = builder.add_bolt('officeneedsexpenses595da', OfficeNeedsExpenses595da, par=5, inputs = {equipmentexpenses0a185e3_bolt : Grouping.fields('unique_id'), workingplacecost98026c71_bolt : Grouping.fields('unique_id')})


    # emitter_bolt = builder.add_bolt("emitter_bolt", EmitterBolt, par=10,
    #                                 inputs={})


    topology_config = {constants.TOPOLOGY_RELIABILITY_MODE:
                        constants.TopologyReliabilityMode.EFFECTIVELY_ONCE,
                        constants.TOPOLOGY_STATEFUL_CHECKPOINT_INTERVAL_SECONDS: 30}

    builder.set_config(topology_config)

    # Finalize the topology graph
    builder.build_and_submit()