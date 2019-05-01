# Import Grouping and TopologyBuilder from heronpy
from heronpy.api.stream import Grouping
from heronpy.api.topology import TopologyBuilder
import heronpy.api.api_constants as constants

# Import the defined Bolts and Spouts
from kafka_input_spout import KafkaInputSpout
<%TopologyBoltImports%>
# from report_aggregation_bolt import ReportAggregationBolt
# from price_calculation_bolt import PriceCalculationBolt

if __name__ == '__main__':
    # Define the topology name.
    builder = TopologyBuilder("<%TopologyName%>")

    # Start with the random sentence generator, create a reference and define a parallelism hint with par attribute
    kafka_input_spout = builder.add_spout("kafka_input_spout", KafkaInputSpout, par=4)

    <%TopolgyBoltDefinitions%>

    topology_config = {constants.TOPOLOGY_RELIABILITY_MODE:
                         constants.TopologyReliabilityMode.EFFECTIVELY_ONCE,
                         constants.TOPOLOGY_STATEFUL_CHECKPOINT_INTERVAL_SECONDS: 30}

    builder.set_config(topology_config)

    # Finalize the topology graph
    builder.build_and_submit()