import tkinter as tk

import pyperclip

import zetools
from zetools import configs, zettelkasten


class ExtLabel(tk.Label):
    def __init__(self, master, text: str, **kwargs):
        self.name = text
        kwargs['bg'] = configs.background_colour
        kwargs['font'] = (configs.std_font, configs.std_font_size)
        kwargs['fg'] = configs.emph_text_colour
        kwargs['cursor'] = "hand2"
        super().__init__(master=master, text=text, **kwargs)
        self.bind("<Button-1>", lambda _: self.event_generate("<<zt-ext-clicked>>"))


class View(tk.Frame):
    """Brain ID generator widget."""

    def __init__(self, master, **kwargs):
        super().__init__(master=master, bg=configs.background_colour, **kwargs)
        self._showing_file_exts = False
        # Create child widgets;
        self._icon = zetools.ImageLabel(master=self, image_path='{path}/{name}'.format(
            path=configs.assets_filepath,
            name="logo.png"
        ), img_width=200, bg=zetools.configs.background_colour)
        self._ID_label = tk.Label(master=self, bg=configs.background_colour,
                                  font=(configs.std_font, int(configs.std_font_size)),
                                  fg=configs.emph_text_colour,
                                  cursor="hand2")
        self._ID_label.bind("<Button-1>", lambda _: self._on_zt_click())
        self._ext_toolbar = tk.Frame(master=self, bg=configs.background_colour)
        self._png_label = ExtLabel(master=self._ext_toolbar, text=".png")
        self._jpg_label = ExtLabel(master=self._ext_toolbar, text=".jpg")
        self._md_label = ExtLabel(master=self._ext_toolbar, text=".md")
        self._pdf_label = ExtLabel(master=self._ext_toolbar, text=".pdf")
        self._btn_ext_cancel = zetools.ImageLabel(master=self._ext_toolbar, image_path='{path}/{name}'.format(
            path=configs.assets_filepath,
            name="close.png"
        ), img_width=15, bg=zetools.configs.background_colour, cursor="hand2")
        self._png_label.grid(row=0, column=0)
        self._jpg_label.grid(row=0, column=1)
        self._md_label.grid(row=0, column=2)
        self._pdf_label.grid(row=0, column=3)
        self._btn_ext_cancel.grid(row=0, column=4, padx=10)
        self._btn_ext_cancel.bind("<Button-1>", lambda _: self.toggle_ext_toolbar())
        self._build()

    def toggle_ext_toolbar(self):
        self._showing_file_exts = not self._showing_file_exts
        self._clear_views()
        self._build()

    def _clear_views(self):
        """Clears all child widgets."""
        for result in self.winfo_children():
            result.pack_forget()

    def _build(self):
        self._icon.pack()
        if self._showing_file_exts:
            self._ext_toolbar.pack()
        else:
            self._ID_label.pack()

    def _update_id(self) -> None:
        self._ID_label.configure(text=zettelkasten.generate())
        self.after(1000, self._update_id)

    def _on_zt_click(self) -> None:
        self.toggle_ext_toolbar()
        self.event_generate("<<zt-clicked>>")

    def start(self) -> None:
        """Starts the label update thread."""
        self._update_id()


class Controller:
    """Controller for brain widget."""

    def __init__(self, view: 'View'):
        self._view = view
        self._view.bind("<<zt-clicked>>", self._on_zt_clicked)
        self._view.bind_all("<<zt-ext-clicked>>", self._on_zt_ext_clicked)

    @staticmethod
    def _on_zt_clicked(_) -> None:
        pyperclip.copy(zettelkasten.generate())

    def _on_zt_ext_clicked(self, event) -> None:
        pyperclip.copy(pyperclip.paste() + event.widget.name)
        self._view.toggle_ext_toolbar()
