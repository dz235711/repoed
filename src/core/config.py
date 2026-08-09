from tomllib import load as load_toml
from pathlib import Path

from pydantic import BaseModel

from .languages import Language
from .vcs import Vcs


class Git(BaseModel):
    respect_gitignore: bool


class Repository(BaseModel):
    root: Path
    vcs: Vcs
    git: Git


class Ignore(BaseModel):
    extra: list[str]


class Indexing(BaseModel):
    languages: list[Language]


class Config(BaseModel):
    repository: Repository
    ignore: Ignore
    indexing: Indexing

    @classmethod
    def load(cls, path: Path) -> Config:
        with open(path, "rb") as f:
            data = load_toml(f)
        return cls(**data)
