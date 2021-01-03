import tkinter as tk
from timeit import default_timer
from typing import List, TYPE_CHECKING

import zetools
from zetools import configs, search, results_widget

if TYPE_CHECKING:
    ...


class AdvSearchField(tk.Frame):
    """Advanced search field widget"""

    def __init__(self, master, label_text: str, **kwargs):
        super().__init__(master=master, bg=configs.background_colour, **kwargs)
        self._field = tk.Entry(master=self, bg=configs.entry_background_colour,
                               fg=configs.emph_text_colour,
                               font=(configs.std_font, configs.std_font_size),
                               width=45, highlightthickness=1, relief=tk.SUNKEN,
                               highlightbackground=configs.entry_background_colour,
                               highlightcolor=configs.emph_text_colour)
        self._label = tk.Label(master=self, bg=configs.background_colour,
                               fg=configs.std_text_colour, width=10,
                               font=(configs.std_font, configs.std_font_size),
                               anchor=tk.E, text=label_text)
        self._label.grid(row=0, column=0, padx=7)
        self._field.grid(row=0, column=1)

    def get(self) -> str:
        """Returns the content of the entry textbox."""
        return self._field.get()

    def clear(self) -> None:
        """Clears the content of the textbox."""
        self._field.delete(0, 'end')


class View(tk.Frame):
    """General search widget."""

    def __init__(self, master, **kwargs):
        super().__init__(master=master, bg=configs.background_colour, **kwargs)
        self._backlog_view_enabled = False
        self._advanced_search_enabled = False
        self._btn_backlog = zetools.ImageLabel(master=self, image_path='{path}/{name}'.format(
            path=configs.assets_filepath,
            name="backlog_button.png"
        ), img_width=26, bg=zetools.configs.background_colour, cursor="hand2")
        self._btn_backlog.bind("<Button-1>", self._on_toggle_backlog_view)
        self._btn_advanced_search = zetools.ImageLabel(master=self, image_path='{path}/{name}'.format(
            path=configs.assets_filepath,
            name="expand_button.png"
        ), img_width=30, bg=zetools.configs.background_colour, cursor="hand2")
        self._btn_advanced_search.bind("<Button-1>", self._on_toggle_adv_fields)
        self._lbl_project_prefix = tk.Label(master=self, text=" #incomplete, #project- ", bg=configs.background_colour,
                                            fg=configs.std_text_colour, relief=tk.SUNKEN,
                                            font=(configs.std_font, configs.std_font_size))
        self._txt_in_title = AdvSearchField(self, label_text="in title:")
        self._txt_not_in_title = AdvSearchField(self, label_text="not in title:")
        self._txt_nowhere = AdvSearchField(self, label_text="nowhere:")
        self._btn_search = zetools.ImageLabel(master=self, image_path='{path}/{name}'.format(
            path=configs.assets_filepath,
            name="search.png"
        ), img_width=25, bg=zetools.configs.background_colour, cursor="hand2")
        self._btn_search.bind("<Button-1>", lambda _: self.event_generate("<<Search>>"))
        self._txt_search = tk.Entry(master=self, bg=configs.entry_background_colour,
                                    fg=configs.emph_text_colour,
                                    width=50, highlightthickness=1,
                                    relief=tk.SUNKEN, highlightbackground=configs.entry_background_colour,
                                    highlightcolor=configs.emph_text_colour,
                                    font=(configs.std_font, configs.std_font_size))
        self._build()

    @staticmethod
    def _prep_search_string(search_string: str) -> List[str]:
        raw_list = search_string.split(',')
        output = []
        for term in raw_list:
            stripped_term = term.strip()
            if not stripped_term == '':
                output.append(stripped_term)
        return output

    def get(self) -> 'search.SearchDef':
        return search.SearchDef(
            inc_all=self._prep_search_string(self._txt_search.get()),
            inc_title=self._prep_search_string(self._txt_in_title.get()),
            ex_all=self._prep_search_string(self._txt_nowhere.get()),
            ex_title=self._prep_search_string(self._txt_not_in_title.get()),
            case_match=False,
            backlog_mode=self._backlog_view_enabled
        )

    def _on_toggle_backlog_view(self, _) -> None:
        """Responds to toggle backlog search_view button press."""
        self._backlog_view_enabled = not self._backlog_view_enabled
        self.reset_search()
        self._clear()
        self._build()

    def _on_toggle_adv_fields(self, _) -> None:
        """Responds to toggle advanced fields button press."""
        self._advanced_search_enabled = not self._advanced_search_enabled
        self.reset_adv_fields()
        self._clear()
        self._build()

    def _build_std_search(self) -> None:
        """Adds the standard search components to the UI."""
        self._btn_backlog.grid(row=0, column=0, padx=3)
        self._btn_advanced_search.grid(row=0, column=1, padx=3)
        self._txt_search.configure(width=50)
        self._txt_search.grid(row=0, column=2, columnspan=2, padx=3)
        self._btn_search.grid(row=0, column=4)

    def _build_backlog_search(self) -> None:
        """Builds the backlog search."""
        self._btn_backlog.grid(row=0, column=0, padx=3)
        self._btn_advanced_search.grid(row=0, column=1, padx=3)
        self._lbl_project_prefix.grid(row=0, column=2)
        self._txt_search.configure(width=31)
        self._txt_search.grid(row=0, column=3, padx=(5, 3))
        self._btn_search.grid(row=0, column=4)

    def _build_adv_search(self) -> None:
        """Adds the advanced fields to the UI."""
        self._txt_in_title.grid(row=1, column=0, columnspan=4, padx=1)
        self._txt_not_in_title.grid(row=2, column=0, columnspan=4, padx=1)
        self._txt_nowhere.grid(row=3, column=0, columnspan=4, padx=1)

    def reset_search(self) -> None:
        """Clears the text from all the search fields."""
        self._txt_search.delete(0, 'end')
        self.reset_adv_fields()

    def reset_adv_fields(self) -> None:
        """Clears the test in the advanced search fields."""
        self._txt_in_title.clear()
        self._txt_not_in_title.clear()
        self._txt_nowhere.clear()

    def _clear(self) -> None:
        """Clears all child widgets."""
        for result in self.winfo_children():
            result.grid_forget()

    def _build(self) -> None:
        """Assembles the views."""
        if self._backlog_view_enabled:
            self._build_backlog_search()
        else:
            self._build_std_search()
        if self._advanced_search_enabled:
            self._build_adv_search()


class Controller:
    def __init__(self, search_view: 'View', results_widget_controller: 'results_widget.Controller'):
        self._view = search_view
        self._results_widget_controller = results_widget_controller
        self._view.bind_all("<<Search>>", self._on_search)
        self._view.bind_all("<<Clear-Search>>", self._on_clear_search, add='+')

    def _on_search(self, _) -> None:
        """Handler for search event."""
        self._results_widget_controller.show_search_spinner()
        start = default_timer()
        results = search.search(self._view.get())
        end = default_timer()
        self._results_widget_controller.load_results(results)
        self._results_widget_controller.set_summary(len(results), end-start)

    def _on_clear_search(self, _) -> None:
        """Handles the <<Reset-Search>> event."""
        self._view.reset_search()
