from dataclasses import dataclass
from enum import StrEnum
from functools import cache
from typing import Callable, Optional

from tree_sitter import Parser, Language as TSLanguage
import tree_sitter_python as tspython
from frozendict import frozendict


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


@dataclass(frozen=True)
class LanguageProfile:
    language: Language
    extensions: list[str]
    parser_factory: Callable[[], Parser]


@cache
def _get_language_profiles() -> frozendict[Language, LanguageProfile]:
    return frozendict(
        {
            Language.PYTHON: LanguageProfile(
                language=Language.PYTHON,
                extensions=[".py"],
                parser_factory=lambda: Parser(TSLanguage(tspython.language())),
            ),
        }
    )


def get_language_profiles(languages: list[Language]) -> list[LanguageProfile]:
    profiles = _get_language_profiles()
    return [profiles[language] for language in languages]
