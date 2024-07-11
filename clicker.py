import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from json import dump, load
from tkinter.messagebox import askyesno

class App:
    def __init__(self):
        self.count = 0
        self.skins = {}

        with open("save.json") as file:
            data = load(file)
            try:
                self.count = data["count"]
            except KeyError:
                pass

        self.window = tk.Tk()
        self.window.geometry("500x500")

        image = ImageTk.PhotoImage(Image.open("red1.jpg"))
        self.clicker = tk.Button(self.window, image=image, command=self.click)
        self.clicker.place(relx=0.5, rely=0.5, anchor="center")

        self.counter = ttk.Label(self.window, text=str(self.count))
        self.counter.pack()

        self.menu = tk.Menu()
        self.window.config(menu=self.menu)
        self.menu.add_command(label="Сброс сохранения", command=self.reset)

        self.window.mainloop()

        self.save()


    def click(self):
        self.count += 1
        self.counter.config(text=self.count)
    def save(self):
        with open("save.json", "w") as file:
            data = {"count": self.count}
            dump(data, file)
    def reset(self):
        if askyesno("Сброс сохранения", "Вы хотите полностью стереть ваш прогресс?"):
            with open("save.json", "w") as file:
                dump({}, file)
                self.count = 0
                self.skins = {}
                self.counter.config(text=self.count)

App()