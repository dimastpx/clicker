import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from json import dump, load
from tkinter.messagebox import askyesno

class App:
    def __init__(self):
        self.count = 0
        self.skins = []
        self.oneclick_bonus = 1
        self.second_bonus = 0

        with open("save.json") as file:
            data = load(file)
            try:
                self.count = data["count"]
                self.skins = data["skins"]
                self.oneclick_bonus = data["oneclick"]
                self.second_bonus = data["second"]
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
        self.menu.add_command(label="Картинка", command=self.skins_open)

        self.window.mainloop()

        self.save()


    def click(self):
        self.count += self.oneclick_bonus
        self.counter.config(text=self.count)
    def save(self):
        with open("save.json", "w") as file:
            data = {"count": self.count,
                    "skins": self.skins,
                    "oneclick": self.oneclick_bonus,
                    "second": self.second_bonus}
            dump(data, file)
    def reset(self):
        if askyesno("Сброс сохранения", "Вы хотите полностью стереть ваш прогресс?"):
            with open("save.json", "w") as file:
                dump({}, file)
                self.count = 0
                self.skins = []
                self.counter.config(text=self.count)
    def second(self):
        self.count += self.second_bonus

    def skins_open(self):
        pass

App()