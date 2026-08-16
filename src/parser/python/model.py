from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Optional

from core.model import ParsedFile, ParserContext, SourceSpan


@dataclass(frozen=True, slots=True)
class Expression:
    text: str
    span: SourceSpan


class DiagnosticKind(StrEnum):
    SYNTAX_ERROR = "syntax_error"
    MISSING_NODE = "missing_node"
    UNSUPPORTED_CONSTRUCT = "unsupported_construct"


class DiagnosticSeverity(StrEnum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True, slots=True)
class Diagnostic:
    message: str
    span: SourceSpan
    kind: DiagnosticKind
    severity: DiagnosticSeverity


@dataclass(frozen=True, slots=True)
class Decorator:
    expression: Expression
    span: SourceSpan


class ParameterType(StrEnum):
    POSITIONAL_ONLY = "positional_only"
    POSITIONAL_OR_KEYWORD = "positional_or_keyword"
    VAR_POSITIONAL = "var_positional"
    KEYWORD_ONLY = "keyword_only"
    VAR_KEYWORD = "var_keyword"


@dataclass(frozen=True, slots=True)
class Parameter:
    name: str
    kind: ParameterType
    span: SourceSpan
    name_span: SourceSpan
    annotation: Optional[Expression] = None
    default_value: Optional[Expression] = None


@dataclass(frozen=True, slots=True)
class ImportName:
    name: str
    span: SourceSpan
    name_span: SourceSpan
    alias: Optional[str] = None
    alias_span: Optional[SourceSpan] = None


class ImportType(StrEnum):
    IMPORT = "import"
    FROM = "from"
    FUTURE = "future"


@dataclass(frozen=True, slots=True)
class Import:
    kind: ImportType
    module: Optional[str]
    relative_level: int
    names: tuple[ImportName, ...]
    is_wildcard: bool
    span: SourceSpan
    module_span: Optional[SourceSpan] = None
    scope_qualified_name: Optional[str] = None


class SymbolType(StrEnum):
    CLASS = "class"
    FUNCTION = "function"
    ASYNC_FUNCTION = "async_function"
    METHOD = "method"
    ASYNC_METHOD = "async_method"


@dataclass(frozen=True, slots=True)
class Class:
    name: str
    qualified_name: str
    span: SourceSpan
    name_span: SourceSpan
    body_span: SourceSpan
    bases: tuple[Expression, ...]
    decorators: tuple[Decorator, ...]
    parent_qualified_name: Optional[str]
    type_parameters: tuple[Expression, ...] = ()
    occurrence: int = 0

    @property
    def kind(self) -> SymbolType:
        return SymbolType.CLASS


@dataclass(frozen=True, slots=True)
class Function:
    name: str
    qualified_name: str
    kind: SymbolType
    span: SourceSpan
    name_span: SourceSpan
    body_span: SourceSpan
    parameters: tuple[Parameter, ...]
    decorators: tuple[Decorator, ...]
    parent_qualified_name: Optional[str]
    return_annotation: Optional[Expression] = None
    type_parameters: tuple[Expression, ...] = ()
    occurrence: int = 0


type PythonDefinition = Class | Function


class ReferenceType(StrEnum):
    NAME = "name"
    ATTRIBUTE = "attribute"
    CALL = "call"


@dataclass(frozen=True, slots=True)
class Reference:
    kind: ReferenceType
    target: Expression
    span: SourceSpan
    scope_qualified_name: Optional[str]


@dataclass(frozen=True, slots=True)
class MainGuard:
    span: SourceSpan
    body_span: SourceSpan


@dataclass(frozen=True, slots=True)
class PythonParsedFile(ParsedFile):
    module_name: Optional[str]
    imports: tuple[Import, ...]
    classes: tuple[Class, ...]
    functions: tuple[Function, ...]
    diagnostics: tuple[Diagnostic, ...]
    is_package_initializer: bool
    is_test_file: bool
    references: tuple[Reference, ...] = ()
    main_guards: tuple[MainGuard, ...] = ()
    module_docstring: Optional[Expression] = None


@dataclass(frozen=True, slots=True)
class PythonParserContext(ParserContext):
    import_root: Optional[Path]
