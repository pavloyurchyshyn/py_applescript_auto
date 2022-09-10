from abc import abstractmethod
from typing import Union


class AbsArgsKeys:
    """
    Keys which will be replaced by values.
    """

    @property
    @abstractmethod
    def Script(self):
        raise NotImplementedError

    Scr = Script

    @property
    @abstractmethod
    def Object(self):
        raise NotImplementedError

    Obj = Object

    @property
    @abstractmethod
    def Window(self):
        raise NotImplementedError

    Win = Window

    @property
    @abstractmethod
    def Application(self):
        raise NotImplementedError

    App = Application

    @property
    @abstractmethod
    def Value(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def Values(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def VariableName(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def Options(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def File(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def Whom(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def Property(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def Condition(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def If(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def Elif(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def Else(self):
        raise NotImplementedError


class AbsBaseAScript:

    @property
    @abstractmethod
    def Keys(self) -> AbsArgsKeys:
        raise NotImplementedError

    @abstractmethod
    def add_script(self, script, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def add_value(self, script, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def add(self, script,
            key: Union[str, None] = None,
            pos: int = 0,
            next_key='default_value',
            next_key_delim='\n',
            delay=0):
        raise NotImplementedError

    @abstractmethod
    def insert_scripts(self, *scripts,
                       key: str = None,
                       pos: int = 0,
                       delimiter: str = '\n', **kwargs):
        raise NotImplementedError

    @abstractmethod
    def add_kwargs(self, kwargs: dict):
        raise NotImplementedError

    @abstractmethod
    def add_delay(self, delay: int = 5, **kwargs):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def replace_to_position(body, script, key, position: int = 0) -> str:
        raise NotImplementedError

    @abstractmethod
    def join_scripts(self, *scripts):
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def pretty_str(self):
        raise NotImplementedError
