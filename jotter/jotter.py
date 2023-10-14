from pathlib import Path
from datetime import datetime
import typer
from typing_extensions import Annotated
from rich import print

from jotter import ERRORS, __app_name__, config, database

app = typer.Typer()


@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="note database location?",
        help="Supply a location other than the default to initialize and use the database.",
    )
) -> None:
    """Initialize the note database."""
    # initialize config
    app_init_error = config.init_app(db_path)
    if app_init_error:
        print(
            f'[red]Creating config file failed with "{ERRORS[app_init_error]}"[/red]',
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        print(f'[red]Creating database failed with "{ERRORS[db_init_error]}"[/red]')
        raise typer.Exit(1)
    else:
        print(f"[green]The note database is: {db_path}[/green]")


@app.command()
def new_note(
    body: Annotated[str, typer.Argument(help="This is the main text of the note.")],
    title: Annotated[str, typer.Option(help="Give your note a good title.")] = None,
    tags: Annotated[
        list[str],
        typer.Option(
            "--tag", help="Create tags one by one to help organize them to your liking."
        ),
    ] = None,
):
    """Create a new note."""
    pass


@app.command()
def edit_note(
    note: Annotated[int, typer.Argument(help="number of the note you want to edit.")],
    body: Annotated[str, typer.Option(help="The new body of the note.")] = None,
    title: Annotated[str, typer.Option(help="The new title for the note.")] = None,
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
    body: Annotated[
        str, typer.Option(help="List all notes with these body words in their bodies.")
    ] = None,
    title: Annotated[
        str, typer.Option("List all notes with these words in their titles.")
    ] = None,
    tags: Annotated[
        list[str], typer.Option("--tag", help="List all notes with this tag.")
    ] = None,
    created: Annotated[
        datetime,
        typer.Option(formats=["%Y-%m-%d"], help="List all notes created on this date."),
    ] = None,
    edited: Annotated[
        datetime,
        typer.Option(
            formats=["%Y-%m-%d"],
            help="List all notes that were last edited on this date.",
        ),
    ] = None,
):
    """List all of your notes. Optionally filtering by --title, --body, --tags, --created, or --edited"""
    pass


@app.command()
def show_note(
    note: Annotated[int, typer.Argument(help="Number of the note you want to show.")]
):
    """Select a note to print its contents to the screen."""
    pass


@app.command()
def delete_note(
    note: Annotated[
        int, typer.Argument(help="The number of the note you want to delete")
    ]
):
    pass


if __name__ == "__main__":
    app()
