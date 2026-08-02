from functools import lru_cache
from pathlib import Path

from .config import Config

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config.toml"


@lru_cache
def get_config():
    return Config.load(CONFIG_PATH)
