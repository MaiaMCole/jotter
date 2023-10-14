import configparser
from pathlib import Path
import json

from jotter import config, SUCCESS, DB_WRITE_ERROR

DEFAULT_DB_FILE_PATH = Path.home().joinpath(f".{Path.home().stem}_jotter_db.json")


def get_database_path() -> Path:
    """Return the current path to the note database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config.CONFIG_FILE_PATH)
    return Path(config_parser["General"]["database"])


def init_database(db_path: Path) -> int:
    """Create the note database."""
    try:
        db_path.write_text("[]")
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


def addnote(newnote: dict[str, any]):
    notes = []
    database_file = get_database_path()
    with database_file.open("r") as jsonIn:
        notes = json.load(jsonIn)
