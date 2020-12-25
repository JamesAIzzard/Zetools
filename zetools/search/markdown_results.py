from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from zetools import MarkdownFile

_results_table_header = '''|Latest search matched {num_results} file(s):|
|---|
'''
_result_template = '''|[{section_title}](files\\{filepath})|\n'''


def insert_results_section(results: List['MarkdownFile'], results_page: 'MarkdownFile') -> 'MarkdownFile':
    """Builds the results section of the page."""
    results_section = _results_table_header.format(num_results=len(results))
    for result in results:
        results_section = results_section + _result_template.format(title=result.title, filepath=result.rel_filepath)
    results_page.set_section(1, 'Search Results', results_section)
    return results_page
