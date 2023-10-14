def create_title_from_body(body: str) -> str:
    """
    In the case that there is no title given a title is created from the first words of the the new note's body.
    """
    noPunctuation = body.strip(".!?")
    parts = noPunctuation.split(" ")
    return " ".join(parts[0:3]).title()
