import tkinter as tk


class LabelledEntry(tk.Frame):
    """Labelled entry box."""

    def __init__(self, master, label_kwargs, entry_kwargs):
        super().__init__(master=master)
        if 'bg' in label_kwargs:
            self.configure(bg=label_kwargs['bg'])
        elif 'background_colour' in label_kwargs:
            self.configure(bg=label_kwargs['background_colour'])
        self._label = tk.Label(master=self, **label_kwargs)
        self._label.grid(row=0, column=0)
        self._entry = tk.Entry(master=self, **entry_kwargs)
        self._entry.grid(row=0, column=1)

    def get(self) -> str:
        return self._entry.get()

    def clear(self) -> None:
        self._entry.delete(0, tk.END)

    def configure_label(self, **kwargs):
        self._label.configure(**kwargs)

    def configure_entry(self, **kwargs):
        self._entry.configure(**kwargs)
