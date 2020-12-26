import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zetools import MarkdownFile


class SearchResult(tk.Frame):
    """Search result display widget."""

    def __init__(self, master, markdown_file: 'MarkdownFile'):
        super().__init__(master)
        self._markdown_file = markdown_file
        self._title_display = tk.Label(master=self, text=self._markdown_file.title)
        self._title_display.bind("<Button-1>", lambda: master.event_generate("<<ResultTitleClick>>"))
        self._filename_display = tk.Label(master=self, text=self._markdown_file.rel_filepath)
        self._title_display.bind("<Button-1>", lambda: master.event_generate("<<ResultFNameClick>>"))

