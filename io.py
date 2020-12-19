from typing import List


def read_md(filename: str) -> List[str]:
    """Returns the markdown file as a list of strings."""
    with open('{}.md'.format(filename), 'r') as fh:
        return fh.readlines()


def write_md(filename: str, content: str) -> None:
    """Writes the content into the markdown file of the specified filename.
    If the file doesn't exist, it is created. If the file is empty, it is overwritten."""
    with open('{}.md'.format(filename), 'r') as fh:
        fh.write(content)
