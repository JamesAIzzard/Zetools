import tkinter as tk
from typing import Optional

from PIL import ImageTk, Image


class ScrollFrame(tk.Frame):
    def __init__(self, master, width: int, height: int, **kwargs):
        super().__init__(master, **kwargs)
        canvas = tk.Canvas(self, width=width, height=height)
        if 'bg' in kwargs:
            canvas.configure(bg=kwargs['bg'])
        canvas.configure(relief=tk.FLAT)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class SizeableImage(ImageTk.PhotoImage):
    def __init__(self, image_path: str, img_width: Optional[int] = None, img_height: Optional[int] = None):
        _raw_image = Image.open(image_path)
        # If only img_width is provided, scale to img_width and preserve aspect ratio;
        if img_width is not None and img_height is None:
            ratio = img_width / _raw_image.width
            _raw_image = _raw_image.resize((int(_raw_image.width * ratio), int(_raw_image.height * ratio)))
        # If only img_height is provided, scale to img_height and preserve aspect ratio;
        elif img_width is None and img_height is not None:
            ratio = img_height / _raw_image.height
            _raw_image = _raw_image.resize((int(_raw_image.width * ratio), int(_raw_image.height * ratio)))
        # If both are provided, ditch aspect ratio and resize;
        elif img_width is not None and img_height is not None:
            _raw_image = _raw_image.resize((int(img_width), int(img_height)))
        super().__init__(_raw_image)


class ImageLabel(tk.Label):
    def __init__(self, master, image_path: str, img_width: Optional[int] = None, img_height: Optional[int] = None,
                 **kwargs):
        self._image = SizeableImage(image_path=image_path, img_width=img_width, img_height=img_height)
        super().__init__(master, image=self._image, **kwargs)
