import os
from typing import List, TYPE_CHECKING

from zetools import repository, configs, zettelkasten

if TYPE_CHECKING:
    from zetools import MarkdownFile


def get_template_markdown_files() -> List['MarkdownFile']:
    """Returns a list of the title of each template."""
    templates = []
    (_, _, template_filenames) = next(os.walk(configs.template_filepath))
    for template_filename in template_filenames:
        templates.append(repository.read_md('{path}/{name}'.format(
            path=configs.template_filepath,
            name=template_filename
        )))
    return templates


def create_new_from_template(template_filepath: str) -> 'MarkdownFile':
    """Creates a new note in the vault, based on the template specified."""
    # Open the template file;
    md_temp = repository.read_md(template_filepath)
    # Change the filename & filepath;
    md_temp.filename_without_ext = zettelkasten.generate()
    md_temp.path = configs.vault_filepath
    # Write the template file into the vault;
    repository.write_md(md_temp)
    # Return the file;
    return md_temp
