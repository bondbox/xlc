# coding:utf-8

from .langtags import LANGUAGES  # noqa:F401
from .langtags import LangItem  # noqa:F401,H306
from .langtags import LangT  # noqa:F401
from .langtags import LangTag  # noqa:F401
from .langtags import LangTags


class Database:
    def __init__(self):
        self.__langtags: LangTags = LangTags()

    @property
    def langtags(self) -> LangTags:
        return self.__langtags


DATABASE: Database = Database()
