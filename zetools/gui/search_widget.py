import tkinter as tk
from typing import Callable, List, Dict

import zetools


class SearchWidget(tk.Frame):
    """Search input widget."""

    def __init__(self, master, on_search: Callable[[Dict[str, str]], None]):
        super().__init__(master=master, bg=zetools.gui.configs.background_colour)
        self._on_search = on_search
        self._advanced_fields_visible = False
        self._toggle_advanced_button = tk.Button(master=self, text='...', bg=zetools.gui.configs.button_colour,
                                                 font=(zetools.gui.configs.std_font, 10),
                                                 command=self._toggle_advanced_fields)
        self._toggle_advanced_button.grid(row=0, column=0)
        self._search_entry = tk.Entry(master=self, bg=zetools.gui.configs.entry_background_colour,
                                      fg=zetools.gui.configs.emph_text_colour,
                                      width=45, relief=tk.FLAT,
                                      font=(zetools.gui.configs.std_font, zetools.gui.configs.std_font_size))
        self._search_entry.grid(row=0, column=1)
        self._search_button = tk.Button(master=self, text='Search', width=25, bg=zetools.gui.configs.button_colour,
                                        font=(zetools.gui.configs.std_font, zetools.gui.configs.std_font_size),
                                        command=lambda: print(self.get()))
        self._search_button.grid(row=0, column=2)
        self._advanced_fields = tk.Frame(master=self)
        label_kwargs = {
            "bg": zetools.gui.configs.background_colour,
            "fg": zetools.gui.configs.std_text_colour,
            "width": 21,
            "font": (zetools.gui.configs.std_font, zetools.gui.configs.std_font_size),
            "anchor": "w"
        }
        entry_kwargs = {
            "bg": zetools.gui.configs.entry_background_colour,
            "fg": zetools.gui.configs.emph_text_colour,
            "width": 50,
            "relief": tk.FLAT,
            "font": (zetools.gui.configs.std_font, zetools.gui.configs.std_font_size)
        }
        self._includes_in_title_entry = zetools.gui.LabelledEntry(
            master=self._advanced_fields,
            label_kwargs=dict(**label_kwargs, text="includes in title:"),
            entry_kwargs=entry_kwargs
        )
        self._includes_in_title_entry.pack()
        self._excludes_everywhere_entry = zetools.gui.LabelledEntry(
            master=self._advanced_fields,
            label_kwargs=dict(**label_kwargs, text="excludes everywhere:"),
            entry_kwargs=entry_kwargs
        )
        self._excludes_everywhere_entry.pack()
        self._excludes_in_title_entry = zetools.gui.LabelledEntry(
            master=self._advanced_fields,
            label_kwargs=dict(**label_kwargs, text="excludes in title"),
            entry_kwargs=entry_kwargs
        )
        self._excludes_in_title_entry.pack()

    def _place_advanced_fields(self) -> None:
        """Adds the advanced field entries to the grid."""
        self._advanced_fields.grid(row=1, column=0, columnspan=3, pady=15)

    def _toggle_advanced_fields(self) -> None:
        """Toggles the visiblity of the advanced search fields."""
        if self._advanced_fields_visible:
            self._advanced_fields_visible = False
            self._advanced_fields.grid_forget()
            self._clear_advanced_fields()
        else:
            self._advanced_fields_visible = True
            self._place_advanced_fields()

    def _clear_advanced_fields(self) -> None:
        """Zeroes the content of the advanced fields."""
        self._includes_in_title_entry.clear()
        self._excludes_everywhere_entry.clear()
        self._excludes_in_title_entry.clear()

    def get(self) -> Dict[str, List[str]]:
        """Returns the text """
        terms = {
            "inc_all": self._search_entry.get(),
            "inc_title": self._includes_in_title_entry.get(),
            "ex_all": self._excludes_everywhere_entry.get(),
            "ex_title": self._excludes_in_title_entry.get()
        }
        for key, value in terms.items():
            terms[key] = value.split(',')
            for i, term in enumerate(terms[key]):
                terms[key][i] = terms[key][i].strip().lower()
        return terms
