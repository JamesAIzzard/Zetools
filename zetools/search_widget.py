import tkinter as tk

import zetools
from zetools import configs


class AdvSearchField(tk.Frame):
    """Advanced search field widget"""

    def __init__(self, master, label_text: str, **kwargs):
        super().__init__(master=master, bg=configs.background_colour, **kwargs)
        self._field = tk.Entry(master=self, bg=configs.entry_background_colour,
                               fg=configs.emph_text_colour,
                               font=(configs.std_font, configs.std_font_size),
                               width=40, highlightthickness=1, relief=tk.SUNKEN,
                               highlightbackground=configs.entry_background_colour,
                               highlightcolor=configs.emph_text_colour)
        self._label = tk.Label(master=self, bg=configs.background_colour,
                               fg=configs.std_text_colour, width=10,
                               font=(configs.std_font, configs.std_font_size),
                               anchor=tk.E, text=label_text)
        self._label.grid(row=0, column=0, padx=7)
        self._field.grid(row=0, column=1)


class View(tk.Frame):
    """General search widget."""

    def __init__(self, master, **kwargs):
        super().__init__(master=master, bg=configs.background_colour, **kwargs)
        self._backlog_view_enabled = False
        self._advanced_search_enabled = False
        self._btn_backlog = zetools.ImageLabel(master=self, image_path='{path}/{name}'.format(
            path=configs.assets_filepath,
            name="backlog_button.png"
        ), img_width=26, bg=zetools.configs.background_colour, cursor="hand2")
        self._btn_backlog.bind("<Button-1>", self._toggle_backlog_view)
        self._btn_advanced_search = zetools.ImageLabel(master=self, image_path='{path}/{name}'.format(
            path=configs.assets_filepath,
            name="expand_button.png"
        ), img_width=30, bg=zetools.configs.background_colour, cursor="hand2")
        self._btn_advanced_search.bind("<Button-1>", self._toggle_adv_fields)
        self._lbl_project_prefix = tk.Label(master=self, text=" #project- ", bg=configs.background_colour,
                                            fg=configs.std_text_colour, relief=tk.SUNKEN,
                                            font=(configs.std_font, configs.std_font_size))
        self._in_title_field = AdvSearchField(self, label_text="in title:")
        self._not_in_title_field = AdvSearchField(self, label_text="not in title:")
        self._nowhere_field = AdvSearchField(self, label_text="nowhere:")
        self._btn_search = zetools.ImageLabel(master=self, image_path='{path}/{name}'.format(
            path=configs.assets_filepath,
            name="search.png"
        ), img_width=30, bg=zetools.configs.background_colour, cursor="hand2")
        self._txt_search = tk.Entry(master=self, bg=configs.entry_background_colour,
                                    fg=configs.emph_text_colour,
                                    width=45, highlightthickness=1,
                                    relief=tk.SUNKEN, highlightbackground=configs.entry_background_colour,
                                    highlightcolor=configs.emph_text_colour,
                                    font=(configs.std_font, configs.std_font_size))
        self._grid_views()

    def _toggle_backlog_view(self, _) -> None:
        self._backlog_view_enabled = not self._backlog_view_enabled
        self._clear_views()
        self._grid_views()

    def _toggle_adv_fields(self, _) -> None:
        self._advanced_search_enabled = not self._advanced_search_enabled
        self._clear_views()
        self._grid_views()

    def _grid_std_search(self) -> None:
        """Adds the standard search components to the UI."""
        self._btn_backlog.grid(row=0, column=0)
        self._btn_advanced_search.grid(row=0, column=1, padx=3)
        self._txt_search.configure(width=45)
        self._txt_search.grid(row=0, column=2, columnspan=2, padx=3)
        self._btn_search.grid(row=0, column=4)

    def _grid_adv_search_fields(self) -> None:
        """Adds the advanced fields to the UI."""
        self._in_title_field.grid(row=1, column=0, columnspan=4, padx=1)
        self._not_in_title_field.grid(row=2, column=0, columnspan=4, padx=1)
        self._nowhere_field.grid(row=3, column=0, columnspan=4, padx=1)

    def _clear_views(self) -> None:
        """Clears all child widgets."""
        for result in self.winfo_children():
            result.grid_forget()

    def _grid_views(self) -> None:
        """Assembles the views."""
        if self._backlog_view_enabled:
            self._btn_backlog.grid(row=0, column=0, padx=3)
            self._lbl_project_prefix.grid(row=0, column=1, columnspan=2)
            self._txt_search.configure(width=40)
            self._txt_search.grid(row=0, column=3, padx=3)
            self._btn_search.grid(row=0, column=4)
        else:
            if self._advanced_search_enabled:
                self._grid_std_search()
                self._grid_adv_search_fields()
            else:
                self._grid_std_search()
