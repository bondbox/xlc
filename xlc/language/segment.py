# coding:utf-8

import os
from typing import Any
from typing import Dict

from toml import loads

from xlc.database import DATABASE
from xlc.database.langtags import LangItem
from xlc.database.langtags import LangT  # noqa:H306


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


class Segment(Section):
    def __init__(self, ltag: LangT):
        self.__lang: LangItem = DATABASE.langtags[ltag]
        super().__init__()

    @property
    def lang(self) -> LangItem:
        return self.__lang

    @classmethod
    def load(cls, ltag: LangT, data: Dict[str, Any]) -> "Segment":
        instance: Segment = cls(ltag)
        for k, v in data.items():
            instance.update(k, v)
        return instance

    @classmethod
    def loads(cls, ltag: LangT, data: str) -> "Segment":
        return cls.load(ltag=ltag, data=loads(data))

    @classmethod
    def loadf(cls, file: str) -> "Segment":
        with open(file, "r", encoding="utf-8") as rhdl:
            base: str = os.path.basename(file)
            ltag: str = base[:base.find(".")]
            data: str = rhdl.read()
            return cls.loads(ltag=ltag, data=data)
