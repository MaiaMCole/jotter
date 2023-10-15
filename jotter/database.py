import configparser
from typing import NamedTuple
from pathlib import Path
import json
from datetime import datetime

from jotter import config, SUCCESS, DB_WRITE_ERROR, NO_NOTE_ERROR

DEFAULT_DB_FILE_PATH = Path.home().joinpath(f".{Path.home().stem}_jotter_db.json")


class Note(NamedTuple):
    return_code: int
    note: dict[str, any] = None


class Notes(NamedTuple):
    return_code: int
    notes: list[dict[str, any]] = None


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


def getnotes() -> Notes:
    database_file = get_database_path()
    with database_file.open("r") as jsonIn:
        try:
            notes: list = json.load(jsonIn)
            return Notes(SUCCESS, notes)
        except OSError:
            return Notes(DB_WRITE_ERROR)


def writenotes(incoming_notes: Notes) -> Notes:
    database_file = get_database_path()
    with database_file.open("w") as jsonOut:
        try:
            json.dump(incoming_notes.notes, jsonOut)
            return Notes(SUCCESS, incoming_notes.notes)
        except OSError:
            return Notes(DB_WRITE_ERROR)


def addnote(newnote: dict[str, any]) -> Notes:
    read_notes = getnotes()
    if read_notes.return_code != SUCCESS:
        return read_notes
    else:
        newnote["created"] = datetime.now().date().isoformat()
        read_notes.notes.append(newnote)
        return writenotes(read_notes)


def filternotes(query: dict[str, any]) -> Notes:
    selected_notes_dict = {}
    db_notes = getnotes()

    # add to a dictionary, overwriting a key so that no duplicates are included.
    def select_this_note(note: dict[str, any]):
        noteIndex = db_notes.notes.index(note)
        selected_notes_dict[noteIndex] = note

    # first check if reading db was successful
    if db_notes.return_code != SUCCESS:
        return db_notes
    else:
        # loop over key value pairs in query dictionary
        # loop through db_notes.notes list for each query type
        for type, value in query.items():
            # check for the unusual types that need additional treatment
            if type == "tags":
                for tag in value:
                    for note in db_notes.notes:
                        noteTags = note.get("tags", None)
                        if noteTags is not None and tag in noteTags:
                            select_this_note(note)
            elif type == "created" or type == "edited":
                # value in this case is already a datetime object
                for note in db_notes.notes:
                    dateKey = note.get(type, None)
                    if dateKey is not None and value == datetime.strptime(
                        dateKey, "%Y-%m-%d"
                    ):
                        select_this_note(note)
            # l
            else:
                for note in db_notes.notes:
                    noteValue = note[type]
                    if value.lower() in noteValue.lower():
                        select_this_note(note)
    selected_notes_list = []
    for noteIndex, note in selected_notes_dict.items():
        note["note_index"] = noteIndex
        selected_notes_list.append(note)
    return Notes(db_notes.return_code, list(selected_notes_list))


def editnote(note_args: dict[str, any]) -> Notes:
    note_index = note_args["note_number"] - 1
    del note_args["note_number"]
    note_args["edited"] = datetime.now().date().isoformat()
    db_notes = getnotes()
    if db_notes.return_code != SUCCESS:
        return db_notes
    try:
        for key, value in note_args.items():
            db_notes.notes[note_index][key] = value
        return writenotes(db_notes)
    except IndexError:
        return Notes(NO_NOTE_ERROR)


def selectnote(note_number: int) -> Note:
    note_index = note_number - 1
    db_notes = getnotes()
    if db_notes.return_code != SUCCESS:
        return db_notes
    try:
        selected_note = db_notes.notes[note_index]
        return Note(SUCCESS, selected_note)
    except IndexError:
        return Note(NO_NOTE_ERROR)


def deletenote(note_number: int) -> Notes:
    note_index = note_number - 1
    db_notes = getnotes()
    try:
        db_notes.notes.pop(note_index)
        return writenotes(db_notes)
    except IndexError:
        return Note(NO_NOTE_ERROR)
