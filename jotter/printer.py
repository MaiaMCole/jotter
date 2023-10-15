from rich.markdown import Markdown

from jotter.database import Note, Notes, SUCCESS


def markdown_notes(notes: Notes) -> Markdown | Notes:
    column_end = " |"
    if notes.return_code == SUCCESS:
        table = f"| note #{column_end} title{column_end} body{column_end} tags{column_end} created{column_end} edited{column_end}\n"
        table += "|---|---|---|---|---|---|\n"
        for note in notes.notes:
            tags: list = note.get("tags", [" - "])
            values = [
                notes.notes.index(note) + 1,
                note["title"].title(),
                note["body"][0:23] + "...",
                ", ".join(tags),
                note.get("created", " - "),
                note.get("edited", " - "),
            ]
            row_text = "|"
            for value in values:
                row_text += f" {value}{column_end}"
            row_text += "\n"
            table += row_text
        md = Markdown(table)
        return md
    else:
        return notes


def markdown_filtered_notes(notes: Notes) -> Markdown | Notes:
    column_end = " |"
    if notes.return_code == SUCCESS:
        table = f"| note #{column_end} title{column_end} body{column_end} tags{column_end} created{column_end} edited{column_end}\n"
        table += "|---|---|---|---|---|---|\n"
        for note in notes.notes:
            tags: list = note.get("tags", [" - "])
            values = [
                note["note_index"] + 1,
                note["title"].title(),
                note["body"][0:23] + "...",
                ", ".join(tags),
                note.get("created", " - "),
                note.get("edited", " - "),
            ]
            row_text = "|"
            for value in values:
                row_text += f" {value}{column_end}"
            row_text += "\n"
            table += row_text
        md = Markdown(table)
        return md


def markdown_note(note: Note) -> Markdown | Note:
    if note.return_code != SUCCESS:
        return note
    else:
        tags = note.note.get("tags", [" - "])
        edited = note.note.get("edited", " - ")
        note_text = f"# {note.note['title']}\n\n"
        note_text += note.note["body"] + "\n\n---\n\n"
        note_text += f"tags: {', '.join(tags)} | "
        note_text += f"created: {note.note['created']} | "
        note_text += f"edited: {edited}\n\n---\n\n"
        md = Markdown(note_text)
        return md
