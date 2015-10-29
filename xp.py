__author__ = 'Wing2048'
from tkinter import *

root = Tk()
root.wm_title("Stat Tracker")


def get_next_level(l):
    """
    Calculate the next level XP cap
    :param l: level
    :return: the xp cap of that level
    """
    if l <= 10:
        return (1.5 ** l) * 300
    else:
        return 57 * l * 100


def read():
    """
    Read and update the stat counters from ./data.db
    """
    with open('data.db', 'r') as file:
        for line in file:
            n, l, x = line.split(',')  # stat name, current stat level, current stat xp
            l = int(l)
            x = float(x)
            for stat in stats:
                if stat.name == n:
                    stat.level = l
                    stat.xp = x
                    stat.check_levels()  # update the stat counter to the new value


def update_file():
    """
    Write stat changes to ./data.db
    """
    with open('data.db', 'w') as file:
        for stat in stats:
            file.write(stat.name + ',' + str(stat.level) + ',' + str(stat.xp) + '\n')


class Stat():
    def __init__(self, r, name, x, y, l, xp):
        """

        :param r: root tk object of the counter
        :param name: name of the stat to be tracked
        :param x: x position in grid
        :param y: y position in grid
        :param l: starting level
        :param xp: starting xp
        """
        self.name = name
        self.frame = Frame(r)  # containing frame
        self.frame.grid(column=x, row=y)
        self.title = Label(self.frame, text=name)  # title label
        self.title.grid(column=0, row=0, columnspan=3, sticky='nsew')
        self.easy_button = Button(self.frame, text='Easy', command=self.add_easy)  # button to add small xp
        self.hard_button = Button(self.frame, text='Hard', command=self.add_hard)  # button to add large xp
        self.easy_button.grid(column=0, row=1, sticky='nw')
        self.hard_button.grid(column=1, row=1, sticky='nw')
        self.level = l
        self.xp = xp
        self.next_lvl = get_next_level(self.level)  # calculate next xp cap
        self.stats = Label(self.frame, text="Lvl %s, %.0f%% to Lvl %s (%.0f / %.0f xp)" % (
            self.level,
            self.xp / self.next_lvl * 100,
            self.level + 1,
            self.xp,
            self.next_lvl
        ))
        self.stats.grid(column=2, row=1)

    def add_easy(self):
        """
        Adds a small amount of xp to the counter
        Use if you have done an easy problem
        """
        self.xp += 100
        self.check_levels()  # check if you've levelled up
        update_file()  # rewrite file

    def add_hard(self):
        """
        Adds a larger amount of xp to the counter
        Use if you have done a hard problem
        """
        self.xp += 200
        self.check_levels()  # check if you've levelled up
        update_file()  # rewrite file

    def check_levels(self):
        """
        Checks whether the stat counter has exceeded its XP cap

        """
        if self.xp >= self.next_lvl:
            self.xp -= self.next_lvl
            self.level += 1
            self.next_lvl = get_next_level(self.level)  # calculate next level cap
        self.update_text()  # update the label text

    def update_text(self):
        """
        Updates the stat counter display label and adjusts the window width

        """
        self.stats.configure(text="Lvl %s, %.0f%% to Lvl %s (%.0f / %.0f xp)" % (
            self.level,
            self.xp / self.next_lvl * 100,
            self.level + 1,
            self.xp,
            self.next_lvl
        ))
        root.update()  # update screen widths
        root.minsize(root.winfo_width(), root.winfo_height())  # resizes the window to fit the content
        root.update()  # reupdate the screen


stats = [  # list of stats
           Stat(root, "Mathematics", 0, 0, 0, 0),
           Stat(root, "Physics", 0, 1, 0, 0),
           Stat(root, "SDD", 0, 2, 0, 0),
           Stat(root, "IPT", 0, 3, 0, 0),
           Stat(root, "Mathematics Ext I", 1, 0, 0, 0),
           Stat(root, "Mathematics Ext II", 1, 1, 0, 0),
           Stat(root, "English", 1, 2, 0, 0),
           ]
read()  # read file
root.update()  # update screen size
root.resizable(0, 0)  # stop the window from resizing
root.mainloop()