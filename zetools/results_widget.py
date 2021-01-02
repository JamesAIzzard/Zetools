import tkinter as tk
from typing import List, TYPE_CHECKING

import zetools
from zetools import configs

if TYPE_CHECKING:
    from zetools import MarkdownFile


class SearchResultWidget(tk.Frame):
    """View component for a search result."""

    def __init__(self, master, search_result: 'MarkdownFile', **kwargs):
        super().__init__(master=master, **kwargs)
        self.search_result = search_result


class ResultsNavWidget(tk.Frame):
    """Widget to navigate through results pages."""

    def __init__(self, master, **kwargs):
        super().__init__(master=master, bg=configs.background_colour, **kwargs)
        self._nav_to_start = zetools.ImageLabel(master=self, image_path='{}/{}'.format(
            configs.assets_filepath, "nav_to_start.png"), img_width=20, bg=configs.background_colour, cursor="hand2")
        self._nav_to_start.grid(row=0, column=0)
        self._nav_forwards = zetools.ImageLabel(master=self, image_path='{}/{}'.format(
            configs.assets_filepath, "nav_forwards.png"), img_width=15, bg=configs.background_colour, cursor="hand2")
        self._nav_forwards.grid(row=0, column=1)
        self._nav_status = tk.Label(master=self, text="pg 0 of 0", bg=configs.background_colour,
                                    font=(configs.std_font, configs.small_font_size), fg=configs.std_text_colour)
        self._nav_status.grid(row=0, column=2)
        self._nav_backwards = zetools.ImageLabel(master=self, image_path='{}/{}'.format(
            configs.assets_filepath, "nav_backwards.png"), img_width=15, bg=configs.background_colour, cursor="hand2")
        self._nav_backwards.grid(row=0, column=3)
        self._nav_to_end = zetools.ImageLabel(master=self, image_path='{}/{}'.format(
            configs.assets_filepath, "nav_to_end.png"), img_width=20, bg=configs.background_colour, cursor="hand2")
        self._nav_to_end.grid(row=0, column=4)


class ResultsSummaryWidget(tk.Label):
    """Widget to present results summary."""

    def __init__(self, master, **kwargs):
        super().__init__(master=master, font=(configs.std_font, configs.small_font_size),
                         fg=configs.std_text_colour,
                         bg=configs.background_colour,
                         **kwargs)
        self.num_results: int = 0
        self.search_time: float = 0
        self._template = '{num_results} results ({search_time:.2f}s)'
        self.update()

    def update(self) -> None:
        self.configure(text=self._template.format(
            num_results=self.num_results,
            search_time=self.search_time
        ))


class ResultsFilterWidget(tk.Frame):
    """Widget to present results filtering functionality."""

    def __init__(self, master, **kwargs):
        super().__init__(master, bg=configs.background_colour, **kwargs)
        self.hidden_result_filepaths: List['str'] = []
        self._template = '{num_hidden} results hidden'
        self._btn_clear = zetools.ImageLabel(master=self, image_path='{}/{}'.format(
            configs.assets_filepath, "clear_filter.png"), img_width=25, bg=configs.background_colour, cursor="hand2")
        self._btn_clear.grid(row=0, column=0)
        self._lbl_hidden_count = tk.Label(master=self, bg=configs.background_colour,
                                          font=(configs.std_font, configs.small_font_size),
                                          fg=configs.std_text_colour)
        self._lbl_hidden_count.grid(row=0, column=1)
        self.update()

    def clear_hidden(self) -> None:
        self.hidden_result_filepaths = []

    def update(self) -> None:
        self._lbl_hidden_count.configure(text=self._template.format(num_hidden=len(self.hidden_result_filepaths)))


class View(tk.Frame):
    """Results view widget."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs, bg=configs.background_colour)
        self._current_results_page: int = 1
        self._results_pages: List[tk.Frame] = []
        # Main layout components;
        self.grid_columnconfigure(0, weight=1)
        # Results header bar;
        self._header = tk.Frame(master=self, bg=configs.background_colour)
        # self._header.columnconfigure(1, weight=1)
        self._results_nav = ResultsNavWidget(master=self._header)
        self._results_nav.grid(row=0, column=0, padx=20)
        self._results_summary = ResultsSummaryWidget(master=self._header)
        self._results_summary.grid(row=0, column=1, padx=20)
        self._results_filter = ResultsFilterWidget(master=self._header)
        self._results_filter.grid(row=0, column=2, padx=20)
        self._header.grid(row=0, column=0, sticky="EW")
        # Results pages;
        self._results_page_container = tk.Frame(master=self, bg=configs.background_colour)
        self._results_page_container.grid(row=1, column=0)

    def load_new_results(self, results: List['MarkdownFile']) -> None:
        """Publishes a list of results to the view."""
        self._clear_results()
        paged_results = self._chunk_results_list(results)
        for group in paged_results:
            page = tk.Frame(master=self._results_page_container)
            for result in group:
                r = SearchResultWidget(master=page, search_result=result)
                r.pack()
        self._results_pages[self._current_results_page - 1].pack()

    def _increment_page(self) -> None:
        if self._current_results_page < len(self._results_pages):
            self._current_results_page = self._current_results_page + 1

    def _decrement_page(self) -> None:
        if self._current_results_page > 2:
            self._current_results_page = self._current_results_page - 1

    def _clear_results(self):
        self._current_results_page = 1
        for result in self._results_page_container.winfo_children():
            result.pack_forget()

    @staticmethod
    def _chunk_results_list(results_list: List['MarkdownFile']) -> List[List['MarkdownFile']]:
        """Splits the overall results list into pages, each one a list of search results."""
        chunked_list = []
        for i in range(0, len(results_list), configs.num_results_per_page):
            chunked_list.append(results_list[i:i + configs.num_results_per_page])
        return chunked_list


class Controller:
    def __init__(self, view: 'View'):
        self._view = view
        self._hidden_results: List['MarkdownFile'] = []
