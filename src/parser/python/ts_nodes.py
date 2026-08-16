from enum import StrEnum


class CoreFields(StrEnum):
    NAME = "name"


class NameTypes(StrEnum):
    DOTTED_NAME = "dotted_name"
    NAME = "name"


class NodeType(StrEnum):
    IMPORT_STATEMENT = "import_statement"
    FUTURE_IMPORT_STATEMENT = "future_import_statement"
    IMPORT_FROM_STATEMENT = "import_from_statement"


class ImportStatementFields(StrEnum):
    NAME = CoreFields.NAME


class ImportNameTypes(StrEnum):
    ALIASED_IMPORT = "aliased_import"
    DOTTED_NAME = NameTypes.DOTTED_NAME


class AliasedImportFields(StrEnum):
    NAME = CoreFields.NAME
    ALIAS = "alias"


class ImportFromFields(StrEnum):
    MODULE_NAME = "module_name"
    NAME = CoreFields.NAME


class ImportFromTypes(StrEnum):
    WILDCARD_IMPORT = "wildcard_import"


class ModuleNameTypes(StrEnum):
    DOTTED_NAME = NameTypes.DOTTED_NAME
    RELATIVE_IMPORT = "relative_import"


class RelativeImportChildTypes(StrEnum):
    DOTTED_NAME = NameTypes.DOTTED_NAME
    IMPORT_PREFIX = "import_prefix"
