from dataclasses import dataclass
from pathlib import Path

from config.language import Language


@dataclass(frozen=True)
class ParsedFile:
    path: Path
    language: Language


@dataclass(frozen=True)
class Coordinate:
    line: int
    column: int
    byte_offset: int


@dataclass(frozen=True)
class SourceSpan:
    start: Coordinate
    end: Coordinate
