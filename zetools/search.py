from typing import List, Dict, TYPE_CHECKING

from ripgrepy import Ripgrepy

from . import configs, io

if TYPE_CHECKING:
    from zetools.core import MarkdownFile

_results_table_header = '''|Latest search matched {num_results} file(s):|
|---|
'''
_result_template = '''|[{title}]({filepath})|\n'''


def _process_raw_search_terms(raw_search_terms: Dict[str, str]) -> Dict[str, List[str]]:
    search_terms = {}
    for key, value in raw_search_terms.items():
        terms = value.split(',')
        search_terms[key] = []
        for term in terms:
            if not term.strip() == '':
                search_terms[key].append(term.strip().lower())

    return search_terms


def _generate_results_section(results: List['MarkdownFile']) -> str:
    """Builds the results section of the page."""
    results_section = _results_table_header.format(num_results=len(results))
    for result in results:
        results_section = results_section + _result_template.format(title=result.title, filepath=result.rel_filepath)
    return results_section


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


def run_search(raw_search_terms: Dict[str, str]) -> None:
    """Runs the search, based on the criteria in the search page."""
    result_paths = []
    main_page = io.read_md(r'{vault_path}\{main_page_name}'.format(
        vault_path=configs.vault_filepath,
        main_page_name=configs.main_page_filename
    ))
    # Process the search terms;
    search_terms = _process_raw_search_terms(raw_search_terms)

    # Filter on any 'includes-anywhere';
    search_terms['includes_anywhere'] = list(set(search_terms['includes_anywhere'] + search_terms['includes_in_title']))
    if len(search_terms['includes_anywhere']) > 0:
        for term in search_terms['includes_anywhere']:
            result_paths = _filter_on_includes_anywhere(term, result_paths)

    # Filter on 'excludes-everywhere'
    search_terms['excludes_everywhere'] = list(
        set(search_terms['excludes_everywhere'] + search_terms['excludes_in_title']))
    if len(search_terms['excludes_everywhere']) > 0:
        for term in search_terms['excludes_everywhere']:
            result_paths = _filter_on_excludes_everywhere(term, result_paths)

    # Now read the files in, we need to inspect their titles;
    files = []
    for filepath in result_paths:
        files.append(io.read_md(filepath))

    # Now filter files based on include and exclude;
    matches = []  # final matches
    for file in files:
        title_words = file.title.lower().split()
        if any(x in search_terms['excludes_in_title'] for x in title_words):
            continue
        if len(search_terms['includes_in_title']) > 0 and \
                not any(x in search_terms['includes_in_title'] for x in title_words):
            continue
        matches.append(file)

    # Now update and write the search page;
    main_page.set_section(1, 'Search Results', _generate_results_section(matches))
    io.write_md(main_page)
