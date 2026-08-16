from enum import StrEnum

PACKAGE_INITIALISER_FILENAME = "__init__.py"


class TsNodeType(StrEnum):
    IMPORT_STATEMENT = "import_statement"
    IMPORT_FROM_STATEMENT = "import_from_statement"
