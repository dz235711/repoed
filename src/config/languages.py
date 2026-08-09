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


@cache
def _get_language_profiles() -> frozendict[Language, LanguageProfile]:
    return frozendict(
        {
            Language.PYTHON: LanguageProfile(
                language=Language.PYTHON,
                extensions=frozenset({".py"}),
            ),
        }
    )


def get_language_profiles(languages: list[Language]) -> list[LanguageProfile]:
    profiles = _get_language_profiles()
    return [profiles[language] for language in languages]


@cache
def _get_extension_to_language_profile_map() -> frozendict[str, LanguageProfile]:
    profiles = _get_language_profiles()
    extension_map = {}
    for profile in profiles.values():
        for ext in profile.extensions:
            extension_map[ext] = profile
    return frozendict(extension_map)


class LanguageExtensionNotFoundError(Exception):
    pass


def get_language_profile_by_extension(extension: str) -> LanguageProfile:
    profile = _get_extension_to_language_profile_map().get(extension)
    if profile is None:
        raise LanguageExtensionNotFoundError(
            f"No language profile found for extension: {extension}"
        )
    return profile
