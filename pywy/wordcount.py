from jpype.types import *
import jpype.imports
import os

from JVM.java_classes import PywyJMV
from pathlib import Path


def wordcount():
    from org.apache.wayang.basic.data import Tuple2

    from org.apache.wayang.core.api import Configuration
    from org.apache.wayang.core.optimizer.cardinality import DefaultCardinalityEstimator
    from org.apache.wayang.java import Java

    # from org.apache.wayang.spark import Spark

    from java.util import Collection
    from java.util import Arrays

    # context = WayangContext(Configuration(defaultConfiguration="wayang-core-defaults.properties"))
    context = JClass("org.apache.wayang.core.api.WayangContext")(
        Configuration(defaultConfiguration="wayang-core-defaults.properties")
    )

    # builder = JavaPlanBuilder(context)  # .withJobName("wordcount")

    builder = JClass("org.apache.wayang.api.JavaPlanBuilder")(context)

    wordcounts = (
        builder.readTextFile("/Users/victor/Documents/incubator-wayang/CONTRIBUTING.md")
        .withName("Split words")
        .flatMap(lambda x: x.split("\n"))
        .filter(lambda token: not token)
        .withName("Filter empty words")
        .map(lambda word: Tuple2(word.lower(), 1))
        .withName("To lower case, add counter")
        .reduceByKey(lambda t1, t2: t1.getField1() + t2.getField1())
        # .collect()
    )
    print(wordcounts.collect())


if __name__ == "__main__":
    for name, var in os.environ.items():
        if "wayang" in name.lower():
            print(f"{name}: {var}")

    print(
        f'{os.environ["WAYANG_HOME"]}',
    )
    home = Path(os.environ["WAYANG_HOME"])
    home = home.parent.parent.parent
    # # jar_pth = [
    # #     f'{os.environ["WAYANG_HOME"]}/jars/*',
    # #     f'{os.environ["WAYANG_HOME"]}/libs/*',
    # #     f'{os.environ["SPARK_HOME"]}/jars/*',
    # #     f'{os.environ["HADOOP_HOME"]}/jars/*',
    # #     f'{os.environ["HADOOP_HOME"]}/conf/*',
    # # ]
    jar_pth = [*home.rglob("*.jar")] + [*home.rglob("*.class")]
    # jar_pth = [*home.rglob("*.class")]
    # print(len(jar_pth))
    # # jar_pth = home.rglob("*.jar")

    jvm = PywyJMV()
    jvm.start()
    jvm.set_jclass(jar_pth)

    wordcount()
#
