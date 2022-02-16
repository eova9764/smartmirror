from time import strftime
import tkinter as tk

from consts import *

class ClockWidget(tk.Label):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings = {'hr': 12}

    def update(self):
        timestr = strftime('%I:%M:%S %p')
        self.config(text=timestr)
        self.after(1000, self.update)

    def get_settings_menu(self, root):
        return ClockConfig(root, self.settings)

class ClockConfig(tk.Frame):
    def __init__(self, root, settings, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        
        self.settings = settings

        self.config(bg=BGCOL)

        tk.Label(self, text='Clock settings', bg=BGCOL, font=FONT, fg=FGCOL).pack()
