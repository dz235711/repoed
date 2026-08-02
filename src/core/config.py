from tomllib import load as load_toml
from pydantic import BaseModel
from pathlib import Path

from .enums import VCS, Language

class Git(BaseModel):
    respect_gitignore: bool


class Repository(BaseModel):
    root: str
    vcs: VCS
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
