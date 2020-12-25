import tkinter as tk
from PIL import ImageTk, Image


class ImageWidget(tk.Label):
    def __init__(self, master, image_path: str, width:int, **kwargs):
        _raw_image = Image.open(image_path)
        ratio = width / _raw_image.width
        _raw_image = _raw_image.resize((int(_raw_image.width * ratio), int(_raw_image.height * ratio)))
        self._image = ImageTk.PhotoImage(_raw_image)
        super().__init__(master, image=self._image, **kwargs)
