from enum import StrEnum, verify, UNIQUE
from pathlib import Path
import os

# this variable need to me set into as environment variable
_WAYANG_HOME = os.environ["WAYANG_HOME"]
_WAYANG_HOME = Path(_WAYANG_HOME) / "jars" / "*"


@verify(UNIQUE)
class WYdrivers(StrEnum):
    SPARK = "SPARK"
    FLINK = "FLINK"
    SQLITE = "SQLITE"
    POSTGRESS = "POSTGRESS"
