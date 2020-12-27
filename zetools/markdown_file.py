import os
from typing import List

from . import configs


class MarkdownFile:
    """Represents and manipulates a markdown file."""

    def __init__(self, content_lines: List[str], filepath: str):
        self.filepath = filepath
        self.content_lines = content_lines

    @property
    def path(self) -> str:
        return os.path.split(self.filepath)[0]

    @path.setter
    def path(self, path: str) -> None:
        self.filepath = r'{path}\{filename_with_ext}'.format(
            path=path,
            filename_with_ext=self.filename_with_ext
        )

    @property
    def filename_with_ext(self) -> str:
        return os.path.basename(self.filepath)

    @property
    def filename_without_ext(self) -> str:
        return self.filename_with_ext.split('.')[0]

    @filename_without_ext.setter
    def filename_without_ext(self, filename_without_ext: str) -> None:
        ext = os.path.splitext(self.filepath)[1]
        self.filepath = r'{path}\{new_name}{ext}'.format(
            path=self.path,
            new_name=filename_without_ext,
            ext=ext
        )

    @property
    def title(self) -> str:
        """Gets the section_title of the markdown file."""
        return self.content_lines[0][1:].strip()

    @property
    def content(self) -> str:
        """Gets the content of a markdown file as a single string."""
        return ''.join(self.content_lines)

    @property
    def rel_filepath(self) -> str:
        """Returns the filepath of the markdown file, relative to the the vault."""
        return self.filepath.replace(configs.vault_filepath + '\\', '')

    def set_section(self, level: int, section_title: str, content: str) -> None:
        """Sets the content of a section in the file."""
        hash_delimiter = '#' * (level + 1)
        header = hash_delimiter + ' {}\n'.format(section_title)
        firstline, lastline = None, None
        # Find the first line of the section content;
        for i, line in enumerate(self.content_lines):
            if line == header:
                firstline = i + 1
                break
        for i, line in enumerate(self.content_lines[firstline:], start=firstline):
            if line[:level + 2] == hash_delimiter + ' ':
                lastline = i
        if lastline is None:
            lastline = len(self.content_lines)
        # Split the content into lines;
        content_lines = content.splitlines(keepends=True)
        self.content_lines = self.content_lines[:firstline] + content_lines + self.content_lines[lastline:]
