from dataclasses import dataclass
from pathlib import Path

from config.language import Language


@dataclass(frozen=True, slots=True)
class ParsedFile:
    rel_path: Path
    language: Language


@dataclass(frozen=True, slots=True)
class Coordinate:
    line: int
    column: int
    byte_offset: int


@dataclass(frozen=True, slots=True)
class SourceSpan:
    start: Coordinate
    end: Coordinate


@dataclass(frozen=True, slots=True)
class SourceName:
    name: str
    span: SourceSpan


@dataclass(frozen=True, slots=True)
class ParserContext:
    rel_path: Path
