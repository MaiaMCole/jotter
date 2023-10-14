from typer.testing import CliRunner

from jotter.helpers import create_title_from_body
from jotter import jotter

from tests import TEST_DB_FILE_LOCATION

runner = CliRunner()


def test_create_title_from_body():
    title1 = create_title_from_body("Three word body.")
    title2 = create_title_from_body("A four word body.")
    title3 = create_title_from_body("Two words.")
    title4 = create_title_from_body("word")
    title5 = create_title_from_body("Here is a slightly longer body to test.")

    assert title1 == "Three Word Body"
    assert title2 == "A Four Word"
    assert title3 == "Two Words"
    assert title4 == "Word"
    assert title5 == "Here Is A"


def test_new_note():
    result = runner.invoke(
        jotter.app,
        [
            "new-note",
            "--title",
            "Test note 1",
            "--body",
            "Test note body for unit tests.",
            "--tag",
            "test",
        ],
    )
    print(result)
