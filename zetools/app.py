import tkinter as tk

from zetools import configs, top_menu_widget, zetool_widget, search_widget, results_widget, app_footer_bar


class App:
    """Zetools top-level application class."""

    def __init__(self):
        # Build the main _window;
        self._window = tk.Tk()
        self._window.configure(background=configs.background_colour)
        self._window.title("Zetools")
        self._window.minsize(configs.window_width, configs.window_height)
        self._window.iconbitmap('{path}/{name}'.format(
            path=configs.assets_filepath,
            name="favicon.ico"
        ))

        # Init the components & controllers;
        self._top_menu_view = top_menu_widget.View(root=self._window)
        self._top_menu_controller = top_menu_widget.Controller(root=self._window, view=self._top_menu_view)
        self._brain_widget_view = zetool_widget.View(master=self._window)
        self._brain_widget_controller = zetool_widget.Controller(view=self._brain_widget_view)
        self._results_widget_view = results_widget.View(master=self._window, pady=20, padx=5)
        self._results_widget_controller = results_widget.Controller(view=self._results_widget_view)
        self._search_widget_view = search_widget.View(master=self._window)
        self._search_widget_controller = search_widget.Controller(
            search_view=self._search_widget_view,
            results_widget_controller=self._results_widget_controller
        )
        self._status_footer_bar = app_footer_bar.View(master=self._window)
        # Bind global enter to search;
        self._window.bind("<Return>", lambda _: self._window.event_generate("<<Search>>"))
        # Grid them into the window;
        self._grid_views()

    def _grid_views(self):
        """Handles gridding of search_view components as per application state."""
        self._window.config(menu=self._top_menu_view)
        self._window.grid_columnconfigure(0, weight=1)
        self._brain_widget_view.grid(row=0, column=0, pady=15)
        self._search_widget_view.grid(row=1, column=0)
        self._window.grid_rowconfigure(2, weight=1)
        self._results_widget_view.grid(row=2, column=0, sticky="NSEW")
        self._status_footer_bar.grid(row=3, column=0, sticky="nesw", padx=10, pady=10)

    def run(self):
        """Start the main application loop."""
        self._brain_widget_view.start()
        self._status_footer_bar.start()
        self._window.mainloop()
