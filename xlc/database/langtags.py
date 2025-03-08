# coding:utf-8

from os.path import dirname
from os.path import join
from typing import Any
from typing import Dict
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar

from toml import load

from xlc.database.subtags import Entry
from xlc.database.subtags import Language
from xlc.database.subtags import Region
from xlc.database.subtags import Script


class LangTag:
    """Language tag

    The syntax of the language tag in BCP47 is:
        langtag       = language["-" script]["-" region]

        language      = 2*3ALPHA            ; shortest ISO 639 code
                        ["-" extlang]       ; sometimes followed by
                                            ; extended language subtags
                      / 4ALPHA              ; or reserved for future use
                      / 5*8ALPHA            ; or registered language subtag

        extlang       = 3ALPHA              ; selected ISO 639 codes
                        *2("-" 3ALPHA)      ; permanently reserved

        script        = 4ALPHA              ; ISO 15924 code

        region        = 2ALPHA              ; ISO 3166-1 code
                      / 3DIGIT              ; UN M.49 codes

    The order of language tags is:
        1. language-script-region
        2. language-script
        3. language-region
        4. language
    """
    HYPHEN: str = "-"

    def __init__(self, langtag: str):
        tags: List[str] = langtag.replace("_", self.HYPHEN).split(self.HYPHEN)
        self.__language: Language = Language.get(tags.pop(0))
        self.__script: Optional[Script] = None
        self.__region: Optional[Region] = None
        if len(tags) == 1:
            key = tags.pop()  # region or script
            try:
                script = Script.get(key)
                self.__script = script
            except KeyError:
                region = Region.get(key)
                self.__region = region
        elif len(tags) == 2:
            self.__region = Region.get(tags.pop())
            self.__script = Script.get(tags.pop())
        full = self.filter(self.language, self.script, self.region)
        self.__name: str = self.join(*full)
        self.__tags: List[str] = []
        if len(full) == 3:
            self.__tags.append(self.join(full[0], full[1]))
            self.__tags.append(self.join(full[0], full[2]))
            self.__tags.append(self.join(full[0]))
        elif len(full) == 2:
            self.__tags.append(self.join(full[0]))

    def __iter__(self) -> Iterator[str]:
        return iter(self.__tags)

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: "LangT") -> bool:
        return self.name == str(other)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def tags(self) -> List[str]:
        """Replaceable subtags"""
        return self.__tags

    @property
    def language(self) -> Language:
        """Language in ISO 639"""
        return self.__language

    @property
    def script(self) -> Optional[Script]:
        """Script in ISO 15924"""
        return self.__script

    @property
    def region(self) -> Optional[Region]:
        """Country or Region in ISO 3166-1"""
        return self.__region

    @classmethod
    def filter(cls, *tags: Optional[Entry]) -> Tuple[Entry, ...]:
        return tuple(filter(None, tags))

    @classmethod
    def join(cls, *tags: Optional[Entry]) -> str:
        return cls.HYPHEN.join(str(tag) for tag in cls.filter(*tags))


LangT = TypeVar("LangT", str, LangTag)


class LangTagDict(Dict[str, LangTag]):
    def __init__(self):
        super().__init__()

    def __getitem__(self, index: str) -> LangTag:
        return self.lookup(index)

    def lookup(self, langtag: LangT) -> LangTag:
        lang: str = langtag.name if isinstance(langtag, LangTag) else langtag
        if lang not in self:
            ltag: LangTag = LangTag(lang)
            self.setdefault(lang, ltag)
        return super().__getitem__(lang)


LANGUAGES: LangTagDict = LangTagDict()


class LangItem():
    def __init__(self, langtag: LangTag, aliases: Iterable[str] = [],
                 description: str = "", recognition: str = ""):
        self.__langtag: LangTag = langtag
        self.__aliases: Tuple[LangTag, ...] = tuple(LANGUAGES[a] for a in aliases)  # noqa:E501
        self.__description: str = description or langtag.language.name
        self.__recognition: str = recognition or langtag.language.name

    @property
    def langtag(self) -> LangTag:
        return self.__langtag

    @property
    def aliases(self) -> Tuple[LangTag, ...]:
        return self.__aliases

    @property
    def description(self) -> str:
        return self.__description

    @property
    def recognition(self) -> str:
        return self.__recognition


class LangTags():
    """Language tags"""
    CONFIG: str = join(dirname(__file__), "langtags.toml")

    def __init__(self):
        data: Dict[str, Any]
        self.__tags: Dict[LangTag, LangItem] = {}
        with open(self.CONFIG, "r", encoding="utf-8") as rhdl:
            for lang, data in load(rhdl).items():
                ltag: LangTag = LANGUAGES.lookup(lang)
                desc: str = data.get("description", "")
                reco: str = data.get("recognition", "")
                if not reco:
                    for tag in ltag.tags:
                        _tag = LANGUAGES.lookup(tag)
                        if _tag in self.__tags:
                            reco = self.__tags[_tag].recognition
                            break
                aliases: List[str] = data.get("aliases", [])
                item = LangItem(langtag=ltag, aliases=aliases,
                                description=desc, recognition=reco)
                for atag in item.aliases:
                    self.__tags.setdefault(atag, item)
                self.__tags[item.langtag] = item

    def __iter__(self) -> Iterator[LangTag]:
        return iter(self.__tags)

    def __len__(self) -> int:
        return len(self.__tags)

    def lookup(self, langtag: LangT) -> LangItem:
        """Lookup language tag or replaceable subtags"""
        ltag: LangTag = LANGUAGES.lookup(langtag) if isinstance(langtag, str) else langtag  # noqa:E501
        if ltag in self.__tags:
            return self.__tags[ltag]
        for _tag in ltag.tags:
            tag = LANGUAGES[_tag]
            if tag in self.__tags:
                return self.__tags[tag]
        raise LookupError(f"No such language tag: {langtag}")
