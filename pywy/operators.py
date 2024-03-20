from JVM.java_classes import PywyJMV
from typing import Self

# from jpype import imports
from jpype.types import *
from jpype.beans import *
import jpype
import os

import numpy as np

jar_pth = [
    f'{os.environ["WAYANG_HOME"]}/jars/*',
    f'{os.environ["WAYANG_HOME"]}/libs/*',
    f'{os.environ["SPARK_HOME"]}/jars/*',
    f'{os.environ["HADOOP_HOME"]}/jars/*',
    f'{os.environ["HADOOP_HOME"]}/conf/*',
]

jvm = PywyJMV()
jvm.start()
jvm.set_jclass(jar_pth)


# JavaPlanBuilder = JClass("org.apache.wayang.api.JavaPlanBuilder")
# JavaConfiguration = JClass("org.apache.wayang.core.api.Configuration")
# JavaWayangContex = JClass("org.apache.wayang.core.api.WayangContext")


class WayangClass:
    _instance = None
    _jclass = None

    def __new__(self, *args, **kwargs) -> Self:
        self._instance = JClass(self._jclass)(*args, **kwargs)
        return self._instance


@jpype.JImplementationFor("org.apache.wayang.api.JavaPlanBuilder")
class PlanBuilder(WayangClass):
    _jclass = "org.apache.wayang.api.JavaPlanBuilder"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


@jpype.JImplementationFor("org.apache.wayang.core.api.Configuration")
class Configuration(WayangClass):

    _jclass = "org.apache.wayang.core.api.Configuration"

    def __init__(self, *args, **kwargs) -> None:
        print(*args, **kwargs)
        print(self._instance, self._jclass)
        super().__init__(*args, **kwargs)


@jpype.JImplementationFor("org.apache.wayang.core.api.WayangContext")
class WayangContext(WayangClass):
    _jclass = "org.apache.wayang.core.api.WayangContext"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


configuration = Configuration()
context = WayangContext(configuration)
builder = PlanBuilder(context)

fp = "/Users/victor/Documents/incubator-wayang/CONTRIBUTING.md"
file_path = JString(fp)

wordcounts = (
    builder.readTextFile(fp)
    .flatMap(lambda contet: np.array(contet.split()))
    # .flatMap(lambda x: np.arange(0, 1000, dtype=np.int32))
    .withName("bosta que não funciona")
    .dataQuanta()
    .collect()
)

print(wordcounts)
