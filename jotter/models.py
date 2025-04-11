from typing import NamedTuple


class Note(NamedTuple):
    return_code: int
    id: int
    title: str
    body: str
    tags: list
    created: str
    edited: str


class Notes(NamedTuple):
    return_code: int
    notes: list[Note] = None
