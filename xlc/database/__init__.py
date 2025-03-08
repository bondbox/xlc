# coding:utf-8

from xlc.database.langtags import LANGUAGES  # noqa:F401
from xlc.database.langtags import LangItem  # noqa:F401,H306
from xlc.database.langtags import LangT  # noqa:F401
from xlc.database.langtags import LangTag  # noqa:F401
from xlc.database.langtags import LangTags
from xlc.database.subtags import Language  # noqa:F401
from xlc.database.subtags import Region  # noqa:F401
from xlc.database.subtags import Script  # noqa:F401


class Database:
    def __init__(self):
        self.__langtags: LangTags = LangTags.from_config()

    @property
    def langtags(self) -> LangTags:
        return self.__langtags


DATABASE: Database = Database()
