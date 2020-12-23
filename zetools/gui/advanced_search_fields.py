import tkinter as tk
from typing import List

import zetools


class AdvancedSearchFields:
    def __init__(self, master):
        self._frame = tk.Frame(master=master, bg=zetools.gui.configs.background_colour)
        self._inc_title = zetools.gui.LabelledEntry(master=master, label_text="includes in title: ",
                                                    entry_char_width=zetools.gui.configs.search_char_width)
        self._inc_title.grid(row=1, column=0, sticky="w", pady=1)
        self._ex_all = zetools.gui.LabelledEntry(master=master, label_text="excludes everywhere: ",
                                                 entry_char_width=zetools.gui.configs.search_char_width)
        self._ex_all.grid(row=2, column=0, sticky="w", pady=1)
        self._ex_title = zetools.gui.LabelledEntry(master=master, label_text="excludes in title: ",
                                                   entry_char_width=zetools.gui.configs.search_char_width)
        self._ex_title.grid(row=3, column=0, sticky="w", pady=1)

    def get_inc_title(self) -> str:
        return self._inc_title.get()

    def get_ex_all(self) -> str:
        return self._ex_all.get()

    def get_ex_title(self) -> str:
        return self._ex_title.get()

    def clear_all(self) -> None:
        self._inc_title.delete(first=0, last=tk.END)
        self._ex_all.delete(first=0, last=tk.END)
        self._ex_title.delete(first=0, last=tk.END)

    def pack(self, **kwargs) -> None:
        self._frame.pack(**kwargs)

    def grid(self, **kwargs) -> None:
        self._frame.grid(**kwargs)
