import importlib.util as importutil
import sys
from typing import NewType

WayangModule = NewType("WayangModule", str)


class ModuleManager:
    def __init__(self) -> None:
        pass


def load_module(module_name: str):
    spec = importutil.find_spec(module_name)
    loader = importutil.LazyLoader(spec.loader)
    spec.loader = loader
    module = importutil.module_from_spec(spec=spec)
    sys.modules[module_name] = module
    loader.exec_module(module)
    return module


if __name__ == "__main__":
    pass

## TO DO:
# imports e resolver data structures

# import org.apache.wayang.api.JavaPlanBuilder
# import org.apache.wayang.basic.data.Tuple2
# import org.apache.wayang.core.api.Configuration
# import org.apache.wayang.core.api.WayangContext
# import org.apache.wayang.core.optimizer.cardinality.DefaultCardinalityEstimator
# import org.apache.wayang.java.Java
# import org.apache.wayang.spark.Spark
# import java.util.Collection
# import java.util.Arrays
