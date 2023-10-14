import configparser
from pathlib import Path
import json
from datetime import datetime

from jotter import config, SUCCESS, DB_WRITE_ERROR

DEFAULT_DB_FILE_PATH = Path.home().joinpath(f".{Path.home().stem}_jotter_db.json")


def get_database_path() -> Path:
    """Return the current path to the note database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config.CONFIG_FILE_PATH)
    return Path(config_parser["general"]["database"])


def init_database(db_path: Path) -> int:
    """Create the note database."""
    try:
        db_path.write_text("[]")
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


def getnotes() -> list[dict[str, any]]:
    database_file = get_database_path()
    with database_file.open("r") as jsonIn:
        notes: list = json.load(jsonIn)
    return notes


def writenotes(notes: list[dict[str, any]]) -> list[dict[str, any]]:
    database_file = get_database_path()
    with database_file.open("w") as jsonOut:
        json.dump(notes, jsonOut)
    return notes


def addnote(newnote: dict[str, any]) -> list[dict[str, any]]:
    notes = getnotes()
    newnote["created"] = datetime.now().date().isoformat()
    notes.append(newnote)
    writenotes(notes)
    print(notes)
    return notes


def editnote(notenumber: int) -> dict:
    pass
