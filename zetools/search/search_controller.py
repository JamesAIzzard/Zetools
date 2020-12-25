from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from zetools.search import SearchDef
    from zetools.markdown_file import MarkdownFile


class SearchController:
    def __init__(self):
        pass

    @staticmethod
    def on_search(search_definition: 'SearchDef') -> List['MarkdownFile']:
        print(search_definition)
