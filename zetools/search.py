import re
from typing import List, Dict, Any, TYPE_CHECKING

from ripgrepy import Ripgrepy

from . import exceptions, configs, io

if TYPE_CHECKING:
    from zetools.core import MarkdownFile

_page_template: str = '''# Zettelkasten - Advanced Search

## Search Criteria

{search_criteria}
        
---

## Search Results
{results_section}
'''
_blank_search_section = '''    includes-anywhere: []
    includes-in-title: []
    excludes-everywhere: []
    excludes-in-title: []

    - Use // to comment out groups, e.g:
        // includes-anywhere: [ignore me]
'''
_results_section = '''{search_status}

{results_list}'''
_search_status = '''Matched {num_files} file(s)'''
_result_template = '''- [{title}]({filepath})\n'''

_rgx = re.compile('(?<=\[).*?(?=\])')  # noqa - Square bracket extraction regex.


class TermsNotFoundError(exceptions.ZetoolsException):
    """Indicates a search term block was not found in the md file."""


def _format_results(results: List['MarkdownFile']) -> str:
    """Builds the results section of the page."""
    results_list = ''
    for result in results:
        results_list = results_list + _result_template.format(title=result.title, filepath=result.rel_filepath)
    return _results_section.format(search_status=_search_status.format(num_files=len(results)),
                                   results_list=results_list)


def _parse_terms(tag: str, file_lines: List[str]) -> Any:
    """Parses the terms from the specified tag."""
    # Compile regex to extract text from between square brackets;

    # Hunt through the lines until you find the file.
    for line in file_lines:
        if tag in line and '//' not in line and r'\\' not in line:  # Allows tags to be commented out.
            raw_terms = _rgx.findall(line)[0]
            terms = []
            for term in raw_terms.split(','):
                term = term.strip()
                if not term == '':
                    terms.append(term.lower())
            return terms
    raise TermsNotFoundError


def _parse_all_search_terms(file_lines: List[str]) -> Dict[str, Any]:
    """Parses the search page lines into a dictionary of all search terms."""
    return {
        'includes-anywhere': _parse_terms('includes-anywhere', file_lines),
        'includes-in-title': _parse_terms('includes-in-title', file_lines),
        'excludes-everywhere': _parse_terms('excludes-everywhere', file_lines),
        'excludes-in-title': _parse_terms('excludes-in-title', file_lines),
    }


def _get_rg(search_term: str, prev_result_paths: List[str]) -> 'Ripgrepy':
    """Factory function to instantion the ripgrep instance with the correct file/path/pattern."""
    if len(prev_result_paths) == 0:
        rg = Ripgrepy(search_term, configs.vault_filepath)
    else:
        rg = Ripgrepy(search_term, ' '.join(prev_result_paths))
    return rg


def _filter_on_includes_anywhere(search_term: str, prev_result_paths: List[str]) -> List[str]:
    """Returns a list of filepaths, representing each file which includes the search_term."""
    rg = _get_rg(search_term, prev_result_paths)
    raw_result = rg.i().g('*.md').json().run().as_dict  # noqa
    results = []
    for match in raw_result:
        match_path = match['data']['path']['text']
        if match_path not in results:
            results.append(match_path)
    return results


def _filter_on_excludes_everywhere(search_term: str, prev_result_paths: List[str]) -> List[str]:
    """Returns a list of filepaths, representing each file which does not include the search term."""
    rg = _get_rg(search_term, prev_result_paths)
    raw_result = rg.i().g('*.md').files_without_matches().run()
    filenames = raw_result.as_string.splitlines()  # noqa
    return filenames


def run_search() -> None:
    """Runs the search, based on the criteria in the search page."""
    result_paths = []
    search_page = io.read_md(r'{vault_path}\{search_page_name}'.format(
        vault_path=configs.vault_filepath,
        search_page_name=configs.search_page_filename
    ))
    # Grab the search terms;
    search_terms = _parse_all_search_terms(search_page.content_lines)

    # Filter on any 'includes-anywhere';
    search_terms['includes-anywhere'] = set(search_terms['includes-anywhere'] + search_terms['includes-in-title'])
    if len(search_terms['includes-anywhere']) > 0:
        for term in search_terms['includes-anywhere']:
            result_paths = _filter_on_includes_anywhere(term, result_paths)

    # Filter on 'excludes-everywhere'
    search_terms['excludes-everywhere'] = set(search_terms['excludes-everywhere'] + search_terms['excludes-in-title'])
    if len(search_terms['excludes-everywhere']) > 0:
        for term in search_terms['excludes-everywhere']:
            result_paths = _filter_on_excludes_everywhere(term, result_paths)

    # Now read the files in, we need to inspect their titles;
    files = []
    for filepath in result_paths:
        files.append(io.read_md(filepath))

    # Now filter files based on include and exclude;
    matches = []  # final matches
    for file in files:
        title_words = file.title.lower().split()
        if any(x in search_terms['excludes-in-title'] for x in title_words):
            continue
        if len(search_terms['includes-in-title']) > 0 and \
                not any(x in search_terms['includes-in-title'] for x in title_words):
            continue
        matches.append(file)

    # Now update and write the search page;
    search_page.set_section(1, 'Search Results', _format_results(matches))
    io.write_md(search_page)
