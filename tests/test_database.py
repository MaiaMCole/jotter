import json
from datetime import datetime
from typer.testing import CliRunner

from jotter import database, jotter, NO_NOTE_ERROR, SUCCESS
from tests import TEST_DIRECTORY, TEST_DB_FILE_LOCATION

runner = CliRunner()

new_note = {
    "title": "my dawg",
    "body": "my dawggiee babyyyy",
    "tags": ["woof", "3"],
}


def test_savenote_created():
    runner.invoke(jotter.app, ["init", "-db", str(TEST_DB_FILE_LOCATION)])
    notes_after_save = database.addnote(new_note)
    saved_note = notes_after_save.notes.pop()
    assert saved_note["created"] == datetime.now().date().isoformat()


def test_savenote_notecount():
    runner.invoke(jotter.app, ["init", "-db", str(TEST_DB_FILE_LOCATION)])
    oldNotes = database.getnotes()
    newNotes = database.addnote(new_note)
    assert len(newNotes.notes) == len(oldNotes.notes) + 1


def test_selectnotes():
    with open(TEST_DIRECTORY.joinpath("jotter_test_data.json"), "r") as jsonIn:
        testData = json.load(jsonIn)
        for data in testData:
            database.addnote(data)
        # should retrieve 1 notes
        selection1 = database.selectnotes({"title": "first"})
        # should retrieve 2 notes
        selection2 = database.selectnotes({"title": "note"})
        # should retrieve 2 notes
        selection3 = database.selectnotes({"tags": ["short"]})
        # should retrieve 1 notes
        selection4 = database.selectnotes({"tags": "second", "created": "2000-1-1"})
        # should retrieve 0 notes
        selection5 = database.selectnotes({"created": "2000-1-1"})

        assert len(selection1.notes) == 1
        assert len(selection2.notes) == 2
        assert len(selection3.notes) == 2
        assert len(selection4.notes) == 1
        assert len(selection5.notes) == 0


def test_selectnote():
    runner.invoke(jotter.app, ["init", "-db", str(TEST_DB_FILE_LOCATION)])
    note_number1 = 1
    note_number2 = 5
    database.addnote(new_note)
    note1 = database.selectnote(note_number1)
    note2 = database.selectnote(note_number2)
    assert note1.return_code == SUCCESS
    # There should only be one note in the db now.
    assert note2.return_code == NO_NOTE_ERROR
    assert note1.note == new_note
    assert id(note1.note) != id(new_note)


def test_editnote_notecount():
    note_number = 1
    notes_before_edit = database.addnote(new_note)
    notes_after_edit = database.editnote(
        {"note_number": note_number, "title": "A changed title"}
    )
    assert len(notes_before_edit) == len(notes_after_edit)


def test_editnote_edited():
    runner.invoke(jotter.app, ["init", "-db", str(TEST_DB_FILE_LOCATION)])
    note_number = 1
    database.addnote(new_note)
    note_before_edit = database.selectnote(note_number)
    database.editnote({"note_number": note_number, "title": "A changed title"})
    note_after_edit = database.selectnote(note_number)
    assert note_after_edit != note_before_edit
    assert note_before_edit.note.get("edited", None)
    assert note_before_edit.note.get("created", None) == note_after_edit.note.get(
        "created", None
    )
    assert note_after_edit.note.get("edited", None) == datetime.now().date().isoformat()
    # Make sure we are not dealing with references of the same Notes object.
    assert id(note_before_edit) != id(note_after_edit)
    assert id(note_before_edit.note) != id(note_after_edit.note)
