from typing import List, TypedDict, TYPE_CHECKING

from ripgrepy import Ripgrepy

import zetools
from zetools import repository

if TYPE_CHECKING:
    from zetools import MarkdownFile


class SearchDef(TypedDict):
    """Container for search definition data."""
    inc_all: List[str]
    inc_title: List[str]
    ex_all: List[str]
    ex_title: List[str]
    case_match: bool


def _get_rg(search_term: str, prev_result_paths: List[str]) -> 'Ripgrepy':
    """Factory function to instantion the ripgrep instance with the correct file/path/pattern."""
    if len(prev_result_paths) == 0:
        rg = Ripgrepy(search_term, zetools.configs.vault_filepath)
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


def search(search_def: 'SearchDef') -> List['MarkdownFile']:
    """Returns a list of MarkdownFiles which match the search defined in the search criteria dictionary."""
    result_paths = []

    # Filter on any 'includes-anywhere';
    # Merge any inc-title terms into the overall list;
    search_def['inc_all'] = list(set(search_def['inc_all'] + search_def['inc_title']))
    if len(search_def['inc_all']) > 0:
        for term in search_def['inc_all']:
            result_paths = _filter_on_includes_anywhere(term, result_paths)

    # Filter on 'excludes-everywhere'
    search_def['ex_all'] = list(
        set(search_def['ex_all'] + search_def['ex_title']))
    if len(search_def['ex_all']) > 0:
        for term in search_def['ex_all']:
            result_paths = _filter_on_excludes_everywhere(term, result_paths)

    # Now read the files in, we need to inspect their titles;
    files = []
    for filepath in result_paths:
        files.append(repository.read_md(filepath))

    # Now filter files based on include and exclude;
    matches = []  # final matches
    for file in files:
        title_words = file.title.lower().split()
        if any(x in search_def['ex_title'] for x in title_words):
            continue
        if len(search_def['inc_title']) > 0 and \
                not any(x in search_def['inc_title'] for x in title_words):
            continue
        matches.append(file)

    return files
