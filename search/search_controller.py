from typing import TYPE_CHECKING

from zetools import search, repository, configs

if TYPE_CHECKING:
    from zetools.search import SearchView


class SearchController:
    def __init__(self, search_view: 'SearchView'):
        self._view = search_view
        self._view.bind('<<Search>>', self._on_search)

    def _on_search(self, event) -> None:
        """Handler for search event."""
        results = search.search(self._view.get())
        results_page = repository.read_md(configs.main_page_filepath)
        search.insert_markdown_results_section(results, results_page)
        repository.write_md(results_page)
        self._view.display_results(results)
