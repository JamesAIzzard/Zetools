import tkinter as tk
from typing import List, TYPE_CHECKING

from pyperclip import copy

import zetools
from zetools import configs

if TYPE_CHECKING:
    from zetools import MarkdownFile


class SearchResultWidget(tk.Frame):
    """View component for a search result."""

    def __init__(self, master, search_result: 'MarkdownFile', **kwargs):
        super().__init__(master=master, bg=configs.background_colour, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        self.search_result = search_result
        # Hide result icon;
        self._hide_icon = zetools.ImageLabel(master=self, image_path='{path}/{name}'.format(
            path=configs.assets_filepath,
            name="toggle_visibility.png"
        ), img_width=15, bg=zetools.configs.background_colour, cursor="hand2")
        self._hide_icon.bind("<Button-1>", lambda _: self.event_generate("<<Hide-Result-Clicked>>"))
        self._hide_icon.grid(row=0, column=0)
        # Result title;
        if search_result.has_next_tag:
            title_colour = configs.emph_text_colour
        else:
            title_colour = configs.std_text_colour
        self._lbl_title = tk.Label(master=self, text=self.truncate_text(self.search_result.title),
                                   bg=configs.background_colour,
                                   font=(configs.std_font, configs.small_font_size),
                                   fg=title_colour, cursor="hand2")
        self._lbl_title.bind("<Button-1>", lambda _: self.event_generate("<<Result-Title-Clicked>>"))
        self._lbl_title.grid(row=0, column=1, sticky="W", padx=10)
        # Result filename;
        self._lbl_filename = tk.Label(master=self, text=self.search_result.filename_with_ext,
                                      bg=configs.background_colour,
                                      fg=configs.emph_text_colour, font=(configs.std_font, configs.small_font_size),
                                      cursor="hand2")
        self._lbl_filename.bind("<Button-1>", lambda _: self.event_generate("<<Result-Filename-Clicked>>"))
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
        # Nav to first page;
        self._nav_to_start = zetools.ImageLabel(master=self, image_path='{}/{}'.format(
            configs.assets_filepath, "nav_to_start.png"), img_width=20, bg=configs.background_colour, cursor="hand2")
        self._nav_to_start.bind("<Button-1>", lambda _: self.event_generate("<<Results-Page-First>>"))
        self._nav_to_start.grid(row=0, column=0)
        # Nav backwards;
        self._nav_backwards = zetools.ImageLabel(master=self, image_path='{}/{}'.format(
            configs.assets_filepath, "nav_backwards.png"), img_width=15, bg=configs.background_colour, cursor="hand2")
        self._nav_backwards.bind("<Button-1>", lambda _: self.event_generate("<<Results-Page-Down>>"))
        self._nav_backwards.grid(row=0, column=1)
        # Nav status;
        self._nav_status = tk.Label(master=self, text="pg 0 of 0", bg=configs.background_colour,
                                    font=(configs.std_font, configs.small_font_size), fg=configs.std_text_colour)
        self._nav_status.grid(row=0, column=2)
        # Nav forwards;
        self._nav_forwards = zetools.ImageLabel(master=self, image_path='{}/{}'.format(
            configs.assets_filepath, "nav_forwards.png"), img_width=15, bg=configs.background_colour, cursor="hand2")
        self._nav_forwards.bind("<Button-1>", lambda _: self.event_generate("<<Results-Page-Up>>"))
        self._nav_forwards.grid(row=0, column=3)
        # Nav to last page'
        self._nav_to_end = zetools.ImageLabel(master=self, image_path='{}/{}'.format(
            configs.assets_filepath, "nav_to_end.png"), img_width=20, bg=configs.background_colour, cursor="hand2")
        self._nav_to_end.bind("<Button-1>", lambda _: self.event_generate("<<Results-Page-Last>>"))
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
        self._template = '{num_results} results ({search_time:.4f}s)'
        self.set_summary(0, 0.00)

    def set_summary(self, num_results: int, search_time: float) -> None:
        self.configure(text=self._template.format(
            num_results=num_results,
            search_time=search_time
        ))


class ResultsFilterWidget(tk.Frame):
    """Widget to present results filtering functionality."""

    def __init__(self, master, **kwargs):
        super().__init__(master, bg=configs.background_colour, **kwargs)
        self._template = '{num_hidden} results hidden'

        # Clear results button;
        self._btn_clear = zetools.ImageLabel(master=self, image_path='{}/{}'.format(
            configs.assets_filepath, "clear_filter.png"), img_width=20, bg=configs.background_colour, cursor="hand2")
        self._btn_clear.bind("<Button-1>", lambda _: self.event_generate("<<Clear-Hidden-Results>>"))
        self._btn_clear.grid(row=0, column=0)
        # Hidden results summary readout;
        self._lbl_hidden_count = tk.Label(master=self, bg=configs.background_colour,
                                          font=(configs.std_font, configs.small_font_size),
                                          fg=configs.std_text_colour)
        self._lbl_hidden_count.grid(row=0, column=1)

        self.set_filter_num(0)

    def set_filter_num(self, num_hidden: int) -> None:
        self._lbl_hidden_count.configure(text=self._template.format(num_hidden=num_hidden))


class View(tk.Frame):
    """Results search_view widget."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs, bg=configs.background_colour)
        # Main layout components;
        self.grid_columnconfigure(0, weight=1)
        # Results header bar;
        self._header = tk.Frame(master=self, bg=configs.background_colour)
        self.results_nav = ResultsNavWidget(master=self._header)
        self.results_nav.grid(row=0, column=0, padx=(20, 0))
        self.results_summary = ResultsSummaryWidget(master=self._header)
        self.results_summary.grid(row=0, column=1, padx=(20, 0))
        self.results_filter = ResultsFilterWidget(master=self._header)
        self.results_filter.grid(row=0, column=2, padx=(20, 0))
        self._clear_results = zetools.ImageLabel(master=self._header, image_path='{}/{}'.format(
            configs.assets_filepath, "bin.png"), img_width=20, bg=configs.background_colour, cursor="hand2")
        self._clear_results.bind("<Button-1>", lambda _: self.event_generate("<<Clear-Search>>"))
        self._clear_results.grid(row=0, column=3, padx=(20, 0))
        self._header.grid(row=0, column=0)
        # Results pages;
        self._results_container = tk.Frame(master=self, bg=configs.background_colour)
        self._results_container.grid_columnconfigure(0, weight=1)
        self._results_container.grid(row=1, column=0, pady=(20, 0), padx=5, sticky="EW")

    def clear_results(self, ):
        """Empties the result page container;"""
        for result in self._results_container.winfo_children():
            result.grid_forget()

    def show_results(self, results: List['MarkdownFile']) -> None:
        """Publishes the list of results to the view."""
        self.clear_results()
        if len(results):
            for n, result in enumerate(results, start=0):
                r = SearchResultWidget(master=self._results_container, search_result=result)
                r.grid(row=n, column=0, sticky="EW")
        else:
            lbl_no_results = tk.Label(master=self._results_container, text="No Results", bg=configs.background_colour,
                                      font=(configs.std_font, configs.small_font_size),
                                      fg=configs.std_text_colour)
            lbl_no_results.grid(row=0, column=0, sticky="EW")

    def show_search_spinner(self) -> None:
        """Starts the results spinner."""
        self.clear_results()
        lbl_spinner = tk.Label(master=self._results_container, text="Loading...", bg=configs.background_colour,
                               font=(configs.std_font, configs.small_font_size),
                               fg=configs.std_text_colour)
        lbl_spinner.grid(row=0, column=0, sticky="EW")
        self.update()


class Controller:
    def __init__(self, view: 'View'):
        self._view = view
        self._current_page_num: int = 1
        self._hidden_result_filenames: List[str] = []
        self._all_results: List['MarkdownFile'] = []
        self._view.bind_all("<<Results-Page-First>>", self._on_page_results_to_start)
        self._view.bind_all("<<Results-Page-Down>>", self._on_page_results_down)
        self._view.bind_all("<<Results-Page-Up>>", self._on_page_results_up)
        self._view.bind_all("<<Results-Page-Last>>", self._on_page_results_to_end)
        self._view.bind_all("<<Hide-Result-Clicked>>", self._on_hide_result_clicked)
        self._view.bind_all("<<Clear-Hidden-Results>>", self._on_clear_hidden_results)
        self._view.bind_all("<<Result-Title-Clicked>>", self._on_result_title_clicked)
        self._view.bind_all("<<Result-Filename-Clicked>>", self._on_result_filename_clicked)
        self._view.bind_all("<<Clear-Search>>", self._on_clear_search, add='+')

    @property
    def _current_page_results(self) -> List['MarkdownFile']:
        """Returns the list of markdown files shown on the current page."""
        if not self._has_results:
            return []
        if self._current_page_num > self._num_pages:
            self._current_page_num = self._num_pages
        return self._results_pages[self._current_page_num - 1]

    @property
    def _num_pages(self) -> int:
        return len(self._results_pages)

    @property
    def _num_results(self) -> int:
        return len(self._all_results)

    @property
    def _results_pages(self) -> List[List['MarkdownFile']]:
        """Returns a list of lists of markdown files, representing the results pages."""
        return self._chunk_results_list(self._visible_results)

    @property
    def _visible_results(self) -> List['MarkdownFile']:
        """Returns a list of markdown files which are not marked as hidden."""
        visible_results = []
        for result in self._all_results:
            if result.filename_without_ext not in self._hidden_result_filenames:
                visible_results.append(result)
        return visible_results

    @property
    def _num_hidden_results(self) -> int:
        """Returns the number of currently hidden results."""
        return len(self._hidden_result_filenames)

    @property
    def _has_results(self) -> bool:
        """Returns True/False to indicate if there are any results loaded."""
        return self._num_pages > 0

    @staticmethod
    def _chunk_results_list(results_list: List['MarkdownFile']) -> List[List['MarkdownFile']]:
        """Splits the overall results list into pages, each one a list of search results."""
        chunked_list = []
        for i in range(0, len(results_list), configs.num_results_per_page):
            chunked_list.append(results_list[i:i + configs.num_results_per_page])
        return chunked_list

    def load_results(self, results: List['MarkdownFile']) -> None:
        """Presents a fresh set of results."""
        self._all_results = results
        if len(results):
            self._current_page_num = 1
        else:
            self._current_page_num = 0
        self._view.results_nav.set_nav_status(self._num_pages, self._current_page_num)
        self._view.show_results(self._current_page_results)

    def set_summary(self, num_results: int, search_time: float) -> None:
        self._view.results_summary.set_summary(num_results, search_time)

    def show_search_spinner(self) -> None:
        self._view.show_search_spinner()

    def _update_results_nav(self) -> None:
        """Updates the figures in the results nav bar."""
        self._view.results_nav.set_nav_status(self._num_pages, self._current_page_num)

    def _on_clear_search(self, _) -> None:
        """Handler for <<Clear-Search>>"""
        self._all_results = []
        self._current_page_num = 0
        self._hidden_result_filenames = []
        self._update_results_nav()
        self._view.results_summary.set_summary(0, 0.00)
        self._view.show_results([])

    def _on_page_results_up(self, _) -> None:
        """Handler for <<Results-Page-Up>>"""
        if self._current_page_num < self._num_pages:
            self._current_page_num = self._current_page_num + 1
            self._update_results_nav()
            self._view.show_results(self._current_page_results)

    def _on_page_results_down(self, _) -> None:
        """Handler for <<Results-Page-Down>>"""
        if self._current_page_num > 1:
            self._current_page_num = self._current_page_num - 1
            self._update_results_nav()
            self._view.show_results(self._current_page_results)

    def _on_page_results_to_end(self, _) -> None:
        """Handler for <<Results-Page-Last>>"""
        if self._has_results:
            self._current_page_num = self._num_pages
            self._update_results_nav()
            self._view.show_results(self._current_page_results)

    def _on_page_results_to_start(self, _) -> None:
        """Handler for <<Results-Page-First>>"""
        if self._has_results:
            self._current_page_num = 1
            self._update_results_nav()
            self._view.show_results(self._current_page_results)

    def _on_clear_hidden_results(self, _) -> None:
        """Handler for <<Clear-Hidden-Results>>"""
        self._hidden_result_filenames = []
        if self._current_page_num == 0:
            self._current_page_num = 1
        self._update_results_nav()
        self._view.results_filter.set_filter_num(self._num_hidden_results)
        self._view.show_results(self._current_page_results)

    def _on_hide_result_clicked(self, event) -> None:
        """Handler for <<Hide-Result-Clicked>>"""
        self._hidden_result_filenames.append(event.widget.search_result.filename_without_ext)
        if self._current_page_num > self._num_pages:
            self._current_page_num = self._num_pages
        self._update_results_nav()
        self._view.results_filter.set_filter_num(self._num_hidden_results)
        self._view.show_results(self._current_page_results)

    @staticmethod
    def _on_result_title_clicked(event) -> None:
        """Handler for <<Result-Title-Clicked>>"""
        zetools.repository.open_md(md_file=event.widget.search_result)

    @staticmethod
    def _on_result_filename_clicked(event) -> None:
        """Handler for <<Result-Filename-Clicked>>"""
        copy(event.widget.search_result.filename_with_ext)
