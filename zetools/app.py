import tkinter as tk

from zetools import configs, top_menu, brain_widget


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

        self._event_register = {}

        # Init the components & controllers;
        self._top_menu_view = top_menu.View(root=self._window)
        self._top_menu_controller = top_menu.Controller(root=self._window, view=self._top_menu_view)
        self._brain_widget_view = brain_widget.View(master=self._window)
        self._brain_widget_controller = brain_widget.Controller(view=self._brain_widget_view)
        # self._note_search_bar = zetools.NoteSearchBar(root=self._window)
        # self._note_search_bar_controller = zetools.NoteSearchBarController(view=self._note_search_bar)
        # self._backlog_search_bar = zetools.BacklogSearchBar(root=self._window)
        # self._backlog_search_controller = zetools.BacklogSearchController(view=self._backlog_search_bar)
        # self._results_pane = zetools.ResultsPane(root=self._window)
        # self._results_pane_controller = zetools.ResultsPaneController(view=self._results_pane)
        # self._status_footer_bar = zetools.StatusFooterBar(root=self._window)
        # self._status_footer_bar_controller = zetools.StatusFooterBarController(view=self._status_footer_bar)
        # Grid them into the window;
        self._grid_views()

    def _grid_views(self):
        """Handles gridding of view components as per application state."""
        self._window.config(menu=self._top_menu_view)
        self._window.grid_columnconfigure(0, weight=1)
        self._brain_widget_view.grid(row=0, column=0, pady=15)
        # if self._note_search_bar_controller.note_search_enabled:
        #     self._note_search_bar.grid(row=1, column=0, padx=50)
        # elif self._backlog_search_bar_controller.backlog_search_enabled:
        #     self._backlog_search_bar.grid(row=1, column=0, padx=50)
        # self._results_pane.grid(row=2, column=0, pady=20)
        # self._status_footer.grid(row=3, column=0, sticky="nesw", padx=10, pady=10)

    def run(self):
        """Start the main application loop."""
        self._brain_widget_view.start()
        # self._status_footer.start()
        self._window.mainloop()
