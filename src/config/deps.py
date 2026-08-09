from functools import cache
from pathlib import Path

from config.config import Config

_CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config.toml"


@cache
def get_config() -> Config:
    return Config.load(_CONFIG_PATH)
