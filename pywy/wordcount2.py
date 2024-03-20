import os
import numpy as np
from JVM.java_classes import PywyJMV

from jpype import *
import jpype.imports

jar_pth = [
    f'{os.environ["WAYANG_HOME"]}/jars/*',
    f'{os.environ["WAYANG_HOME"]}/libs/*',
    f'{os.environ["WAYANG_HOME"]}/conf/*',
    f'{os.environ["SPARK_HOME"]}/jars/*',
    f'{os.environ["HADOOP_HOME"]}/jars/*',
]

jvm = PywyJMV()

jvm.start()
jvm.set_jclass(jar_pth)

from java.util import Arrays
from java.util import LinkedList

from org.apache.wayang.basic.data import Tuple2
from org.apache.wayang.core.types import DataSetType
from org.apache.wayang.core.optimizer import ProbabilisticDoubleInterval
from org.apache.wayang.core.function import FlatMapDescriptor, FunctionDescriptor
from org.apache.wayang.core.optimizer.costs import LoadProfileEstimator
from org.apache.wayang.basic.operators import *

from org.apache.wayang.core.plan.wayangplan import WayangPlan
from org.apache.wayang.core.api import WayangContext

from org.apache.wayang.core.api import Configuration

text_file_source = TextFileSource(
    "/Users/victor/Documents/incubator-pywayang/python/README.md"
)
text_file_source.setName("Load_file")

# # operator
# flatmap_operator = FlatMapOperator(
#     FlatMapDescriptor(
#         lambda line: line.split(),
#     )
# )
flatmap_operator = FlatMapOperator(lambda content: content.split())
flatmap_operator.setName("Split Words")


filter_operator = FilterOperator(lambda txt: JBoolean(not txt), JString.class_)
# # filter_operator = FilterOperator(
# #     lambda txt: JBoolean(not txt),
# #     DataSetType.createDefaultUnchecked(JArray(JString).class_),
# # )
# # filter_operator.setName("Filter empty words")

# collector = LinkedList()
collector = Tuple2()
sink = LocalCallbackSink.createCollectingSink(
    collector, DataSetType.createDefaultUnchecked(JString.class_)
)

sink.setName("Collect result")

text_file_source.connectTo(0, sink, 0)
flatmap_operator.connectTo(0, sink, 0)
flatmap_operator.connectTo(0, filter_operator, 0)
filter_operator.connectTo(0, sink, 0)

plan = JClass("org.apache.wayang.core.plan.wayangplan.WayangPlan")(sink)
way_context = JClass("org.apache.wayang.core.api.WayangContext")()

way_context.execute(plan)
