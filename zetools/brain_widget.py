import tkinter as tk

import pyperclip

import zetools
from zetools import configs, zettelkasten


class View(tk.Frame):
    """Brain ID generator widget."""

    def __init__(self, master, **kwargs):
        super().__init__(master=master, bg=configs.background_colour, cursor="hand2", **kwargs)
        # Create child widgets;
        self._brain_icon = zetools.ImageLabel(master=self, image_path='{path}/{name}'.format(
            path=configs.assets_filepath,
            name="brain.png"
        ), img_width=300, bg=zetools.configs.background_colour)
        self._ID_label = tk.Label(master=self, bg=configs.background_colour,
                                  font=(configs.std_font, configs.std_font_size),
                                  fg=configs.emph_text_colour,
                                  cursor="hand2")
        self._brain_icon.bind("<Button-1>", self._on_brain_click)
        self._brain_icon.pack()
        self._ID_label.bind("<Button-1>", self._on_brain_click)
        self._ID_label.pack()

    def _update_id(self) -> None:
        # self._current_ID.set(zettelkasten.generate())
        self._ID_label.configure(text=zettelkasten.generate())
        self.after(1000, self._update_id)

    def _on_brain_click(self, _) -> None:
        self.event_generate("<<brain-widget-clicked>>")

    def start(self) -> None:
        """Starts the label update thread."""
        self._update_id()


class Controller:
    """Controller for brain widget."""

    def __init__(self, view: 'View'):
        self._view = view
        self._view.bind("<<brain-widget-clicked>>", self._on_brain_clicked)

    @staticmethod
    def _on_brain_clicked(_) -> None:
        pyperclip.copy(zettelkasten.generate())
