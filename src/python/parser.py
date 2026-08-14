from pathlib import Path

import tree_sitter_python as tspython
import tree_sitter as ts

from python.model import ParsedPythonFile, Node
from python.const import PACKAGE_INITIALISER_FILENAME
from config.language import Language


class Parser:
    __slots__ = ["_parser"]

    def __init__(self):
        self._parser = ts.Parser(ts.Language(tspython.language()))

    def parse(self, path: Path) -> ParsedPythonFile:
        tree = self._parser.parse(path.read_bytes())
        root = tree.root_node

        imports = []
        classes = []
        functions = []
        errors = []
        is_package_initializer = path.name == PACKAGE_INITIALISER_FILENAME
        is_test_file = path.name.startswith("test_") or path.parent.name == "tests"

        return ParsedPythonFile(
            path=path,
            language=Language.PYTHON,
            module_name=None,
            imports=tuple(imports),
            classes=tuple(classes),
            functions=tuple(functions),
            errors=tuple(errors),
            is_package_initializer=is_package_initializer,
            is_test_file=is_test_file,
        )
