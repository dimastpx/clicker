import tkinter as tk
import tkinter as ttk
from PIL import ImageTk, Image

class App:
    def __init__(self):
        window = tk.Tk()
        image = ImageTk.PhotoImage(Image.open("IMG_20230602_080430_876.png"))
        img = tk.Button(window, image=image)
        img.grid()

        window.mainloop()

App()