from jotter import database, jotter
from datetime import datetime
import os
from typer.testing import CliRunner

from tests import TEST_DB_FILE_LOCATION

runner = CliRunner()


def test_saveNote():
    runner.invoke(jotter.app, ["init", "-db", str(TEST_DB_FILE_LOCATION)])
    new_note = {
        "title": "my dawg",
        "body": "my dawggiee babyyyy",
        "tags": ["woof", "3"],
    }
    saved_note = database.addnote(new_note)
    assert saved_note["created"] == datetime.now().date().isoformat()
