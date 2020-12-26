from typing import TYPE_CHECKING

from zetools import ScrollFrame, search, configs

if TYPE_CHECKING:
    from zetools import MarkdownFile


class SearchResultsView(ScrollFrame):
    """Scrollable table-like view to show search results."""

    def __init__(self, master, **kwargs):
        super().__init__(master=master, bg=configs.background_colour, **kwargs)
        self.scrollable_frame.configure(bg=configs.background_colour)

    def add_result(self, markdown_file: 'MarkdownFile') -> None:
        """Creates and inserts a result for a markdown file."""
        r = search.SearchResult(master=self.scrollable_frame, markdown_file=markdown_file)
        r.pack()

    def clear_results(self) -> None:
        """Removes all results from the frame."""
        for result in self.scrollable_frame.winfo_children():
            result.destroy()
