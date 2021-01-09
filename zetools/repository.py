import os
import shutil
import subprocess
import threading
from pathlib import Path
from typing import Optional, List, Tuple, TYPE_CHECKING

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


def get_silo_name_for_note(filename: Optional[str] = None, filepath: Optional[str] = None) -> str:
    """Returns the silo name for a given filename."""
    if filepath is not None:
        filename = os.path.basename(filepath).split('.')[0]
    return filename[:6]


def create_silo(silo_name: str, silo_created_counter: Optional[List[int]] = None) -> None:
    """Creates silo in vault, if it doesn't exist already."""
    if silo_exists(silo_name):
        return
    silo_fp = '{}\\{}'.format(configs.vault_filepath, silo_name)
    os.mkdir(silo_fp)
    if silo_created_counter is not None:
        silo_created_counter[0] = silo_created_counter[0] + 1


def silo_exists(silo_name: str) -> bool:
    """Returns True/False to indicate if silo exists in vault."""
    silo_fp = '{}\\{}'.format(configs.vault_filepath, silo_name)
    p = Path(silo_fp)
    return p.exists()


def sort_silos() -> Tuple[int, int]:
    """Walks through the entire vault, creates silos where rqd and relocates notes into the correct silos."""
    files_moved_counter = [0]
    new_silos_created_counter = [0]

    def resolve_note_location(current_note_filepath: str) -> None:
        """Moves the specified note into the correct silo. Creates the silo if it doesn't exist."""
        corr_silo_name = get_silo_name_for_note(filepath=current_note_filepath)
        if not silo_exists(corr_silo_name):
            create_silo(corr_silo_name, silo_created_counter=new_silos_created_counter)
        dst = '{}\\{}\\{}'.format(configs.vault_filepath, corr_silo_name, filename)
        shutil.move(src=current_note_filepath, dst=dst)
        files_moved_counter[0] = files_moved_counter[0] + 1

    # Any/All files in top level will need moving into silos;
    tl_filenames = next(os.walk(configs.vault_filepath))[2]
    for filename in tl_filenames:
        resolve_note_location('{}\\{}'.format(configs.vault_filepath, filename))

    # Now check each silo, and if we find a note in the wrong silo, move it;
    silo_dirs = next(os.walk(configs.vault_filepath))[1]
    for current_silo_dir in silo_dirs:
        filenames = next(os.walk('{}\\{}'.format(configs.vault_filepath, current_silo_dir)))[2]
        for filename in filenames:
            correct_silo_dir = get_silo_name_for_note(filename=filename)
            if not correct_silo_dir == current_silo_dir:
                resolve_note_location(current_note_filepath='{}\\{}\\{}'.format(
                    configs.vault_filepath,
                    current_silo_dir,
                    filename
                ))

    return files_moved_counter[0], new_silos_created_counter[0]
