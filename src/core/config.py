from tomllib import load as load_toml
from pydantic import BaseModel
from enums import VCS

class Repository(BaseModel):
    root: str
    vcs: VCS

class Ignore(BaseModel):
    extra: list[str]

class Config(BaseModel):
    repository: Repository
    ignore: Ignore

    @classmethod
    def load(cls, path: str) -> "Config":
        with open(path, "rb") as f:
            data = load_toml(f)
        return cls(**data)


print(Config.load("../../config.toml"))