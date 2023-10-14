from jotter import database
from datetime import datetime


def test_saveNote():
    new_note = {
        "title": "my dawg",
        "body": "my dawggiee babyyyy",
        "tags": ["woof", "3"],
    }
    saved_note = database.addnote(new_note)
    assert saved_note["created"] == datetime.now().date().isoformat()
