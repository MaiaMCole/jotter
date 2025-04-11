import configparser
from pathlib import Path
import sqlite3
import json
from datetime import datetime
from jotter import config, SUCCESS, DB_WRITE_ERROR, DB_READ_ERROR, NO_NOTE_ERROR
from jotter.models import Note, Notes
from jotter.helpers import now_iso

DEFAULT_DB_FILE_PATH = Path.home().joinpath(f".{Path.home().stem}_jotter.db")


def get_database_path() -> Path:
    """Return the current path to the note database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config.CONFIG_FILE_PATH)
    return Path(config_parser["general"]["database"])


def get_database_connection() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_path = get_database_path()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    return (connection, cursor)


def instantiate_notes(db_notes: list[tuple]) -> list[dict]:
    """Takes a list of tuples and returns a list of dict. The list of tuples MUST be SELECTed by sql to be in the order of 'id, title, body, tags, created, editied'."""
    notes = []
    for note in db_notes:
        notes.append(
            Note(
                return_code=SUCCESS,
                id=note[0],
                title=note[1],
                body=note[2],
                tags=note[3].split(","),
                created=note[4],
                edited=note[5],
            )
        )
    return notes


# def init_database(db_path: Path) -> int:
def init_database() -> int:
    """Create the note database."""
    try:
        connection, cursor = get_database_connection()
        with connection:
            cursor.execute(
                "CREATE TABLE note (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, body TEXT NOT NULL, created TEXT NOT NULL, edited TEXT, tags TEXT);"
            )
            cursor.execute(
                "CREATE TABLE person (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, mail TEXT NOT NULL);"
            )
            cursor.execute(
                "CREATE TABLE share (id INTEGER PRIMARY KEY AUTOINCREMENT, note_id INTEGER NOT NULL, person_id INTEGER NOT NULL);"
            )
            # now = now_iso()
            # cursor.execute(
            #     f"INSERT INTO note (title, body, tags, created) VALUES('jotter 1', 'Welcome to Jotter! Try making some simple notes', 'welcome', '{now}');"
            # )
        now = now_iso()
        addnote(
            Note(
                return_code=SUCCESS,
                id=0,
                title="Jotter 1",
                body="Welcome to Jotter! Try making some simple notes",
                tags=["Welcome"],
                created=now,
                edited=now,
            )
        )
    except OSError:
        return DB_WRITE_ERROR


def getnotes() -> Notes:
    connection, cursor = get_database_connection()
    with connection:
        try:
            res = cursor.execute(
                "SELECT id, title, body, tags, created, edited FROM note;"
            )
            notes_db = res.fetchall()
            notes = instantiate_notes(notes_db)
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


def addnote(newnote: Note) -> Notes:
    connection, cursor = get_database_connection()
    with connection:
        sql = "INSERT INTO note (title, body, tags, created) VALUES(?, ?, ?, ?)"
        data = (newnote.title, newnote.body, ",".join(newnote.tags), newnote.created)
        cursor.execute(sql, data)


def filternotes(query: dict[str, any]) -> Notes:
    orderby = query.get("orderby")
    del query["orderby"]
    sql = "SELECT id, title, body, tags, created, edited from note WHERE "
    index = 0
    for field, value in query.items():
        index += 1
        andText = "AND" if index > 0 and index < len(query) else ""
        if field == "title" or field == "body":
            sql += f"{field} LIKE '%{value}%' {andText} "
        elif field == "tags":
            tagIndex = 1
            for tag in value:
                tagAndText = "AND" if tagIndex < len(value) else ""
                sql += f"{field} LIKE '%{tag}%' {tagAndText} "
                tagIndex += 1
            sql += f"{andText} "
        elif field == "orderby":
            continue
        else:
            sql += f"{field} LIKE '{value}%' {andText} "
    sql += f"ORDER BY {orderby};"
    try:
        connection, cursor = get_database_connection()
        with connection:
            res = cursor.execute(sql)
            db_notes = res.fetchall()
            if len(db_notes) > 0:
                notes = instantiate_notes(db_notes)
                return Notes(SUCCESS, notes)
            else:
                return Notes(NO_NOTE_ERROR)
    except OSError:
        return Notes(DB_READ_ERROR)


#     # add to a dictionary, overwriting a key so that no duplicates are included.
#     def select_this_note(note: dict[str, any]):
#         noteIndex = db_notes.notes.index(note)
#         selected_notes_dict[noteIndex] = note

#     # first check if reading db was successful
#     if db_notes.return_code != SUCCESS:
#         return db_notes
#     else:
#         # loop over key value pairs in query dictionary
#         # loop through db_notes.notes list for each query type
#         for type, value in query.items():
#             # check for the unusual types that need additional treatment
#             if type == "tags":
#                 for tag in value:
#                     for note in db_notes.notes:
#                         noteTags = note.get("tags", None)
#                         if noteTags is not None and tag in noteTags:
#                             select_this_note(note)
#             elif type == "created" or type == "edited":
#                 # value in this case is already a datetime object
#                 for note in db_notes.notes:
#                     dateKey = note.get(type, None)
#                     if dateKey is not None and value == datetime.strptime(
#                         dateKey, "%Y-%m-%d"
#                     ):
#                         select_this_note(note)
#             # l
#             else:
#                 for note in db_notes.notes:
#                     noteValue = note[type]
#                     if value.lower() in noteValue.lower():
#                         select_this_note(note)
#     selected_notes_list = []
#     for noteIndex, note in selected_notes_dict.items():
#         note["note_index"] = noteIndex
#         selected_notes_list.append(note)
#     return Notes(db_notes.return_code, list(selected_notes_list))


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
