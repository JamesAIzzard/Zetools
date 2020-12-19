import re
from typing import List

from . import io, exceptions


class TermsNotFoundError(exceptions.ZetoolsException):
    """Indicates a search term block was not found in the md file."""


search_file_name: str = 'search.md'

page_template: str = '''# Zettelkasten - Advanced Search

## Search Criteria

    includes-anywhere: []
    includes-in-title: []
    excludes-everywhere: []
    excludes-in-title: []
    max-results-num: []

---

## Search Results
Found results in {num_files} file(s)

{results_printout}
'''

result_template: str = '''- [{title}]({filename}.md)'''


def parse_terms(tag: str, file_lines: List[str]) -> List[str]:
    """Parses the terms from the specified tag."""
    # Compile regex to extract text from between square brackets;
    rgx = re.compile('\[(.*?)\]')
    # Hunt through the lines until you find the file.
    for line in file_lines:
        if tag in line:
            raw_terms = rgx.match(line)
            terms = line.split(',')
            return terms
    raise TermsNotFoundError


def parse_includes_anywhere(file_lines: List[str]) -> List[str]:
    """Parses the includes-anywhere terms."""
    return parse_terms('includes-anywhere', file_lines)


def parse_includes_in_title(file_lines: List[str]) -> List[str]:
    """parses the includes-in-title terms."""
    return parse_terms('includes-in-title', file_lines)


def parse_excludes_everywhere(file_lines: List[str]) -> List[str]:
    """parses the excludes-everywhere terms."""
    return parse_terms('excludes-everywhere', file_lines)


def parse_excludes_in_title(file_lines: List[str]) -> List[str]:
    """parses the excludes-in-title terms."""
    return parse_terms('excludes-in-title', file_lines)
