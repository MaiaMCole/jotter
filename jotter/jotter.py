from pathlib import Path
from datetime import datetime
import typer
from typing_extensions import Annotated
from rich import print
from rich.console import Console

from jotter import SUCCESS, ERRORS, __app_name__, config, database, printer, helpers


app = typer.Typer(pretty_exceptions_short=False)
console = Console()


@app.callback()
def print_command_name(ctx: typer.Context):
    print(f"\n\n[bold]{ctx.invoked_subcommand.upper()}[/bold]")


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
def list_notes():
    db_notes = database.getnotes()
    md = printer.markdown_notes(db_notes)
    console.print(helpers.print_results(md))


@app.command()
def add_note(
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
    if title is None:
        title = helpers.create_title_from_body(body)

    args_dictionary = helpers.create_args_dictionary(title=title, body=body, tags=tags)
    db_notes = database.addnote(args_dictionary)
    md = printer.markdown_notes(db_notes)
    console.print(helpers.print_results(md))


@app.command()
def edit_note(
    note_number: Annotated[
        int, typer.Argument(help="number of the note you want to edit.")
    ],
    body: Annotated[str, typer.Option(help="The new body of the note.")] = None,
    title: Annotated[str, typer.Option(help="The new title for the note.")] = None,
    tags: Annotated[
        list[str],
        typer.Option("--tag", help="The new tags to be associated with the note."),
    ] = None,
):
    """Edit a note in the database."""
    dictionary_args = helpers.create_args_dictionary(
        note_number=note_number,
        body=body,
        title=title,
        tags=tags,
    )
    db_notes = database.editnote(dictionary_args)
    md = printer.markdown_notes(db_notes)
    console.print(helpers.print_results(md))


@app.command()
def filter_notes(
    body: Annotated[
        str, typer.Option(help="List all notes with these body words in their bodies.")
    ] = None,
    title: Annotated[
        str, typer.Option(help="List all notes with these words in their titles.")
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
    dictionary_args = helpers.create_args_dictionary(
        body=body, title=title, tags=tags, created=created, edited=edited
    )
    db_notes = database.filternotes(dictionary_args)
    md = printer.markdown_filtered_notes(db_notes)
    console.print(helpers.print_results(md))


@app.command()
def select_note(
    note_number: Annotated[
        int, typer.Argument(help="Number of the note you want to show.")
    ]
):
    """Select a note to print its contents to the screen."""
    db_note = database.selectnote(note_number)
    md = printer.markdown_note(db_note)
    console.print(md)


@app.command()
def delete_note(
    note_number: Annotated[
        int, typer.Argument(help="The number of the note you want to delete")
    ]
):
    db_notes = database.deletenote(note_number)
    md = printer.markdown_note(db_notes)
    console.print(md)


if __name__ == "__main__":
    app()
