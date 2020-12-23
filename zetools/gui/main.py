import tkinter as tk

from PIL import ImageTk, Image

import zetools

# Configure base window;
window = tk.Tk()
window.configure(background=zetools.gui.configs.background_colour, bd=0, padx=5, pady=5)
window.title("Zetools")
window.geometry("800x500")
window.iconbitmap("zetools/gui/brain_icon.ico")

# Create main page image;
logo = ImageTk.PhotoImage(Image.open("zetools/gui/brain.png"))
logo_label = tk.Label(image=logo, bg=zetools.gui.configs.background_colour)
logo_label.pack()

# Create the search widget;
search_widget = zetools.gui.SearchWidget(window, on_search=zetools.search.run_search)
search_widget.pack()

window.mainloop()
