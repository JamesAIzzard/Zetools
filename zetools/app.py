import tkinter as tk

import zetools
from zetools import configs, search


class App:
    """Zetools top-level application class."""

    def __init__(self):
        # Build the main _window;
        self._window = tk.Tk()
        self._window.configure(background=configs.background_colour)
        self._window.title("Zetools")
        self._window.iconbitmap('{path}/{name}'.format(
            path=configs.assets_filepath,
            name="brain_icon.ico"
        ))
        # Build the components;
        self._top_menu = zetools.TopMenu(master=self._window)
        self._window.config(menu=self._top_menu)
        self._brain_ids = zetools.BrainIDs(master=self._window)
        self._search_view = search.SearchView(master=self._window)
        self._search_controller = search.SearchController(search_view=self._search_view)
        # Assemble the UI;
        self._window.grid_columnconfigure(0, weight=1)
        # self._main_logo.grid(row=0, column=0)
        self._brain_ids.grid(row=0, column=0, pady=15)
        self._search_view.grid(row=1, column=0, padx=50)

    def run(self):
        """Start the main application loop."""
        self._brain_ids.start()
        self._window.mainloop()
