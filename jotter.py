from datetime import datetime
import typer
from typing_extensions import Annotated
from typing import Optional
from rich import print

import callbacks

app = typer.Typer()


@app.command()
def new_note(
    body: Annotated[str, typer.Argument()],
    title: Annotated[Optional[str], typer.Option()] = None,
    tags: Annotated[Optional[list[str]], typer.Option("--tag")] = None,
):
    pass


@app.command()
def edit_note(
    note: Annotated[int, typer.Argument(help="number of the note you want to edit.")],
    body: Annotated[str, typer.Option(help="The new body of the note.")] = None,
    title: Annotated[
        Optional[str], typer.Option(help="The new title for the note.")
    ] = None,
    tags: Annotated[
        list[str],
        typer.Option("--tag", help="The new tags to be associated with the note."),
    ] = None,
):
    """Edit a note in the database."""
    # TODO:
    #   - select the note from the database
    #   - gather input data into a dict (make a function for this)
    #   - add/update "edited" to this dict of new data
    #   - update the note from the database with the dict of new data
    print(
        {
            "note": note,
            "body": body,
            "title": title,
            "tags": tags,
            "edited": datetime.now().date().isoformat(),
        }
    )


@app.command()
def list_notes(
    body: Annotated[str, typer.Option()] = None,
    title: Annotated[Optional[str], typer.Option()] = None,
    tags: Annotated[list[str], typer.Option("--tag")] = None,
    created: Annotated[datetime, typer.Option(formats=["%Y-%m-%d"])] = None,
    edited: Annotated[datetime, typer.Option(formats=["%Y-%m-%d"])] = None,
):
    """List all of your notes. Optionally filtering by --title, --body, --tags, --created, or --edited"""
    pass


if __name__ == "__main__":
    app()
