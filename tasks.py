import os
import tkinter as tk

from consts import *
from keyframe import Keyframe

class Tasks(tk.Label):

    def __init__(self, *args, cfg=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.config(bg=BGCOL, fg=FGCOL, font=FONT)
        self.config(highlightbackground=BGCOL, highlightcolor=BGCOL, highlightthickness=BRDRWID)

        self.label = tk.Label(self, text='TODO')
        self.label.config(bg=BGCOL, fg=FGCOL, font=FONT_M)
        self.label.pack()

        self.tasks_text = tk.Label(self)
        self.tasks_text.config(bg=BGCOL, fg=FGCOL, font=FONT_SM)
        self.tasks_text.pack()

        self.update()

    def update(self):
        if not os.path.exists('tasks.txt'):
            with open('tasks.txt', 'w') as tasks:
                tasks.write('')

        with open('tasks.txt') as taskfile:
            self.tasks = taskfile.readlines()
            self.task_count = len(self.tasks)
            self.tasks_text.config(text=''.join(self.tasks))


        self.after(1000, self.update)

    def get_settings_menu(self, _, exiting=False):
        return None
        #return TasksMenu(self, columns=1, rows=self.task_count+1, tasks=self.tasks)

# TODO: fix
class TasksMenu(Keyframe):
    def __init__(self, root, *args, **kwargs):
        tasks = kwargs.pop('tasks')
        super().__init__(root, *args, **kwargs)

        self.title = tk.Label(text='TEST', bg=BGCOL, fg=FGCOL, font=FONT_SM)
        self.add_widget(self.title, 0, 0, pack=True)

        self.taskwidgets = []
        for i in range(len(tasks)):
            print('adding')
            self.taskwidgets.append(tk.Label(self, text='test string'))
            self.taskwidgets[-1].config(bg=BGCOL, fg=FGCOL, font=FONT_SM)
            self.add_widget(self.taskwidgets[-1], 0, i, pack=True)

