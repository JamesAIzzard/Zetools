import tkinter as tk
from typing import Callable, Dict

import zetools


class SearchWidget:
    """Seach controls widget."""

    def __init__(self, master, on_search: Callable[[Dict[str, str]], None]):
        self._on_search = on_search
        self._advanced_visible = False
        self._frame = tk.Frame(master=master, bg=zetools.gui.configs.background_colour)

        self._main_search = tk.Frame(self._frame, bg=zetools.gui.configs.background_colour)
        self._btn_toggle_advanced = tk.Button(self._main_search, width=3, bg=zetools.gui.configs.button_colour,
                                              text="...", command=self._toggle_advanced)
        self._main_search_field = tk.Entry(self._main_search, width=zetools.gui.configs.search_char_width,
                                           bg=zetools.gui.configs.entry_background_colour,
                                           fg=zetools.gui.configs.emph_text_colour,
                                           font=(zetools.gui.configs.std_font, zetools.gui.configs.std_font_size),
                                           relief=tk.FLAT)
        self._btn_search = tk.Button(self._main_search, width=19, text="Search", bg=zetools.gui.configs.button_colour,
                                     font=(zetools.gui.configs.std_font, zetools.gui.configs.std_font_size),
                                     command=lambda: on_search(self._get_raw_inputs()))
        self._btn_toggle_advanced.grid(row=0, column=0, padx=5)
        self._main_search_field.grid(row=0, column=1)
        self._btn_search.grid(row=0, column=2, padx=6)
        self._main_search.grid(row=0, pady=15)

        self._advanced_fields_frame = tk.Frame(self._frame, bg=zetools.gui.configs.background_colour)
        self._advanced_fields = zetools.gui.AdvancedSearchFields(self._advanced_fields_frame)

    def _toggle_advanced(self) -> None:
        if self._advanced_visible:
            self._advanced_visible = False
            self._advanced_fields_frame.grid_forget()
            self._advanced_fields.clear_all()
        else:
            self._advanced_visible = True
            self._advanced_fields_frame.grid(row=2)

    def _get_raw_inputs(self) -> Dict[str, str]:
        return {
            "inc_all": self._main_search_field.get(),
            "inc_title": self._advanced_fields.get_inc_title(),
            "ex_all": self._advanced_fields.get_ex_all(),
            "ex_title": self._advanced_fields.get_ex_title()
        }

    def pack(self, **kwargs):
        self._frame.pack(**kwargs)

    def grid(self, **kwargs):
        self._frame.grid(**kwargs)
