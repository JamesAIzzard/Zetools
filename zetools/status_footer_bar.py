import tkinter as tk

from zetools import configs, repository


class StatusFooterBar(tk.Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, relief=tk.FLAT,
                         bg=configs.background_colour,
                         fg=configs.faded_text_colour,
                         border=0,
                         anchor=tk.W)

    def set(self, value: str):
        """Sets the text in the status bar."""
        self.configure(text=value)

    def _update(self):
        self.set("{num_notes} notes, using {size_on_disk}MB".format(
            num_notes=repository.count_notes(),
            size_on_disk=repository.get_vault_size()
        ))
        self.after(10000, self._update)

    def start(self) -> None:
        """Starts the footer updating."""
        self._update()
