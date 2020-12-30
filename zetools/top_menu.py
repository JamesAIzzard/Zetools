import tkinter as tk
from typing import Optional, TYPE_CHECKING

import pyperclip

# Perhaps the view shouldn't be fetching the templates like this, but its OK for now.
from zetools import templates, configs, repository

if TYPE_CHECKING:
    pass


class View(tk.Menu):
    def __init__(self, root, **kwargs):
        super().__init__(master=root, **kwargs)
        self._root = root
        self._templates = templates.get_template_markdown_files()
        self.selected_template_name: Optional[str] = None
        self._template_menu = tk.Menu(master=self, tearoff=False)
        self.add_cascade(label="Templates", menu=self._template_menu)
        # self.add_cascade(label="Journal", menu=self._template_menu)
        # self.add_cascade(label="Delete", menu=self._template_menu)

        # Populate the template menu;
        # This is a weird function that makes sure the correct template name is passed in.
        # Otherwise, timeplate name always seemed to be last on the list.
        def _get_adder(template_name):
            def _adder():
                self._template_menu.add_command(label=template_name, command=lambda: self._on_template_click(
                    template_name=template_name
                ))

            return _adder

        for md_template in self._templates:
            adder = _get_adder(md_template.filename_without_ext)
            adder()

    def _on_template_click(self, template_name):
        self.selected_template_name = template_name
        self._root.event_generate('<<template-clicked>>')


class Controller:
    def __init__(self, root, view: 'View'):
        self._view = view
        self._root = root
        self._root.bind("<<template-clicked>>", self.on_create_from_template)

    def on_create_from_template(self, _) -> None:
        """Creates a new note from template, and opens it."""
        # Create the new note;
        template_filepath = "{path}/{filename}.md".format(
            path=configs.template_filepath,
            filename=self._view.selected_template_name)
        new_note = templates.create_new_from_template(template_filepath)
        # Copy the path to clipboard;
        pyperclip.copy(new_note.rel_filepath)
        # Open it;
        repository.open_md(md_file=new_note)
