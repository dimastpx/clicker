import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from json import dump, load
from tkinter.messagebox import askyesno, showerror


class App:
    def __init__(self):
        self.count = 0
        self.skins = ["Краснохвост"]
        self.oneclick_bonus = 1
        self.second_bonus = 0

        self.all_skins = {"Краснохвост": {"target": "Даётся сразу",
                                          "path": "skins/red1.jpg"},
                          "Краснохвост c ножиком": {"target": "1000 коинов",
                                                    "price": 1000,
                                                    "path": "skins/red2.jpg"}}
        self.skin = "Краснохвост"

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

        self.image = ImageTk.PhotoImage(Image.open("skins/red1.jpg"))
        self.clicker = tk.Button(self.window, image=self.image, command=self.click)
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
                self.skins = ["Краснохвост"]
                self.counter.config(text=self.count)

    def second(self):
        self.count += self.second_bonus

    def skins_open(self):
        self.window_skins = tk.Tk()
        for skin in self.all_skins:
            frame = ttk.Frame(self.window_skins)
            ttk.Label(frame, text=skin).grid(row=0, column=0)
            ttk.Label(frame, text="|").grid(row=0, column=1)
            ttk.Label(frame, text=self.all_skins[skin]["target"]).grid(row=0, column=2)
            ttk.Label(frame, text="|").grid(row=0, column=3)
            if skin in self.skins:
                ttk.Button(frame, text="Выбрать", command=lambda x=skin: self.set_skin(x)).grid(row=0, column=4)
            else:
                if "price" in self.all_skins[skin]:
                    ttk.Button(frame, text="Купить", command=lambda x=skin: self.get_skin(x)).grid(row=0, column=4)
            frame.pack()

        self.window_skins.mainloop()
    def get_skin(self, name):
        match name:
            case "Краснохвост c ножиком":
                if self.count >= 1000:
                    self.count -= 1000
                    self.skins.append("Краснохвост c ножиком")
                    self.counter.config(text=self.count)
                else:
                    showerror("Не хватает", "Недостаточно коинов")
    def set_skin(self, name):
        self.image = ImageTk.PhotoImage(Image.open(self.all_skins[name]["path"]))
        self.clicker.config(image=self.image)

        # Не работают картинки


App()
