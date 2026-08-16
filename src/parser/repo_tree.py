from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Root:
    abs_path: Path
    directory: Directory


type Item = Directory | File


@dataclass(frozen=True, slots=True)
class Directory:
    rel_path: Path
    children: tuple[Item, ...]


@dataclass(frozen=True, slots=True)
class File:
    rel_path: Path
