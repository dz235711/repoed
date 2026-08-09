from core.ast import ParsedFile
from config.languages import Language


class Parser:
    def __init__(self, language: Language): ...

    def parse(self, code: bytes) -> ParsedFile:
        return ParsedFile()
