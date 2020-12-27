import tkinter as tk
from typing import TYPE_CHECKING

from zetools import templates, repository

if TYPE_CHECKING:
    pass


class TopMenu(tk.Menu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._templates = templates.get_template_markdown_files()
        self._templates_menu = tk.Menu(master=self)
        self.add_cascade(label="Templates", menu=self._templates_menu)
        self._journal_menu = tk.Menu(master=self)

        for md_template in self._templates:
            self._templates_menu.add_command(
                label=md_template.filename_without_ext,
                command=lambda: self.new_and_open(md_template.filepath)
            )

    @staticmethod
    def new_and_open(template_filepath: str) -> None:
        """Creates a new template based on the template indicated by filename, and opens it in
        default editor."""
        new_note = templates.create_new_from_template(template_filepath)
        repository.open_md(md_file=new_note)
