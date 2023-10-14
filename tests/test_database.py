from jotter import database, jotter
from datetime import datetime
from typer.testing import CliRunner

from tests import TEST_DB_FILE_LOCATION

runner = CliRunner()

new_note = {
    "title": "my dawg",
    "body": "my dawggiee babyyyy",
    "tags": ["woof", "3"],
}


def test_savenote_created():
    runner.invoke(jotter.app, ["init", "-db", str(TEST_DB_FILE_LOCATION)])
    notes_after_save = database.addnote(new_note)
    saved_note = notes_after_save.pop()
    assert saved_note["created"] == datetime.now().date().isoformat()


def test_savenote_notecount():
    runner.invoke(jotter.app, ["init", "-db", str(TEST_DB_FILE_LOCATION)])
    oldNotes = database.getnotes()
    newNotes = database.addnote(new_note)
    assert len(newNotes) == len(oldNotes) + 1


def test_editnote_notecount():
    runner.invoke(jotter.app, ["init", "-db", str(TEST_DB_FILE_LOCATION)])
    # like savedNote_notecount but note lengths should be the same.
    pass


def test_editnote_edited():
    runner.invoke(jotter.app, ["init", "-db", str(TEST_DB_FILE_LOCATION)])
    pass
