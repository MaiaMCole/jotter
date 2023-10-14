import configparser
from pathlib import Path
import json
from jotter import config

DEFAULT_DB_FILE_PATH = Path.home().joinpath(f".{Path.home().stem}_jotter_db.json")


def get_database_path():
    config_parser = configparser.ConfigParser()
    config_parser.read()
    config.CONFIG_FILE_PATH


def addnote(newnote: dict[str, any]):
    notes = []
    pass
