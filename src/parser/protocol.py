from typing import Protocol, TypeVar
from pathlib import Path

from core.model import ParsedFile, ParserContext

_Context = TypeVar("_Context", bound=ParserContext, contravariant=True)


class Parser(Protocol):
    def parse(self, path: Path, context: _Context) -> ParsedFile: ...
