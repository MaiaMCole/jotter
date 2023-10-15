from rich.markdown import Markdown
from jotter import SUCCESS, ERRORS
from jotter.database import Note, Notes


def create_title_from_body(body: str) -> str:
    """
    In the case that there is no title given a title is created from the first words of the the new note's body.
    """
    noPunctuation = body.strip(".!?")
    parts = noPunctuation.split(" ")
    return " ".join(parts[0:2])


def create_args_dictionary(**kwargs) -> dict[str, any]:
    """Create and return a dictionary that removes all None values from the functions arguments."""
    args_dictionary = {}
    for key, value in kwargs.items():
        if value is not None:
            args_dictionary[key] = value
    return args_dictionary


def print_results(results: Notes | Note | Markdown) -> str | Markdown:
    try:
        return_code = results.return_code
        return f"[red-bold]{ERRORS[return_code]}[/red-bold]"
    except AttributeError:
        return results
