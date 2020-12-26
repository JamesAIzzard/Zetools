import subprocess
import tkinter as tk
from typing import TYPE_CHECKING

import pyperclip

from zetools import configs

if TYPE_CHECKING:
    from zetools import MarkdownFile


class SearchResult(tk.Frame):
    """Search result display widget."""

    def __init__(self, master, markdown_file: 'MarkdownFile'):
        super().__init__(master)
        self._markdown_file = markdown_file
        self._title_display = tk.Label(master=self, text=self.truncate_title(self._markdown_file.title), width=59,
                                       anchor=tk.W,
                                       font=(configs.std_font, configs.std_font_size),
                                       bg=configs.background_colour,
                                       fg=configs.std_text_colour)
        self._title_display.bind("<Button-1>", self._on_title_click)
        self._title_display.grid(row=0, column=0)
        self._filename_display = tk.Label(master=self, text=self._markdown_file.rel_filepath, width=17, anchor=tk.E,
                                          font=(configs.std_font, configs.std_font_size),
                                          bg=configs.background_colour,
                                          fg=configs.emph_text_colour)
        self._filename_display.bind("<Button-1>", self._on_filename_click)
        self._filename_display.grid(row=0, column=1)

    @staticmethod
    def truncate_title(title: str) -> str:
        """Trucates titles beyond a set length."""
        return (title[:configs.result_title_max_chars] + '...') if len(
            title) > configs.result_title_max_chars else title

    def _on_title_click(self, _):
        subprocess.run([self._markdown_file.filepath], shell=True)

    def _on_filename_click(self, _):
        pyperclip.copy(self._markdown_file.rel_filepath)
