from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from core.model import ParsedFile, ParserContext, SourceSpan, Expression


@dataclass(frozen=True, slots=True)
class ImportName:
    name: Expression
    span: SourceSpan
    alias: Expression | None = None


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
    module: Expression | RelativeImport
    scope_qualified_name: str | None = None


type Import = ImportStatement | FutureImportStatement | ImportFromStatement


@dataclass(frozen=True, slots=True)
class Parameter:
    name: Expression
    span: SourceSpan
    annotation: Expression | None
    default_value: Expression | None


@dataclass(frozen=True, slots=True)
class TypeParameter:
    name: Expression
    default: Expression | None = None


@dataclass(frozen=True, slots=True)
class BoundedTypeParameter(TypeParameter):
    bind: Expression


@dataclass(frozen=True, slots=True)
class ConstrainedTypeParameters(TypeParameter):
    constraints: list[Expression]


@dataclass(frozen=True, slots=True)
class Parameters:
    parameters: tuple[Parameter, ...]
    positional_parameters: tuple[Parameter, ...]
    keyword_parameters: tuple[Parameter, ...]
    var_positional_parameter: Parameter | None
    var_keyword_parameter: Parameter | None


@dataclass(frozen=True, slots=True)
class PositionalArgument:
    value: Expression


@dataclass(frozen=True, slots=True)
class KeywordArgument(PositionalArgument):
    name: Expression


@dataclass(frozen=True, slots=True)
class Arguments:
    positional_argument: tuple[PositionalArgument, ...]
    keyword_arguments: tuple[KeywordArgument, ...]
    iterable_unpacking: tuple[PositionalArgument, ...]
    keyword_unpacking: tuple[PositionalArgument, ...]


@dataclass(frozen=True, slots=True)
class Decorator:
    name: Expression
    arguments: Arguments


@dataclass(frozen=True, slots=True)
class Function:
    name: Expression
    qualified_name: str
    span: SourceSpan
    is_async: bool
    type_parameters: tuple[TypeParameter, ...]
    parameters: Parameters
    decorators: tuple[Decorator, ...]
    body_span: SourceSpan  # TODO: parse further once initial works
    return_annotation: Expression
    is_method: bool
    parent_qualified_name: str | None = None


@dataclass(frozen=True, slots=True)
class PythonParsedFile(ParsedFile):
    imports: tuple[Import, ...]


@dataclass(frozen=True, slots=True)
class PythonParserContext(ParserContext):
    import_root: Path | None = None
