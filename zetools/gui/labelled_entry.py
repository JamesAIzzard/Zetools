import tkinter as tk

import zetools


class LabelledEntry:
    """Labelled entry box."""

    def __init__(self, master, label_text: str, entry_char_width: int):
        self.frame = tk.Frame(master=master, bg=zetools.gui.configs.background_colour)
        self.label = tk.Label(master=self.frame, text=label_text,
                              width=21, height=1, anchor="w",
                              bg=zetools.gui.configs.background_colour,
                              fg=zetools.gui.configs.std_text_colour,
                              font=(zetools.gui.configs.std_font, zetools.gui.configs.std_font_size))
        self.entry = tk.Entry(master=self.frame, width=entry_char_width,
                              bg=zetools.gui.configs.entry_background_colour,
                              fg=zetools.gui.configs.emph_text_colour,
                              font=(zetools.gui.configs.std_font, zetools.gui.configs.std_font_size),
                              relief=tk.FLAT)
        self.label.grid(column=0, row=0)
        self.entry.grid(column=1, row=0)

    def get(self) -> str:
        return self.entry.get()

    def delete(self, **kwargs) -> None:
        self.entry.delete(**kwargs)

    def pack(self, **kwargs) -> None:
        self.frame.pack(**kwargs)

    def grid(self, **kwargs) -> None:
        self.frame.grid(**kwargs)
