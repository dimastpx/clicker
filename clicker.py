import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from json import dump, load
from tkinter.messagebox import askyesno, showerror

# Сделать бонус за клик/в секунду
class App:
    def __init__(self):
        self.window_skins = None
        self.count = 0
        self.skins = ["Краснохвост"]
        self.oneclick_bonus = 1
        self.second_bonus = 0
        self.boosts_click = {"кусь": 15,
                             "цап": 20,
                             "мур": 50,
                             "чмок": 200}

        self.all_skins = {"Краснохвост": {"target": "Даётся сразу",
                                          "path": "skins/red1.jpg"},
                          "Краснохвост c ножиком": {"target": "80 коинов",
                                                    "price": 80,
                                                    "path": "skins/red2.jpg"},
                          "Милый Краснохвост": {"target": "120 коинов",
                                                "price": 120,
                                                "path": "skins/red3.jpg"},
                          "Милая Сонушка": {"target": "Необходимо получить первых трёх Краснохвостов",
                                            "path": "skins/son1.jpg"}}
        self.skin = "Краснохвост"

        with open("save.json") as file:
            data = load(file)
            try:
                self.count = data["count"]
                self.skins = data["skins"]
                self.oneclick_bonus = data["oneclick"]
                self.second_bonus = data["second"]
                self.boosts_click = data["all_boost"]
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

        self.oneclick_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Бонус за клик", menu=self.oneclick_menu)
        self.init_oneclick_buttons()

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
                    "second": self.second_bonus,
                    "all_boost": self.boosts_click}
            dump(data, file)

    def reset(self):
        if askyesno("Сброс сохранения", "Вы хотите полностью стереть ваш прогресс?"):
            with open("save.json", "w") as file:
                dump({}, file)
                self.count = 0
                self.skins = ["Краснохвост"]
                self.counter.config(text=self.count)
                self.oneclick_bonus = 1

    def second(self):
        self.count += self.second_bonus

    def skins_open(self):
        try:
            self.window_skins.destroy()
        except AttributeError:
            pass
        except tk.TclError:
            pass
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
                    price = self.all_skins[skin]["price"]
                    ttk.Button(frame, text="Купить",
                               command=lambda x=skin, y=price: self.get_skin(x, y)).grid(row=0, column=4)
                else:
                    ttk.Button(frame, text="Получить",
                               command=lambda x=skin: self.get_skin(x)).grid(row=0, column=4)
            frame.pack()

        self.window_skins.mainloop()

    def get_skin(self, name, price=None):
        if price:
            if self.count >= price:
                self.count -= price
                self.skins.append(name)
                self.counter.config(text=self.count)
                self.skins_open()
            else:
                showerror("Не хватает", "Недостаточно коинов")
        else:
            match name:
                case "Милая Сонушка":
                    if "Краснохвост c ножиком" in self.skins and "Милый Краснохвост" in self.skins:
                        self.skins.append(name)
                        self.skins_open()
                    else:
                        showerror("Не собрано", "Вы не собрали все картинки")

    def set_skin(self, name):
        self.image = ImageTk.PhotoImage(Image.open(self.all_skins[name]["path"]))
        self.clicker.config(image=self.image)

    def add_oneclick(self, name):
        price = self.boosts_click[name]
        boost = None
        if self.count >= price:
            self.count -= price
            match name:
                case "кусь":
                    boost = 1
                case "цап":
                    boost = 3
                case "мур":
                    boost = 10
                case "чмок":
                    boost = 25
            self.oneclick_bonus += boost
            self.counter.config(text=self.count)
            self.boosts_click[name] *= 2
            self.oneclick_menu.delete(0, "end")
            self.init_oneclick_buttons()
        else:
            showerror("Не хватает", "Недостаточно коинов")

    def init_oneclick_buttons(self):
        self.oneclick_menu.add_command(label=f"Кусь(+1) - {self.boosts_click["кусь"]}",
                                       command=lambda: self.add_oneclick("кусь"))
        self.oneclick_menu.add_command(label=f"Цап(+3) - {self.boosts_click["цап"]}",
                                       command=lambda: self.add_oneclick("цап"))
        self.oneclick_menu.add_command(label=f"Муррчащий ускоритель(+10) - {self.boosts_click["мур"]}",
                                       command=lambda: self.add_oneclick("мур"))
        self.oneclick_menu.add_command(label=f"Поцелуй от Сонушки(+25) - {self.boosts_click["чмок"]}",
                                       command=lambda: self.add_oneclick("чмок"))


App()
