# coding:utf-8

from .langtags import LangTags


class Database:
    def __init__(self):
        self.__langtags: LangTags = LangTags()

    @property
    def langtags(self) -> LangTags:
        return self.__langtags
