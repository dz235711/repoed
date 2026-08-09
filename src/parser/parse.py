from pathlib import Path

from parser.parser_pool import get_parser_pool
from config.languages import Language


def parse(file_path: Path, language: Language):
    parser = get_parser_pool().get_parser(language)
    return parser.parse(file_path.read_bytes())
