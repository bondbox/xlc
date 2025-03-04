# coding:utf-8

from typing import Any
from typing import Dict

from toml import loads


class Context():
    def __init__(self):
        self.__datas: Dict[str, Any] = {}

    def get(self, index: str) -> Any:
        return self.__datas[index]

    def set(self, index: str, value: Any):
        self.__datas[index] = value

    def render(self, **kwargs: Any) -> Dict[str, str]:
        return {k: v.format(**kwargs) if isinstance(v, str) else str(v)
                for k, v in self.__datas.items()}


class Section(Context):
    def __init__(self, title: str = ""):
        self.__sections: Dict[str, Section] = {}
        self.__title: str = title
        super().__init__()

    def lookup(self, index: str) -> "Section":
        section: Section = self
        for key in index.split("."):
            section = section.search(key)
        return section

    def search(self, index: str) -> "Section":
        if index not in self.__sections:
            section = Section(".".join([self.__title, index]))
            self.__sections.setdefault(index, section)
        return self.__sections[index]

    def update(self, index: str, value: Any):
        if isinstance(value, dict):
            for k, v in value.items():
                self.search(index).update(k, v)
        else:
            self.set(index, value)


class Message(Section):
    def __init__(self):
        super().__init__()

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "Message":
        instance: Message = cls()
        for k, v in data.items():
            instance.update(k, v)
        return instance

    @classmethod
    def loads(cls, data: str) -> "Message":
        return cls.load(data=loads(data))

    @classmethod
    def loadf(cls, file: str) -> "Message":
        with open(file, "r", encoding="utf-8") as rhdl:
            return cls.loads(data=rhdl.read())
