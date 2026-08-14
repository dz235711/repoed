from typing import Optional
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from core.model import SourceSpan, ParsedFile

type Node = Error | Decorator | Parameter | Import | Class | Function


@dataclass(frozen=True)
class Error:
    message: str
    span: SourceSpan


@dataclass(frozen=True)
class Decorator:
    expression: str
    span: SourceSpan


class ParameterType(StrEnum):
    POSITIONAL_ONLY = "positional_only"
    POSITIONAL_OR_KEYWORD = "positional_or_keyword"
    VAR_POSITIONAL = "var_positional"
    KEYWORD_ONLY = "keyword_only"
    VAR_KEYWORD = "var_keyword"


@dataclass(frozen=True)
class Parameter:
    name: str
    annotation: Optional[str]
    default_value: Optional[str]
    type: ParameterType
    span: SourceSpan


@dataclass(frozen=True)
class ImportName:
    name: str
    alias: Optional[str]
    span: SourceSpan


@dataclass(frozen=True)
class Import:
    module: Optional[str]
    relative_level: int
    names: tuple[ImportName, ...]
    is_wildcard: bool
    span: SourceSpan


@dataclass(frozen=True)
class Class:
    name: str
    qualified_name: str
    bases: tuple[str, ...]
    decorators: tuple[Decorator, ...]
    span: SourceSpan
    parent_qualified_name: Optional[str]


class SymbolType(StrEnum):
    CLASS = "class"
    FUNCTION = "function"
    ASYNC_FUNCTION = "async_function"
    METHOD = "method"
    ASYNC_METHOD = "async_method"


@dataclass(frozen=True)
class Function:
    name: str
    qualified_name: str
    kind: SymbolType
    parameters: tuple[Parameter, ...]
    return_annotation: Optional[str]
    decorators: tuple[Decorator, ...]
    span: SourceSpan
    parent_qualified_name: Optional[str]


@dataclass(frozen=True)
class ParsedPythonFile(ParsedFile):
    module_name: Optional[str]
    imports: tuple[Import, ...]
    classes: tuple[Class, ...]
    functions: tuple[Function, ...]
    errors: tuple[Error, ...]
    is_package_initializer: bool
    is_test_file: bool
