import tkinter as tk
from typing import TYPE_CHECKING

from zetools import templates, repository, configs

if TYPE_CHECKING:
    pass


class TopMenu(tk.Menu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._templates = templates.get_template_markdown_files()
        self._templates_menu = tk.Menu(master=self, tearoff=False)
        self.add_cascade(label="New", menu=self._templates_menu)
        self._journal_menu = tk.Menu(master=self)

        # This is a weird function that makes sure the correct template name is passed in.
        # Otherwise, timeplate name always seemed to be last on the list.
        def _get_adder(template_name):
            def adder():
                self._templates_menu.add_command(label=template_name, command=lambda: self.new_and_open(
                    '{path}/{filename}'.format(
                        path=configs.template_filepath,
                        filename="{}.md".format(template_name)
                    )
                ))
            return adder

        for md_template in self._templates:
            adder = _get_adder(md_template.filename_without_ext)
            adder()

    @staticmethod
    def new_and_open(template_filepath: str) -> None:
        """Creates a new template based on the template indicated by filename, and opens it in
        default editor."""
        new_note = templates.create_new_from_template(template_filepath)
        repository.open_md(md_file=new_note)
