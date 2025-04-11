from rich.markdown import Markdown
from jotter import SUCCESS, ERRORS
from jotter.models import Note, Notes
from datetime import datetime


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
    if (
        args_dictionary.get("tags", None) is not None
        and len(args_dictionary.get("tags", None)) == 0
    ):
        del args_dictionary["tags"]

    return args_dictionary


def print_results(results: Notes | Note | Markdown) -> str | Markdown:
    try:
        return_code = results.return_code
        return f"[red-bold]{ERRORS[return_code]}[/red-bold]"
    except AttributeError:
        return results


def now_iso() -> str:
    now = datetime.now().isoformat()
    return now.split(".")[0]
