import tkinter as tk
from typing import List, TYPE_CHECKING

import zetools
from zetools import configs

if TYPE_CHECKING:
    from zetools import MarkdownFile


class SearchResult:
    """Data model of search result"""

    def __init__(self, markdown_file: 'MarkdownFile', context_start_line: int):
        self._markdown_file = markdown_file
        self._context_start_line = context_start_line

    @property
    def _context(self) -> str:
        return self._markdown_file[self._context_start_line:self._context_start_line
                                                            + configs.num_result_context_lines]


class SearchResultWidget(tk.Frame):
    """View component for a search result."""

    def __init__(self, master, search_result: 'SearchResult', **kwargs):
        super().__init__(master=master, **kwargs)
        self.search_result = search_result


class View(tk.Frame):
    """Results view widget."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs, bg=configs.background_colour)
        self.grid_columnconfigure(0, weight=1)
        # Main layout components;
        self._current_results_page: int = 1
        self._results_pages: List[tk.Frame] = []
        self._results_header = tk.Frame(master=self, bg=configs.background_colour)
        self._results_header.grid_columnconfigure(0, weight=1)
        self._results_header.grid_columnconfigure(1, weight=1)
        self._results_status = tk.Label(master=self._results_header, text="0 results (0.0s)",
                                        bg=configs.background_colour,
                                        font=(configs.std_font, configs.small_font_size),
                                        fg=configs.std_text_colour)
        self._results_status.grid(row=0, column=0, padx=20)
        self._results_page_container = tk.Frame(master=self, bg=configs.background_colour)
        self._results_header.grid(row=0, column=0, sticky="EW")
        self._results_page_container.grid(row=1, column=0)
        # Results Navbar
        self._results_nav = tk.Frame(master=self._results_header, bg=configs.background_colour)
        self._nav_to_start = zetools.ImageLabel(master=self._results_nav, image_path='{}/{}'.format(
            configs.assets_filepath, "nav_to_start.png"), img_width=20, bg=configs.background_colour)
        self._nav_to_start.grid(row=0, column=0)
        self._nav_forwards = zetools.ImageLabel(master=self._results_nav, image_path='{}/{}'.format(
            configs.assets_filepath, "nav_forwards.png"), img_width=15, bg=configs.background_colour)
        self._nav_forwards.grid(row=0, column=1)
        self._nav_status = tk.Label(master=self._results_nav, text="pg 0 of 0", bg=configs.background_colour,
                                    font=(configs.std_font, configs.small_font_size), fg=configs.std_text_colour)
        self._nav_status.grid(row=0, column=2)
        self._nav_backwards = zetools.ImageLabel(master=self._results_nav, image_path='{}/{}'.format(
            configs.assets_filepath, "nav_backwards.png"), img_width=15, bg=configs.background_colour)
        self._nav_backwards.grid(row=0, column=3)
        self._nav_to_end = zetools.ImageLabel(master=self._results_nav, image_path='{}/{}'.format(
            configs.assets_filepath, "nav_to_end.png"), img_width=20, bg=configs.background_colour)
        self._nav_to_end.grid(row=0, column=4)
        self._results_nav.grid(row=0, column=1, padx=20)

    def load_new_results(self, results: List['SearchResult']) -> None:
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
    def _chunk_results_list(results_list: List['SearchResult']) -> List[List['SearchResult']]:
        """Splits the overall results list into pages, each one a list of search results."""
        chunked_list = []
        for i in range(0, len(results_list), configs.num_results_per_page):
            chunked_list.append(results_list[i:i + configs.num_results_per_page])
        return chunked_list
