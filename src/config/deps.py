from functools import cache
from pathlib import Path

from config.config import Config

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config.toml"


@cache
def get_config() -> Config:
    return Config.load(CONFIG_PATH)
