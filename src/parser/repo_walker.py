from pathlib import Path
from typing import Generator, Callable
from contextlib import contextmanager

from config.vcs import get_vcs_profile, VcsProfile, Vcs
from config.language import get_language_profiles, LanguageProfile
from config.language import Language

type _IgnoreRule = Callable[[Path], bool]


def walk_repo(
    indexing_languages: list[Language], repository_root: Path, repository_vcs: Vcs
) -> Generator[Path, None, None]:
    language_profiles = get_language_profiles(indexing_languages)
    language_extensions = frozenset().union(
        *[prof.extensions for prof in language_profiles]
    )
    yield from _walk_repo(
        repository_root,
        [lambda path: path.suffix not in language_extensions],
        get_vcs_profile(repository_vcs),
    )


@contextmanager
def _ignore_rules_context(
    path: Path, ignore_rules: list[_IgnoreRule], vcs_profile: VcsProfile
) -> Generator[None, None, None]:
    ignore_file = path / vcs_profile.ignore_filename
    has_ignore_file = ignore_file.exists()
    if has_ignore_file:
        ignore_rules.append(vcs_profile.ignore_parser(ignore_file))
        try:
            yield
        finally:
            if has_ignore_file:
                ignore_rules.pop()
    else:
        yield


def _walk_repo(
    path: Path, ignore_rules: list[_IgnoreRule], vcs_profile: VcsProfile
) -> Generator[Path, None, None]:
    if path.is_dir():
        with _ignore_rules_context(path, ignore_rules, vcs_profile):
            for child in path.iterdir():
                yield from _walk_repo(child, ignore_rules, vcs_profile)
    else:
        if not any(rule(path) for rule in ignore_rules):
            yield path
