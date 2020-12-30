import tkinter as tk
from typing import TYPE_CHECKING

from zetools import ScrollFrame, search, configs

if TYPE_CHECKING:
    from zetools import MarkdownFile


class ResultsView(tk.Frame):
    """Widget to display search results"""

    def __init__(self, master, **kwargs):
        super().__init__(master=master, bg=configs.background_colour, **kwargs)
        self._results_summary = tk.Label(master=self, bg=configs.background_colour)
        self._results_list = ScrollFrame(master=self, bg=configs.background_colour, width=700,
                                         height=configs.results_scroll_view_height)
        self._results_list.scrollable_frame.configure(bg=configs.background_colour)

    def update_search_summary(self, search_duration: float, num_results: int):
        _template = '''Found {num_results} result(s) in {search_duration}s'''
        self._results_summary.configure(text=_template.format(
            num_results=num_results,
            search_duration=search_duration
        ))

    def add_result(self, markdown_file: 'MarkdownFile') -> None:
        """Creates and inserts a result for a markdown file."""
        r = search.SearchResult(master=self._results_list.scrollable_frame, markdown_file=markdown_file)
        r.pack()

    def clear_results(self) -> None:
        """Removes all results from the frame."""
        for result in self._results_list.scrollable_frame.winfo_children():
            result.destroy()
