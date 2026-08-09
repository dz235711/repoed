from pathlib import Path
from typing import Generator, Callable
from contextlib import contextmanager

from config.deps import get_config
from config.vcs import get_vcs_profile, VcsProfile
from config.languages import get_language_profiles, LanguageProfile
from config.config import Config


def walk_repo(config: Config) -> Generator[Path, None, None]:
    language_profiles = get_language_profiles(list(config.indexing.languages))
    language_extensions = frozenset().union(
        *[lp.extensions for lp in language_profiles]
    )
    yield from _walk_repo(
        config.repository.root,
        [lambda path: path.suffix not in language_extensions],
        get_vcs_profile(config.repository.vcs),
    )


@contextmanager
def _ignore_rules_context(
    path: Path, ignore_rules: list[Callable[[Path], bool]], vcs_profile: VcsProfile
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
    path: Path, ignore_rules: list[Callable[[Path], bool]], vcs_profile: VcsProfile
) -> Generator[Path, None, None]:
    if path.is_dir():
        with _ignore_rules_context(path, ignore_rules, vcs_profile):
            for child in path.iterdir():
                yield from _walk_repo(child, ignore_rules, vcs_profile)
    else:
        if not any(rule(path) for rule in ignore_rules):
            yield path
