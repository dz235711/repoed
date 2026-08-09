from functools import cache
from collections import defaultdict

from config.languages import Language
from parser.parser import Parser


class Parser_Pool:

    __slots__ = ("_parsers",)

    def __init__(self):
        self._parsers: dict[Language, Parser] = {}

    def get_parser(self, language: Language) -> Parser:
        return self._parsers.setdefault(language, Parser(language))


@cache
def get_parser_pool() -> Parser_Pool:
    return Parser_Pool()
