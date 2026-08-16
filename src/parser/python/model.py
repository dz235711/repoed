from pydantic.v1 import NoneBytes
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from core.model import ParsedFile, ParserContext, SourceSpan, SourceName


@dataclass(frozen=True, slots=True)
class ImportName:
    name: SourceName
    span: SourceSpan
    alias: SourceName | None = None


@dataclass(frozen=True, slots=True)
class ImportStatement:
    names: tuple[ImportName, ...]
    span: SourceSpan
    scope_qualified_name: str | None = None


@dataclass(frozen=True, slots=True)
class FutureImportStatement:
    names: tuple[ImportName, ...]
    span: SourceSpan


@dataclass(frozen=True, slots=True)
class WildCardImport:
    span: SourceSpan


@dataclass(frozen=True, slots=True)
class RelativeImport:
    relative_level: int
    span: SourceSpan
    module_name: str | None = None


@dataclass(frozen=True, slots=True)
class ImportFromStatement:
    members: tuple[ImportName, ...] | WildCardImport
    span: SourceSpan
    module: SourceName | RelativeImport
    scope_qualified_name: str | None = None


type Import = ImportStatement | FutureImportStatement | ImportFromStatement


@dataclass(frozen=True, slots=True)
class PythonParsedFile(ParsedFile):
    imports: tuple[Import, ...]


@dataclass(frozen=True, slots=True)
class PythonParserContext(ParserContext):
    import_root: Path | None = None
