__author__ = 'Wing2048'
from tkinter import *

root = Tk()


def get_next_level(l):
    if l <= 10:
        return (1.5 ** l) * 300
    else:
        return 57 * l * 100


def read():
    with open('data.db', 'r') as file:
        for line in file:
            n, l, x = line.split(',')
            l = int(l)
            x = float(x)
            for stat in stats:
                if stat.name == n:
                    stat.level = l
                    stat.xp = x
                    stat.check_levels()


def update_file():
    with open('data.db', 'w') as file:
        for stat in stats:
            file.write(stat.name + ',' + str(stat.level) + ',' + str(stat.xp) + '\n')


class Stat():
    def __init__(self, r, name, x, y, l, xp):
        self.name = name
        self.frame = Frame(r)
        self.frame.grid(column=x, row=y)
        self.title = Label(self.frame, text=name)
        self.title.grid(column=0, row=0, columnspan=3, sticky='nsew')
        self.easy_button = Button(self.frame, text='Easy', command=self.add_easy)
        self.hard_button = Button(self.frame, text='Hard', command=self.add_hard)
        self.easy_button.grid(column=0, row=1, sticky='nw')
        self.hard_button.grid(column=1, row=1, sticky='nw')
        self.level = l
        self.xp = xp
        self.next_lvl = get_next_level(self.level)
        self.stats = Label(self.frame, text="Lvl %s, %.0f%% to Lvl %s (%.0f / %.0f xp)" % (
            self.level,
            self.xp / self.next_lvl * 100,
            self.level + 1,
            self.xp,
            self.next_lvl
        ))
        self.stats.grid(column=2, row=1)

    def add_easy(self):
        self.xp += 100
        self.check_levels()
        update_file()

    def add_hard(self):
        self.xp += 200
        self.check_levels()
        update_file()

    def check_levels(self):
        if self.xp >= self.next_lvl:
            self.xp -= self.next_lvl
            self.level += 1
            self.next_lvl = get_next_level(self.level)
        self.update_text()

    def update_text(self):
        self.stats.configure(text="Lvl %s, %.0f%% to Lvl %s (%.0f / %.0f xp)" % (
            self.level,
            self.xp / self.next_lvl * 100,
            self.level + 1,
            self.xp,
            self.next_lvl
        ))
        root.update()
        root.minsize(root.winfo_width(), root.winfo_height())
        root.update()


stats = [
    Stat(root, "Mathematics", 0, 0, 0, 0),
    Stat(root, "Physics", 0, 1, 0, 0),
    Stat(root, "SDD", 0, 2, 0, 0),
    Stat(root, "IPT", 0, 3, 0, 0),
]
read()
root.update()
root.resizable(0, 0)
root.mainloop()