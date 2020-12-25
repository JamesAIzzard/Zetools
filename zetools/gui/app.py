import zetools
from zetools.gui import ImageWidget, SearchWidget


class App:
    """Zetools top-level application class."""
    def __init__(self, master):
        # Centralise;
        # master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        # Brain image;
        icon = ImageWidget(master, image_path="zetools/gui/brain.png", width=300,
                           bg=zetools.gui.configs.background_colour)
        icon.grid(row=0, column=0)
        # Search widget;
        search_widget = SearchWidget(master, on_search=zetools.search.run_search)
        search_widget.grid(row=1, column=0)
