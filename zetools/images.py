import tkinter as tk
from typing import Optional

from PIL import ImageTk, Image


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


class ImageButton(tk.Button):
    def __init__(self, master, image_path: str, img_width: Optional[int] = None, img_height: Optional[int] = None,
                 **kwargs):
        self._image = SizeableImage(image_path=image_path, img_width=img_width, img_height=img_height)
        super().__init__(master, image=self._image, **kwargs)
