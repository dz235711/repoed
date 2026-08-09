from dataclasses import dataclass
from enum import StrEnum
from functools import cache
from typing import Callable, Optional

import tree_sitter as ts
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
    extensions: frozenset[str]


_LANGUAGE_PROFILES = frozendict(
    {
        Language.PYTHON: LanguageProfile(
            language=Language.PYTHON,
            extensions=frozenset({".py"}),
        ),
    }
)

_EXTENSION_TO_LANGUAGE_PROFILE_MAP = frozendict(
    {ext: prof for prof in _LANGUAGE_PROFILES.values() for ext in prof.extensions}
)


def get_language_profiles(languages: list[Language]) -> list[LanguageProfile]:
    return [_LANGUAGE_PROFILES[language] for language in languages]


class LanguageExtensionNotFoundError(Exception):
    pass


def get_language_profile_by_extension(extension: str) -> LanguageProfile:
    profile = _EXTENSION_TO_LANGUAGE_PROFILE_MAP.get(extension)
    if profile is None:
        raise LanguageExtensionNotFoundError(
            f"No language profile found for extension: {extension}"
        )
    return profile
