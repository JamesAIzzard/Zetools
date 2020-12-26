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
        # self._window.geometry("800x500")
        self._window.iconbitmap(configs.ico_filepath)
        # Build the components;
        self._main_logo = zetools.ImageLabel(master=self._window, image_path=configs.brain_image_path, img_width=300,
                                             bg=zetools.configs.background_colour)
        self._search_view = search.SearchView(master=self._window)
        self._search_controller = search.SearchController(search_view=self._search_view)
        # Assemble the UI;
        self._window.grid_columnconfigure(0, weight=1)
        self._main_logo.grid(row=0, column=0)
        self._search_view.grid(row=1, column=0, padx=50)

    def run(self):
        """Start the main application loop."""
        self._window.mainloop()
