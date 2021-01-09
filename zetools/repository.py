import os
import shutil
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
    return sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file()) // (1024 ** 2)


def get_silo_name(filename: str) -> str:
    """Returns the silo name for a given filename."""
    return filename[:6]


def sort_silos() -> None:
    """Walks through the entire vault, creates silos where rqd and relocates notes into the correct silos."""
    files_moved = 0
    new_silos_created = 0

    # def silo_exists(filename: str) -> Bool:
    #     silo_name = get_silo_name(filename)
    #     silo_fp = '{}\\{}'.format(configs.vault_filepath, silo_name)
    #     p = Path(silo_fp)
    #     if not p.exists():
    #         return False

    # Get filenames in top-level vault;
    tl_filenames = next(os.walk(configs.vault_filepath))[2]
    # Check each note and create its silo if it doesn't exist, then move note into silo;
    for filename in tl_filenames:
        silo_dir = get_silo_name(filename)
        silo_fp = '{}\\{}'.format(configs.vault_filepath, silo_dir)
        p = Path(silo_fp)
        if not p.exists():
            os.mkdir(silo_fp)
            new_silos_created = new_silos_created + 1
        # Move the note into its silo
        src = '{}\\{}'.format(configs.vault_filepath, filename)
        dst = '{}\\{}'.format(silo_fp, filename)
        shutil.move(src=src, dst=dst)
        files_moved = files_moved + 1

    # Now check each silo, and if we find a note in the wrong silo, move it;
    silo_dirs = next(os.walk(configs.vault_filepath))[1]
    for current_silo_dir in silo_dirs:
        _, _, filenames = next(os.walk('{}\\{}'.format(configs.vault_filepath, current_silo_dir)))
        for filename in filenames:
            correct_silo_dir = get_silo_name(filename)
            if not correct_silo_dir == current_silo_dir:
                # Create the new silo if it doesn't exist;
                correct_silo_fp = '{}\\{}'.format(configs.vault_filepath, correct_silo_dir)
                p = Path(correct_silo_fp)
                if not p.exists():
                    os.mkdir(correct_silo_fp)
                    new_silos_created = new_silos_created + 1
                # Move the note into the correct silo;
                src = '{}\\{}\\{}'.format(configs.vault_filepath, current_silo_dir, filename)
                dst = '{}\\{}\\{}'.format(configs.vault_filepath, correct_silo_dir, filename)
                shutil.move(src=src, dst=dst)
