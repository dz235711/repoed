from enum import Enum

class VCS(str, Enum):
    GIT = "git"
    MERCURIAL = "mercurial"
    SUBVERSION = "subversion"
    BAZAAR = "bazaar"
    FOSSIL = "fossil"
    CVS = "cvs"

class Language(str, Enum):
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