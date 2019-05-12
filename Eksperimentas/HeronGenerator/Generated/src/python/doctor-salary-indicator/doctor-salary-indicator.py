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
    kafka_input_spout = builder.add_spout("kafka_input_spout", KafkaInputSpout, par=4)

    atlyginimasc5df16a0679a_bolt = builder.add_bolt('atlyginimasc5df16a0679a', Atlyginimasc5df16a0679a, par=2, inputs = {kafka_input_spout : Grouping.fields('SpoutOutput')})
    atostoginiai49e661dd1d6_bolt = builder.add_bolt('atostoginiai49e661dd1d6', Atostoginiai49e661dd1d6, par=2, inputs = {kafka_input_spout : Grouping.fields('SpoutOutput')})
    uzdarbis416f51b52b8a4c_bolt = builder.add_bolt('uzdarbis416f51b52b8a4c', Uzdarbis416f51b52b8a4c, par=1, inputs = {atlyginimasc5df16a0679a_bolt : Grouping.fields('Atlyginimas_c5df16a0-679a-4756-93da-df87b278efca'), atostoginiai49e661dd1d6_bolt : Grouping.fields('Atostoginiai_49e661dd-1d6a-496e-bac5-22d4358145a9')})
    loterijoslaimejimaid0550_bolt = builder.add_bolt('loterijoslaimejimaid0550', LoterijosLaimejimaid0550, par=2, inputs = {kafka_input_spout : Grouping.fields('SpoutOutput')})
    suvalgytasmaistasd05508c_bolt = builder.add_bolt('suvalgytasmaistasd05508c', SuvalgytasMaistasd05508c, par=2, inputs = {kafka_input_spout : Grouping.fields('SpoutOutput')})
    ismestasmaistasd05508c3_bolt = builder.add_bolt('ismestasmaistasd05508c3', IsmestasMaistasd05508c3, par=2, inputs = {kafka_input_spout : Grouping.fields('SpoutOutput')})
    maistoislaidosd05508c30_bolt = builder.add_bolt('maistoislaidosd05508c30', MaistoIslaidosd05508c30, par=1, inputs = {suvalgytasmaistasd05508c_bolt : Grouping.fields('SuvalgytasMaistas_d05508c3-0549-499d-bc02-7c25fd2b3e95'), ismestasmaistasd05508c3_bolt : Grouping.fields('IsmestasMaistas_d05508c3-0549-499d-bc01-7c25fd2b3e85')})
    komunaliniaid05508d3054_bolt = builder.add_bolt('komunaliniaid05508d3054', Komunaliniaid05508d3054, par=2, inputs = {kafka_input_spout : Grouping.fields('SpoutOutput')})
    islaidosd15508c3054849_bolt = builder.add_bolt('islaidosd15508c3054849', Islaidosd15508c3054849, par=1, inputs = {maistoislaidosd05508c30_bolt : Grouping.fields('MaistoIslaidos_d05508c3-0549-499d-bc01-7c25fd2b3e95'), komunaliniaid05508d3054_bolt : Grouping.fields('Komunaliniai_d05508d3-0549-499d-bc01-7c25fd2b3e95')})


    emitter_bolt = builder.add_bolt("emitter_bolt", EmitterBolt, par=10,
                                    inputs={uzdarbis416f51b52b8a4c_bolt : Grouping.ALL, atlyginimasc5df16a0679a_bolt : Grouping.ALL, atostoginiai49e661dd1d6_bolt : Grouping.ALL, loterijoslaimejimaid0550_bolt : Grouping.ALL, islaidosd15508c3054849_bolt : Grouping.ALL, maistoislaidosd05508c30_bolt : Grouping.ALL, suvalgytasmaistasd05508c_bolt : Grouping.ALL, ismestasmaistasd05508c3_bolt : Grouping.ALL, komunaliniaid05508d3054_bolt : Grouping.ALL})


    topology_config = {constants.TOPOLOGY_RELIABILITY_MODE:
                         constants.TopologyReliabilityMode.EFFECTIVELY_ONCE}

    builder.set_config(topology_config)

    # Finalize the topology graph
    builder.build_and_submit()