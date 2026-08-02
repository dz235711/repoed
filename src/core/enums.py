from enum import StrEnum


class VCS(StrEnum):
    GIT = "git"
    MERCURIAL = "mercurial"
    SUBVERSION = "subversion"
    BAZAAR = "bazaar"
    FOSSIL = "fossil"
    CVS = "cvs"


class Language(StrEnum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    CSHARP = "csharp"
    RUBY = "ruby"
    PHP = "php"
    GO = "go"
    RUST = "rust"
    SWIFT = "swift"
    KOTLIN = "kotlin"
