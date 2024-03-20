import jpype
from typing import Dict, Generator, List, Never
from .CONSTS import *
from basics.base_classes import Singleton
from datetime import datetime
from functools import singledispatchmethod
from pathlib import Path
from dataclasses import dataclass, field


# def _validate_class(jclass: Dict[str, "WayangClass"]) -> Generator:
#     for name, mod in jclass.items():
#         if not isinstance(mod, WayangClass):
#             raise ValueError(f"{name} is not instance of 'WayangClass'")
#         yield name, mod


class JVMError(Exception):
    pass


class PywyJMV(Singleton):
    _started = False
    _init_time = None
    _close_time = None

    def __enter__(self, classpath=None):
        self.start()
        if classpath:
            self.set_jclass(classpath)

    def __exit__(*exc_info):
        pass

    @property
    def started(self) -> bool:
        self._started = jpype.isJVMStarted()
        return self._started

    @started.setter
    def started(cls, jvm_status) -> None:
        raise ValueError("Not allowed to set a started value")

    def start(self, classpath: str = None) -> None:
        if self._init_time:
            raise JVMError("JVM already started. Could not rise another JVM process")
        if not self._started:
            if not classpath:
                jpype.startJVM()
            else:
                jpype.startJVM(classpath=classpath)
            self._started = jpype.isJVMStarted()
            self._init_time = datetime.now()

    def shutdown(self) -> None:
        if self._started:
            print("desligando")
            jpype.shutdownJVM()
            self._started = jpype.isJVMStarted()
            self._close_time = datetime.now()

    def time_up(self) -> int:
        if not self._close_time:
            return (datetime.now() - self._init_time).seconds
        return (self._close_time - self._init_time).seconds

    @property
    def core_classes(self) -> Dict:
        return self._core_classes

    @core_classes.setter
    def core_classes(cls, new_class: Dict):
        raise ValueError("Not allowed to set a a new core module")

    # @property
    # def java_classes(self) -> Dict:
    #     return self.classpath

    # @java_classes.setter
    # def java_classes(self, new_jclass: str | List[str]) -> None:
    #     self.set_jclass(new_jclass=new_jclass)

    @singledispatchmethod
    def set_jclass(self, new_jclass) -> None:
        raise ValueError(
            "For adding a new java mode uses dict(module_name='WayangClass') as argument"
        )

    @set_jclass.register(str)
    def _(self, new_jclass: str):
        jpype.addClassPath(new_jclass)

    @set_jclass.register(list)
    def _(self, new_jclass: list) -> None:
        # TO DO: refatorar
        # for name, mod in _validate_class(self.java_classes):
        #     assert _is_core_class(
        #         jclass=mod
        #     ), f"{name} module is a core module and can not be added."
        # self.classpath += new_jclass
        for jar_path in new_jclass:
            print(f"[LOADING] {jar_path.name}")
            jpype.addClassPath(str(jar_path))
