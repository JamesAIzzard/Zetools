from typing import List, Optional, TYPE_CHECKING

from zetools import core

if TYPE_CHECKING:
    from zetools.core import MarkdownFile


def read_md(filepath: str) -> 'MarkdownFile':
    """Returns the markdown file as a list of strings.
    Args:
        filepath (str): Filepath of markdown file, including .md extension.
    """
    with open(filepath, 'r') as fh:
        return core.MarkdownFile(fh.readlines(), filepath)


def write_md(markdown_file: 'MarkdownFile') -> None:
    """Writes the content into the markdown file of the specified filepath.
    If the file doesn't exist, it is created. If the file is empty, it is overwritten."""
    with open(markdown_file.filepath, 'w') as fh:
        fh.write(markdown_file.content)


def get_md_title(filename: Optional[str] = None, lines: Optional[List[str]] = None) -> str:
    """Returns the title of the markdown file. This is the first line of the file, without the # symbol.
    Args:
        filename(str): Filename (without extension) to read and extract title from.
        lines(List[str]): File contents as a list of lines.
    """
    if filename is not None:
        lines = read_md(filename)
    title = lines[0].replace('#', '').strip()
    return title
