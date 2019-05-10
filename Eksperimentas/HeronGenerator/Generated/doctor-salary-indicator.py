# Import Grouping and TopologyBuilder from heronpy
from heronpy.api.stream import Grouping
from heronpy.api.topology import TopologyBuilder
import heronpy.api.api_constants as constants

# Import the defined Bolts and Spouts
from kafka_input_spout import KafkaInputSpout
from Uždarbis_416f51b5-2b8a-4cb0-9978-f713d5990c52 import Uždarbis416f51b52b8a4c
from Atlyginimas_c5df16a0-679a-4756-93da-df87b278efca import Atlyginimasc5df16a0679a
from Atostoginiai_49e661dd-1d6a-496e-bac5-22d4358145a9 import Atostoginiai49e661dd1d6
from LoterijosLaimėjimai_d05508c3-0549-499d-be01-7c25fd2b3e95 import LoterijosLaimėjimaid0550

from emitter_bolt import EmitterBolt
# from report_aggregation_bolt import ReportAggregationBolt

if __name__ == '__main__':
    # Define the topology name.
    builder = TopologyBuilder("doctor-salary-indicator")

    # Start with the random sentence generator, create a reference and define a parallelism hint with par attribute
    kafka_input_spout = builder.add_spout("kafka_input_spout", KafkaInputSpout, par=4)

    uždarbis416f51b52b8a4c_bolt = builder.add_bolt('uždarbis416f51b52b8a4c', Uždarbis416f51b52b8a4c, par=2)
	inputs = {atlyginimasc5df16a0679a_bolt : Grouping.fields('Atlyginimas_c5df16a0-679a-4756-93da-df87b278efca'), atostoginiai49e661dd1d6_bolt : Grouping.fields('Atostoginiai_49e661dd-1d6a-496e-bac5-22d4358145a9')})
    atlyginimasc5df16a0679a_bolt = builder.add_bolt('atlyginimasc5df16a0679a', Atlyginimasc5df16a0679a, par=2)
	inputs = {kafka_input_spout : Grouping.fields('SpoutOutput');})
    atostoginiai49e661dd1d6_bolt = builder.add_bolt('atostoginiai49e661dd1d6', Atostoginiai49e661dd1d6, par=2)
	inputs = {kafka_input_spout : Grouping.fields('SpoutOutput');})
    loterijoslaimėjimaid0550_bolt = builder.add_bolt('loterijoslaimėjimaid0550', LoterijosLaimėjimaid0550, par=2)
	inputs = {kafka_input_spout : Grouping.fields('SpoutOutput');})


    emitter_bolt = builder.add_bolt("emitter_bolt", EmitterBolt, par=4,
                                    inputs={uždarbis416f51b52b8a4c_bolt : Grouping.fields('Uždarbis_416f51b5-2b8a-4cb0-9978-f713d5990c52'), loterijoslaimėjimaid0550_bolt : Grouping.fields('LoterijosLaimėjimai_d05508c3-0549-499d-be01-7c25fd2b3e95')})


    topology_config = {constants.TOPOLOGY_RELIABILITY_MODE:
                         constants.TopologyReliabilityMode.EFFECTIVELY_ONCE,
                         constants.TOPOLOGY_STATEFUL_CHECKPOINT_INTERVAL_SECONDS: 30}

    builder.set_config(topology_config)

    # Finalize the topology graph
    builder.build_and_submit()