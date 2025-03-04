# coding:utf-8

from typing import Any
from typing import Dict

from toml import loads

sec = Dict[str, str]


class Section():
    def __init__(self, title: str, datas: sec):
        self.__title: str = title
        self.__datas: sec = datas

    def __getattr__(self, index: str) -> str:
        return self.__datas[index]

    @property
    def title(self) -> str:
        return self.__title

    def render(self, **kwargs: Any) -> sec:
        return {k: v.format(**kwargs) for k, v in self.__datas.items()}


class Context():
    def __init__(self, **kwargs: Section):
        self.__sections: Dict[str, Section] = kwargs

    def __getattr__(self, section: str) -> Section:
        return self.__sections[section]

    @classmethod
    def load(cls, data: Dict[str, sec]) -> "Context":
        return cls(**{k: Section(k, v) for k, v in data.items()})

    @classmethod
    def loads(cls, data: str) -> "Context":
        return cls.load(data=loads(data))

    @classmethod
    def loadf(cls, file: str) -> "Context":
        with open(file, "r", encoding="utf-8") as rhdl:
            return cls.loads(data=rhdl.read())
