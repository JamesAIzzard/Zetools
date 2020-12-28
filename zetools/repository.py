import os
import subprocess
import threading
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from zetools import markdown_file, configs

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


def count_notes() -> int:
    """Returns the number of notes inside the vault."""
    file_count = sum(len(files) for _, _, files in os.walk(configs.vault_filepath))
    return file_count


def get_vault_size() -> int:
    """Returns the size of the vault on disk in mb."""
    root_directory = Path(configs.vault_filepath)
    return sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())//(1024**2)

