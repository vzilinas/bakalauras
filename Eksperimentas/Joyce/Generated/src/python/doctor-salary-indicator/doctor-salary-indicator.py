# Import Grouping and TopologyBuilder from heronpy
from heronpy.api.stream import Grouping
from heronpy.api.topology import TopologyBuilder
import heronpy.api.api_constants as constants

# Import the defined Bolts and Spouts
from kafka_input_spout import KafkaInputSpout
from Uzdarbis416f51b52b8a4c import Uzdarbis416f51b52b8a4c
from Atlyginimasc5df16a0679a import Atlyginimasc5df16a0679a
from Atostoginiai49e661dd1d6 import Atostoginiai49e661dd1d6
from LoterijosLaimejimaid0550 import LoterijosLaimejimaid0550
from Islaidosd15508c3054849 import Islaidosd15508c3054849
from MaistoIslaidosd05508c30 import MaistoIslaidosd05508c30
from SuvalgytasMaistasd05508c import SuvalgytasMaistasd05508c
from IsmestasMaistasd05508c3 import IsmestasMaistasd05508c3
from Komunaliniaid05508d3054 import Komunaliniaid05508d3054

from emitter_bolt import EmitterBolt
# from report_aggregation_bolt import ReportAggregationBolt

if __name__ == '__main__':
    # Define the topology name.
    builder = TopologyBuilder("doctor-salary-indicator")

    # Start with the random sentence generator, create a reference and define a parallelism hint with par attribute
    kafka_input_spout = builder.add_spout("kafka_input_spout", KafkaInputSpout, par=10)

    atlyginimasc5df16a0679a_bolt = builder.add_bolt('atlyginimasc5df16a0679a', Atlyginimasc5df16a0679a, par=10, inputs = {kafka_input_spout : Grouping.SHUFFLE})
    atostoginiai49e661dd1d6_bolt = builder.add_bolt('atostoginiai49e661dd1d6', Atostoginiai49e661dd1d6, par=10, inputs = {kafka_input_spout : Grouping.SHUFFLE})
    uzdarbis416f51b52b8a4c_bolt = builder.add_bolt('uzdarbis416f51b52b8a4c', Uzdarbis416f51b52b8a4c, par=5, inputs = {atlyginimasc5df16a0679a_bolt : Grouping.fields('unique_id'), atostoginiai49e661dd1d6_bolt : Grouping.fields('unique_id')})
    loterijoslaimejimaid0550_bolt = builder.add_bolt('loterijoslaimejimaid0550', LoterijosLaimejimaid0550, par=10, inputs = {kafka_input_spout : Grouping.SHUFFLE})
    suvalgytasmaistasd05508c_bolt = builder.add_bolt('suvalgytasmaistasd05508c', SuvalgytasMaistasd05508c, par=10, inputs = {kafka_input_spout : Grouping.SHUFFLE})
    ismestasmaistasd05508c3_bolt = builder.add_bolt('ismestasmaistasd05508c3', IsmestasMaistasd05508c3, par=10, inputs = {kafka_input_spout : Grouping.SHUFFLE})
    maistoislaidosd05508c30_bolt = builder.add_bolt('maistoislaidosd05508c30', MaistoIslaidosd05508c30, par=5, inputs = {suvalgytasmaistasd05508c_bolt : Grouping.fields('unique_id'), ismestasmaistasd05508c3_bolt : Grouping.fields('unique_id')})
    komunaliniaid05508d3054_bolt = builder.add_bolt('komunaliniaid05508d3054', Komunaliniaid05508d3054, par=10, inputs = {kafka_input_spout : Grouping.SHUFFLE})
    islaidosd15508c3054849_bolt = builder.add_bolt('islaidosd15508c3054849', Islaidosd15508c3054849, par=5, inputs = {maistoislaidosd05508c30_bolt : Grouping.fields('unique_id'), komunaliniaid05508d3054_bolt : Grouping.fields('unique_id')})


    emitter_bolt = builder.add_bolt("emitter_bolt", EmitterBolt, par=10,
                                    inputs={uzdarbis416f51b52b8a4c_bolt : Grouping.SHUFFLE, atlyginimasc5df16a0679a_bolt : Grouping.SHUFFLE, atostoginiai49e661dd1d6_bolt : Grouping.SHUFFLE, loterijoslaimejimaid0550_bolt : Grouping.SHUFFLE, islaidosd15508c3054849_bolt : Grouping.SHUFFLE, maistoislaidosd05508c30_bolt : Grouping.SHUFFLE, suvalgytasmaistasd05508c_bolt : Grouping.SHUFFLE, ismestasmaistasd05508c3_bolt : Grouping.SHUFFLE, komunaliniaid05508d3054_bolt : Grouping.SHUFFLE})


    topology_config = {constants.TOPOLOGY_RELIABILITY_MODE:
                        constants.TopologyReliabilityMode.EFFECTIVELY_ONCE,
                        constants.TOPOLOGY_STATEFUL_CHECKPOINT_INTERVAL_SECONDS: 30}

    builder.set_config(topology_config)

    # Finalize the topology graph
    builder.build_and_submit()