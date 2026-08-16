from pathlib import Path

import tree_sitter_python as tspython
import tree_sitter as ts

from config.language import Language
from core.model import SourceSpan, Coordinate
from parser.ts_adaptor import src_span_from_node
from parser.python.model import PythonParsedFile, PythonParserContext, Import
from parser.python.const import PACKAGE_INITIALISER_FILENAME, TsNodeType


class Parser:
    __slots__ = ["_parser"]

    def __init__(self):
        self._parser = ts.Parser(ts.Language(tspython.language()))

    def parse(self, code: bytes, context: PythonParserContext) -> PythonParsedFile:
        tree = self._parser.parse(code)

        imports = []
        classes = []
        functions = []
        diagnostics = []
        is_package_initializer = context.path.name == PACKAGE_INITIALISER_FILENAME
        is_test_file = (
            context.path.name.startswith("test_") or context.path.parent.name == "tests"
        )

        fringe = [tree.root_node]
        while fringe:
            node = fringe.pop()
            match node.type:
                case _:
                    fringe.extend(node.children)

        return PythonParsedFile(
            path=context.path,
            language=Language.PYTHON,
            module_name=None,
            imports=tuple(imports),
            classes=tuple(classes),
            functions=tuple(functions),
            diagnostics=tuple(diagnostics),
            is_package_initializer=is_package_initializer,
            is_test_file=is_test_file,
        )
