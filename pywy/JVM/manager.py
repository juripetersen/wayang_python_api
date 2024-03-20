from typing import Dict
from CONSTS import *


class Manager:
    def __init__(self, m_manager: "ModuleManager", jvm: PywyJMV = None) -> None:
        self._jvm = jvm or self.new_jvm()
        self._module_magager = m_manager

    def new_jvm(sefl):
        return PywyJMV()

    def is_jvm_running(self):
        return self._jvm.started

    def jmv_time_up(self) -> int:
        return self._jvm.time_up()

    def get_core_classes(self) -> Dict[str, "WayangClass"]:
        return self._module_magager.core_classes

    def get_non_core_classes(self) -> Dict[str, "WayangClass"]:
        return self._module_magager.java_modules

    def set_non_core_classes(self, module_dict: Dict[str, "WayangClass"]) -> None:
        self._module_magager.java_modules = module_dict
