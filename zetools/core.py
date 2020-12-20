from typing import List

from . import configs


class MarkdownFile:
    """Class to encapsulate and extend a markdown file."""

    def __init__(self, content_lines: List[str], filepath: str):
        self.filepath = filepath
        self.content_lines = content_lines

    @property
    def title(self) -> str:
        return self.content_lines[0][1:].strip()

    @property
    def content(self) -> str:
        return ''.join(self.content_lines)

    @property
    def rel_filepath(self) -> str:
        return self.filepath.replace(configs.vault_filepath + '\\', '')

    def set_section(self, level: int, title: str, content: str) -> None:
        hash_delimiter = '#' * (level + 1)
        header = hash_delimiter + ' {}\n'.format(title)
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
