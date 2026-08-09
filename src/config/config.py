from tomllib import load as load_toml
from pathlib import Path

from pydantic import BaseModel

from config.languages import Language
from config.vcs import Vcs


class Git(BaseModel):
    respect_gitignore: bool


class Repository(BaseModel):
    root: Path
    vcs: Vcs
    git: Git


class Ignore(BaseModel):
    extra: frozenset[str]


class Indexing(BaseModel):
    languages: frozenset[Language]


class Config(BaseModel):
    repository: Repository
    ignore: Ignore
    indexing: Indexing

    @classmethod
    def load(cls, path: Path) -> Config:
        with open(path, "rb") as f:
            data = load_toml(f)
        return cls(**data)
