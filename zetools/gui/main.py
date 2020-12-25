import tkinter as tk

import zetools
from zetools.gui import App
from PIL import ImageTk, Image


def run():
    window = tk.Tk()
    window.configure(background=zetools.gui.configs.background_colour)
    window.title("Zetools")
    window.geometry("800x500")
    window.iconbitmap("zetools/gui/brain_icon.ico")

    app = App(window)

    window.mainloop()
