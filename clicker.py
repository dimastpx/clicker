import tkinter as tk
import tkinter.ttk as ttk
from json import dump, load
from tkinter.messagebox import askyesno, showerror

from PIL import ImageTk, Image


# Сделать бонус за клик/в секунду
class App:
    def __init__(self):
        self.window_skins = None
        self.count = 0
        self.skins = ["Краснохвост"]
        self.oneclick_bonus = 1
        self.second_bonus = 0
        self.levels_constant = (0, 100, 500, 1000, 2000, 5000, 10000, 20000, 100000)
        self.level = 1

        self.boosts_click_constant = {"Кусь(+1)": 15,
                                      "Цап(+3)": 20,
                                      "Мур(+10)": 50,
                                      "Чмок(+50)": 200,
                                      "Кусь Сонушки(+100)": 1000,
                                      "Мурчание Саяны(+200)": 2000,
                                      "Сила Краснохвоста(+300)": 5000,
                                      "Поцелуйчики Сонушки(+1000)": 10000}
        self.boosts_click = self.boosts_click_constant.copy()

        self.boosts_second_constant = {"Сон Сонушки(+10)": 1000,
                                       "Храп Краснохвоста(+20)": 3000,
                                       "Рычание Саяны(+50)": 7000,
                                       "Гнев Алохвоста(+100)": 12000}
        self.boosts_second = self.boosts_second_constant.copy()

        self.all_skins = {"Краснохвост": {"target": "Даётся сразу",
                                          "path": "skins/red1.jpg"},
                          "Краснохвост c ножиком": {"target": "80 коинов",
                                                    "price": 80,
                                                    "path": "skins/red2.jpg"},
                          "Милый Краснохвост": {"target": "120 коинов",
                                                "price": 120,
                                                "path": "skins/red3.jpg"},
                          "Милая Сонушка": {"target": "Разблокируйте первых трёх Краснохвостов",
                                            "path": "skins/son1.jpg"},
                          "Весёлый Краснохвост": {"target": "1000 коинов",
                                                  "price": 1000,
                                                  "path": "skins/red5.png"},
                          "Смелая Сонушка": {"target": "5000 коинов",
                                             "price": 5000,
                                             "path": "skins/son3.png"},
                          "Вкусная Сонушка": {"target": "Купите поцелуйчики Сонушки",
                                              "path": "skins/son2.jpg"},
                          "Краснохвост, идущий к... Сонушке": {"target": "Достигните 20000 коинов",
                                                               "path": "skins/red4.jpg"}}
        self.skin = "Краснохвост"

        with open("save.json") as file:
            data = load(file)
            try:
                self.count = data["count"]
                self.skins = data["skins"]
                self.oneclick_bonus = data["oneclick"]
                self.second_bonus = data["second"]
                self.boosts_click = data["all_boost"]
                self.boosts_second = data["sec_boost"]
                self.skin = data["skin"]
                self.level = data["level"]
            except KeyError:
                pass

        # Окно
        self.window = tk.Tk()
        self.window.geometry("500x500+500+200")
        self.window.title("Мяу кликер")
        self.window.iconbitmap("icon.ico")
        # Изображение кнопки
        self.image = ImageTk.PhotoImage(Image.open("skins/red1.jpg"))
        self.clicker = tk.Button(self.window, image=self.image, command=self.click)
        self.clicker.place(relx=0.5, rely=0.5, anchor="center")

        self.set_skin(self.skin)
        # Счётчик
        self.counter = ttk.Label(self.window, text=str(self.count), font="Arial 15")
        self.counter.pack()

        self.counter_frame = ttk.Frame(self.window)
        self.counter_frame.pack()

        self.counter_click = ttk.Label(self.counter_frame, text=str(self.oneclick_bonus), font="Arial 12")
        self.counter_click.grid(row=0, column=0)

        ttk.Label(self.counter_frame, text="     |     ").grid(row=0, column=1)

        self.counter_second = ttk.Label(self.counter_frame, text=str(self.second_bonus), font="Arial 12")
        self.counter_second.grid(row=0, column=2)

        # Верхнее меню (кнопки)
        self.menu = tk.Menu()
        self.window.config(menu=self.menu)
        self.menu.add_command(label="Сброс сохранения", command=self.reset)
        self.menu.add_command(label="Картинка", command=self.skins_open)
        # Верхнее меню (клик)
        self.oneclick_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Бонус за клик", menu=self.oneclick_menu)
        # Верхнее меню (авто клик)
        self.second_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Автоклик", menu=self.second_menu)
        self.init_click_buttons()
        # Прогресс (бар)
        self.progress_bar = ttk.Progressbar(self.window, value=float(self.level), maximum=100)
        self.progress_bar.pack(side="bottom", fill="x")

        self.level_counter = ttk.Label(text= f"Ваш уровень : {self.level}")
        self.level_counter.pack(side="bottom")
        # Авто клик
        self.autoclick()

        self.window.mainloop()
        # Сохранение после закрытия
        self.save()

    def click(self):
        self.count += self.oneclick_bonus
        self.counter_update()
        self.bar_update()



    def save(self):
        with open("save.json", "w") as file:
            data = {"count": self.count,
                    "skins": self.skins,
                    "oneclick": self.oneclick_bonus,
                    "second": self.second_bonus,
                    "all_boost": self.boosts_click,
                    "sec_boost": self.boosts_second,
                    "skin": self.skin,
                    "level": self.level}
            dump(data, file)

    def reset(self):
        if askyesno("Сброс сохранения", "Вы хотите полностью стереть ваш прогресс?"):
            with open("save.json", "w") as file:
                dump({}, file)
                self.count = 0
                self.skins = ["Краснохвост"]
                self.set_skin("Краснохвост")
                self.counter_update()
                self.oneclick_bonus = 1
                self.second_bonus = 0
                self.level = 1
                self.boosts_click = self.boosts_click_constant
                self.boosts_second = self.boosts_second_constant
                self.clear_menu()
                self.init_click_buttons()

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
        self.window_skins.geometry("+1000+200")
        self.window_skins.title("Выбор картинок")
        self.window_skins.iconbitmap("icon.ico")
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
            ttk.Label(self.window_skins, text="-"*100).pack()
            frame.pack()

        self.window_skins.mainloop()

    def get_skin(self, name, price=None):
        if price:
            if self.count >= price:
                self.count -= price
                self.skins.append(name)
                self.counter_update()
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
                case "Вкусная Сонушка":
                    if self.boosts_click["Поцелуйчики Сонушки(+1000)"] > 10000:
                        self.skins.append(name)
                        self.skins_open()
                    else:
                        showerror("Не куплено", "Вы не купили поцелуйчик Сонушки:(")
                case "Краснохвост, идущий к... Сонушке":
                    if self.count >= 20000:
                        self.skins.append(name)
                        self.skins_open()
                    else:
                        showerror("Не хватает", "На данный момент коинов меньше 20000")

    def set_skin(self, name):
        self.skin = name
        self.image = ImageTk.PhotoImage(Image.open(self.all_skins[name]["path"]))
        self.clicker.config(image=self.image)

    def add_oneclick(self, name: str):
        price = self.boosts_click[name]
        if self.count >= price:
            self.count -= price
            boost = int(name[name.find("(") + 1: name.find(")")])
            self.oneclick_bonus += boost
            self.counter_update()
            self.boosts_click[name] *= 2
            self.clear_menu()
            self.init_click_buttons()
        else:
            self.show_error("Недостаточно коинов")

    def add_second(self, name: str):
        price = self.boosts_second[name]
        if self.count >= price:
            self.count -= price
            boost = int(name[name.find("(") + 1: name.find(")")])
            self.second_bonus += boost
            self.counter_update()
            self.boosts_second[name] *= 2
            self.clear_menu()
            self.init_click_buttons()
        else:
            self.show_error("Недостаточно коинов")

    def autoclick(self):
        self.count += self.second_bonus
        self.counter_update()
        self.bar_update()
        self.window.after(1000, self.autoclick)

    def init_click_buttons(self):
        for i in self.boosts_click:
            self.oneclick_menu.add_command(label=f"{i} - {self.boosts_click[i]:,}",
                                           command=lambda x=i: self.add_oneclick(x))
        for j in self.boosts_second:
            self.second_menu.add_command(label=f"{j} - {self.boosts_second[j]:,}",
                                         command=lambda x=j: self.add_second(x))

    def clear_menu(self):
        self.oneclick_menu.delete(0, "end")
        self.second_menu.delete(0, "end")

    def counter_update(self):
        self.counter.config(text=f"Ваши коины: {self.count:,}")
        self.counter_click.config(text=f"Коинов за клик: {self.oneclick_bonus:,}")
        self.counter_second.config(text=f"Коинов в секунду: {self.second_bonus:,}")

    def show_error(self, text: str):
        temp = ttk.Label(self.window, text=text, foreground="red", font="20")
        temp.pack()
        self.window.after(2000, lambda: temp.destroy())

    def bar_update(self):
        mx = self.levels_constant[self.level]
        if self.count >= mx:
            # Новый уровень
            self.level += 1
            mx = self.levels_constant[self.level]

        self.progress_bar["maximum"] = mx

        self.progress_bar["value"] = self.count
        self.progress_bar.update()

        self.level_counter["text"] = f"Ваш уровень : {self.level}"
        self.level_counter.update()




App()
