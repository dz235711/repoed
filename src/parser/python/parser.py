from pathlib import Path
from dataclasses import replace

import tree_sitter_python as tspython
import tree_sitter as ts

from config.language import Language
from core.model import SourceSpan, Coordinate, SourceName
from parser.ts_adaptor import span_from_node, child_of, decode, first_type_of
from parser.python.model import (
    PythonParsedFile,
    PythonParserContext,
    ImportStatement,
    ImportName,
    FutureImportStatement,
    ImportFromStatement,
    WildCardImport,
    RelativeImport,
)
from parser.python.const import PACKAGE_INITIALISER_FILENAME
from parser.python.ts_nodes import (
    NodeType,
    ImportNameTypes,
    AliasedImportFields,
    ImportFromFields,
    ImportFromTypes,
    NameTypes,
    ModuleNameTypes,
    RelativeImportChildTypes,
    ImportStatementFields,
)


class Parser:
    __slots__ = ["_parser"]

    def __init__(self):
        self._parser = ts.Parser(ts.Language(tspython.language()))

    def parse(self, code: bytes, context: PythonParserContext) -> PythonParsedFile:
        tree = self._parser.parse(code)

        imports = []

        fringe = [tree.root_node]
        while fringe:
            node = fringe.pop()
            match node.type:
                case NodeType.IMPORT_STATEMENT:
                    imports.append(_parse_import_statement(node))
                case NodeType.FUTURE_IMPORT_STATEMENT:
                    imports.append(_parse_future_import_statement(node))
                case NodeType.IMPORT_FROM_STATEMENT:
                    imports.append(_parse_import_from_statement(node))
                case _:
                    fringe.extend(node.children)

        return PythonParsedFile(
            rel_path=context.rel_path,
            language=Language.PYTHON,
            imports=tuple(imports),
        )


def _parse_name(node: ts.Node) -> SourceName:
    match NameTypes(node.type):
        case NameTypes.DOTTED_NAME | NameTypes.NAME:
            assert node.text is not None
            return SourceName(name=decode(node.text), span=span_from_node(node))


def _parse_import_name(node: ts.Node) -> ImportName:
    match ImportNameTypes(node.type):
        case ImportNameTypes.ALIASED_IMPORT:
            import_name = _parse_import_name(child_of(node, AliasedImportFields.NAME))
            alias = child_of(node, AliasedImportFields.ALIAS)
            assert alias.text is not None
            return replace(
                import_name,
                span=span_from_node(node),
                alias=SourceName(name=decode(alias.text), span=span_from_node(alias)),
            )
        case ImportNameTypes.DOTTED_NAME:
            return ImportName(
                name=_parse_name(node),
                span=span_from_node(node),
            )


def _parse_import_statement(node: ts.Node) -> ImportStatement:
    span = span_from_node(node)
    names = tuple(
        _parse_import_name(child)
        for child in node.children_by_field_name(ImportStatementFields.NAME)
    )
    return ImportStatement(names=names, span=span, scope_qualified_name=None)


def _parse_future_import_statement(node: ts.Node) -> FutureImportStatement:
    span = span_from_node(node)
    names = tuple(
        _parse_import_name(child)
        for child in node.children
        if child.type in ImportNameTypes
    )
    return FutureImportStatement(names=names, span=span)


def _parse_module_name(node: ts.Node) -> SourceName | RelativeImport:
    match ModuleNameTypes(node.type):
        case ModuleNameTypes.DOTTED_NAME:
            return _parse_name(node)
        case ModuleNameTypes.RELATIVE_IMPORT:
            level = None
            name = None
            for child in node.children:
                match RelativeImportChildTypes(child.type):
                    case RelativeImportChildTypes.IMPORT_PREFIX:
                        level = child.end_point.column - child.start_point.column
                    case RelativeImportChildTypes.DOTTED_NAME:
                        name = _parse_name(child).name
            assert level is not None
            return RelativeImport(
                relative_level=level,
                module_name=name,
                span=span_from_node(node),
            )


def _parse_import_from_statement(node: ts.Node) -> ImportFromStatement:
    span = span_from_node(node)
    module_node = _parse_module_name(child_of(node, ImportFromFields.MODULE_NAME))
    members = tuple(
        _parse_import_name(child)
        for child in node.children_by_field_name(ImportFromFields.NAME)
    )
    if not members:
        wildcard = first_type_of(node, ImportFromTypes.WILDCARD_IMPORT)
        members = WildCardImport(span=span_from_node(wildcard))
    return ImportFromStatement(
        members=members,
        span=span,
        module=module_node,
        scope_qualified_name=None,
    )
