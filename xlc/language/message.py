# coding:utf-8

import os
from typing import Dict
from typing import Iterator

from xlc.database.langtags import LangDict
from xlc.database.langtags import LangT
from xlc.database.langtags import LangTag
from xlc.database.langtags import LangTags
from xlc.language.segment import Segment


class Message():
    SUFFIX: str = ".xlc"

    def __init__(self):
        self.__segments: Dict[str, Segment] = {}
        self.__languages: LangDict = LangDict()

    def __iter__(self) -> Iterator[str]:
        return iter(self.__segments)

    def __len__(self) -> int:
        return len(self.__segments)

    def __contains__(self, langtag: LangT) -> bool:
        return self.languages.get(langtag).name in self.__segments

    def __getitem__(self, langtag: LangT) -> Segment:
        return self.__segments[self.languages.get(langtag).name]

    @property
    def languages(self) -> LangDict:
        return self.__languages

    def append(self, item: Segment) -> None:
        for atag in item.lang.aliases:
            self.__segments.setdefault(atag, item)
        self.__segments[item.lang.name] = item

    def lookup(self, langtag: LangT) -> Segment:
        ltag: LangTag = self.languages.get(langtag)
        if ltag in self.__segments:
            return self.__segments[ltag.name]
        for _tag in ltag.tags:
            ltag = self.languages[_tag]
            if ltag in self.__segments:
                return self.__segments[ltag.name]
        raise LookupError(f"No such language tag: {langtag}")

    @classmethod
    def load(cls, path: str) -> "Message":
        instance = cls()
        langtags: LangTags = LangTags.from_config()
        for file in os.listdir(path):
            _, ext = os.path.splitext(file)
            full: str = os.path.join(path, file)
            if os.path.isfile(full) and ext == cls.SUFFIX:
                segment: Segment = Segment.loadf(langtags, full)
                instance.append(segment)
        return instance
