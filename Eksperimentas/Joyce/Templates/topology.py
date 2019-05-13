# Import Grouping and TopologyBuilder from heronpy
from heronpy.api.stream import Grouping
from heronpy.api.topology import TopologyBuilder
import heronpy.api.api_constants as constants

# Import the defined Bolts and Spouts
from kafka_input_spout import KafkaInputSpout
<%TopologyBoltImports%>
from emitter_bolt import EmitterBolt
# from report_aggregation_bolt import ReportAggregationBolt

if __name__ == '__main__':
    # Define the topology name.
    builder = TopologyBuilder("<%TopologyName%>")

    # Start with the random sentence generator, create a reference and define a parallelism hint with par attribute
    kafka_input_spout = builder.add_spout("kafka_input_spout", KafkaInputSpout, par=4)

<%TopolgyBoltDefinitions%>

    emitter_bolt = builder.add_bolt("emitter_bolt", EmitterBolt, par=10,
                                    inputs={<%EmitterInputs%>})


    topology_config = {constants.TOPOLOGY_RELIABILITY_MODE:
                         constants.TopologyReliabilityMode.EFFECTIVELY_ONCE}

    builder.set_config(topology_config)

    # Finalize the topology graph
    builder.build_and_submit()