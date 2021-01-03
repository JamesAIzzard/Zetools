import tkinter as tk
from typing import List, TYPE_CHECKING

import zetools
from zetools import configs

if TYPE_CHECKING:
    from zetools import MarkdownFile


class SearchResultWidget(tk.Frame):
    """View component for a search result."""

    def __init__(self, master, search_result: 'MarkdownFile', **kwargs):
        super().__init__(master=master, bg=configs.background_colour, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        self._search_result = search_result
        self._hide_icon = zetools.ImageLabel(master=self, image_path='{path}/{name}'.format(
            path=configs.assets_filepath,
            name="toggle_visibility.png"
        ), img_width=15, bg=zetools.configs.background_colour, cursor="hand2")
        self._hide_icon.grid(row=0, column=0)
        self._lbl_title = tk.Label(master=self, text=self.truncate_text(self._search_result.title),
                                   bg=configs.background_colour,
                                   font=(configs.std_font, configs.small_font_size),
                                   fg=configs.std_text_colour, cursor="hand2")
        self._lbl_title.bind("<<Button-1>>", self.event_generate("<<Result-Title-Click>>"))
        self._lbl_title.grid(row=0, column=1, sticky="W", padx=10)
        self._lbl_filename = tk.Label(master=self, text=self._search_result.filename_with_ext,
                                      bg=configs.background_colour,
                                      fg=configs.emph_text_colour, font=(configs.std_font, configs.small_font_size),
                                      cursor="hand2")
        self._lbl_filename.bind("<<Button-1>>", self.event_generate("<<Result-Filename-Clicked>>"))
        self._lbl_filename.grid(row=0, column=2)

    @staticmethod
    def truncate_text(text: str) -> str:
        """Trucates titles beyond a set length."""
        return (text[:configs.result_title_max_chars] + '...') if len(
            text) > configs.result_title_max_chars else text


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

    def set_nav_status(self, total_pages: int, current_page: int) -> None:
        self._nav_status.configure(text="pg {} of {}".format(current_page, total_pages))


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
            configs.assets_filepath, "clear_filter.png"), img_width=20, bg=configs.background_colour, cursor="hand2")
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
    """Results search_view widget."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs, bg=configs.background_colour)
        self._current_results_page: int = 1
        self._results: List['MarkdownFile'] = []
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
        self._header.grid(row=0, column=0)
        # Results pages;
        self._results_page_container = tk.Frame(master=self, bg=configs.background_colour)
        self._results_page_container.grid_columnconfigure(0, weight=1)
        self._results_page_container.grid(row=1, column=0, pady=(20, 0), padx=5, sticky="EW")

    def load_new_results(self, results: List['MarkdownFile']) -> None:
        """Publishes a list of results to the search_view."""
        self._clear_results()
        paged_results = self._chunk_results_list(results)
        for group in paged_results:
            page = tk.Frame(master=self._results_page_container, bg=configs.background_colour)
            page.grid_columnconfigure(0, weight=1)
            for n, result in enumerate(group, start=0):
                r = SearchResultWidget(master=page, search_result=result)
                r.grid(row=n, column=0, sticky="EW")
            self._results_pages.append(page)
        self._results_pages[self._current_results_page - 1].grid(row=0, column=0, sticky="EW")
        self._results_nav.set_nav_status(len(paged_results), self._current_results_page)

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
