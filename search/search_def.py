from typing import List, TypedDict


class SearchDef(TypedDict):
    """Container for search definition data."""
    inc_all: List[str]
    inc_title: List[str]
    ex_all: List[str]
    ex_title: List[str]
    case_match: bool
