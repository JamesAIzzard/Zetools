import tkinter as tk
from typing import List, TYPE_CHECKING

import zetools
from zetools import configs, search, images

if TYPE_CHECKING:
    from zetools.search import SearchController, SearchDef
    from zetools import MarkdownFile


class SearchView(tk.Frame):
    """Search input widget."""

    def __init__(self, master, controller: 'SearchController'):
        super().__init__(master=master, bg=configs.background_colour)
        self._controller = controller
        self._advanced_fields_visible = False
        self._toggle_advanced_button = tk.Button(master=self, text='...', bg=configs.button_colour,
                                                 font=(configs.std_font, 10),
                                                 command=self._toggle_advanced_fields)
        self._toggle_advanced_button.grid(row=0, column=0)
        self._search_entry = tk.Entry(master=self, bg=configs.entry_background_colour,
                                      fg=configs.emph_text_colour,
                                      width=45, relief=tk.FLAT,
                                      font=(configs.std_font, configs.std_font_size))
        self._search_entry.grid(row=0, column=1)
        self._search_button = tk.Button(master=self, text='Search', width=25, bg=configs.button_colour,
                                        font=(configs.std_font, configs.std_font_size),
                                        command=lambda: self._controller.on_search(search_definition=self.get()))
        self._search_button.grid(row=0, column=2)
        self._advanced_fields = tk.Frame(master=self)
        label_kwargs = {
            "bg": configs.background_colour,
            "fg": configs.std_text_colour,
            "width": 21,
            "font": (configs.std_font, configs.std_font_size),
            "anchor": "w"
        }
        entry_kwargs = {
            "bg": configs.entry_background_colour,
            "fg": configs.emph_text_colour,
            "width": 50,
            "relief": tk.FLAT,
            "font": (configs.std_font, configs.std_font_size)
        }
        self._includes_in_title_entry = zetools.LabelledEntry(
            master=self._advanced_fields,
            label_kwargs=dict(**label_kwargs, text="includes in section:"),
            entry_kwargs=entry_kwargs
        )
        self._includes_in_title_entry.pack()
        self._excludes_everywhere_entry = zetools.LabelledEntry(
            master=self._advanced_fields,
            label_kwargs=dict(**label_kwargs, text="excludes everywhere:"),
            entry_kwargs=entry_kwargs
        )
        self._excludes_everywhere_entry.pack()
        self._excludes_in_title_entry = zetools.LabelledEntry(
            master=self._advanced_fields,
            label_kwargs=dict(**label_kwargs, text="excludes in section"),
            entry_kwargs=entry_kwargs
        )
        self._excludes_in_title_entry.pack()
        self._show_results_button = images.ImageButton(master=self, image_path=configs.expand_button_image_path,
                                                       img_width=20, bg=configs.button_colour)
        self._show_results_button.grid(row=3, column=1, columnspan=3, pady=15)
        self._search_results = tk.Frame(master=self)

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

    def _on_search(self) -> None:
        """Handler for when the search button is pressed."""
        results = self._controller.on_search(self.get())
        self.display_results(results)

    def display_results(self, results: List['MarkdownFile']) -> None:
        pass

    def get(self) -> 'SearchDef':
        """Collects input from fields and returns the search def object."""
        raw_terms = {
            "inc_all": self._search_entry.get(),
            "inc_title": self._includes_in_title_entry.get(),
            "ex_all": self._excludes_everywhere_entry.get(),
            "ex_title": self._excludes_in_title_entry.get(),
        }
        terms = {}
        for key, value in raw_terms.items():
            terms[key] = []
            raw_list = value.split(',')
            for term in raw_list:
                term = term.strip()
                if term != '':
                    terms[key].append(term.lower())
        return search.SearchDef(**terms, case_match=False)