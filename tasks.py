import os
import tkinter as tk

from consts import *

class Tasks(tk.Label):

    def __init__(self, *args, cfg=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.config(bg=BGCOL, fg=FGCOL, font=FONT)
        self.config(highlightbackground=BGCOL, highlightcolor=BGCOL, highlightthickness=BRDRWID)

        self.tasks_text = tk.Label(self)
        self.tasks_text.config(bg=BGCOL, fg=FGCOL, font=FONT_SM)
        self.tasks_text.pack()

        self.update()

    def update(self):
        if not os.path.exists('tasks.txt'):
            with open('tasks.txt', 'w') as tasks:
                tasks.write('')

        with open('tasks.txt') as taskfile:
            self.tasks_text.config(text=taskfile.read())


        self.after(1000, self.update)

    def get_settings_menu(self, _, exiting=False):
        return None
