from typing import Protocol

from core.model import ParsedFile


class Parser(Protocol):
    def parse(self, code: bytes) -> ParsedFile: ...
