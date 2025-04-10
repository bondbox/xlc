# coding:utf-8

import os
from typing import Dict
from typing import Iterator
from typing import Optional

from xlc.database.langtags import LangDict
from xlc.database.langtags import LangT
from xlc.database.langtags import LangTag
from xlc.language.segment import Segment


class Message():
    SUFFIX: str = ".xlc"

    def __init__(self, base: str):
        self.__segments: Dict[str, Segment] = {}
        self.__languages: LangDict = LangDict()
        self.__base: str = base

    def __iter__(self) -> Iterator[str]:
        return iter(self.__segments)

    def __len__(self) -> int:
        return len(self.__segments)

    def __contains__(self, langtag: LangT) -> bool:
        return self.languages.get(langtag).name in self.__segments

    def __getitem__(self, langtag: LangT) -> Segment:
        return self.__segments[self.languages.get(langtag).name]

    @property
    def base(self) -> str:
        return self.__base

    @property
    def languages(self) -> LangDict:
        return self.__languages

    def lookup(self, langtag: LangT) -> Segment:
        ltag: LangTag = self.languages.get(langtag)
        if segment := self.load(ltag):
            return segment
        for _tag in ltag.tags:
            ltag = self.languages[_tag]
            if segment := self.load(ltag):
                return segment
        raise LookupError(f"No such language tag: {langtag}")

    def load(self, ltag: LangTag) -> Optional[Segment]:
        if ltag.name in self.__segments:
            return self.__segments[ltag.name]

        path: str = os.path.join(self.base, ltag.name + self.SUFFIX)
        if os.path.isfile(path):
            segment: Segment = Segment.loadf(path)
            for atag in segment.lang.aliases:
                self.__segments.setdefault(atag, segment)
            self.__segments[segment.lang.name] = segment
            return segment
