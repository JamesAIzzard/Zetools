import subprocess
import threading
from typing import Optional, TYPE_CHECKING

from zetools import markdown_file

if TYPE_CHECKING:
    from zetools.markdown_file import MarkdownFile


def read_md(filepath: str) -> 'MarkdownFile':
    """Returns the markdown file as a list of strings.
    Args:
        filepath (str): Filepath of markdown file, including .md extension.
    """
    with open(filepath, 'r') as fh:
        return markdown_file.MarkdownFile(fh.readlines(), filepath)


def write_md(md_file: 'MarkdownFile') -> None:
    """Writes the content into the markdown file of the specified filepath.
    If the file doesn't exist, it is created. If the file is empty, it is overwritten."""
    with open(md_file.filepath, 'w') as fh:
        fh.write(md_file.content)


def open_md(md_file: Optional['MarkdownFile'] = None, filepath: Optional[str] = None) -> None:
    """Opens the specified or provided file the default editor."""
    if filepath is None:
        filepath = md_file.filepath

    def run():
        subprocess.run([filepath], shell=True)

    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
