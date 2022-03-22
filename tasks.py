import os
import tkinter as tk

from configmenu import ConfigMenu
from consts import *
from keyframe import Keyframe
from setting import Setting

class Tasks(tk.Label):

    def __init__(self, *args, cfg=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.config(bg=BGCOL, fg=FGCOL, font=FONT)
        self.config(highlightbackground=BGCOL, highlightcolor=BGCOL, highlightthickness=BRDRWID)

        self.settings = {}

        self.label = tk.Label(self, text='TODO')
        self.label.config(bg=BGCOL, fg=FGCOL, font=FONT_M)
        self.label.pack()

        self.tasks_text = tk.Label(self)
        self.tasks_text.config(bg=BGCOL, fg=FGCOL, font=FONT_SM)
        self.tasks_text.pack()

        self.update()

    def update(self):
        # Create task file if it is missing
        if not os.path.exists('tasks.txt'):
            with open('tasks.txt', 'w') as tasks:
                tasks.write('')

        # Read all tasks from task file
        with open('tasks.txt', 'r') as taskfile:
            self.tasks = taskfile.readlines()

        # Add any new tasks into settings
        for task in self.tasks:
            if task not in self.settings:
                self.settings[task] = Setting(task, ['Done', 'Todo', 'Remove'], current_val='Todo')

        # Format into string for display
        taskstr = ''
        delflag = False
        deltasks = []
        for task in self.settings:
            if self.settings[task].get_value() == 'Done':
                taskstr += f'✓ {task}\n'
            elif self.settings[task].get_value() == 'Remove':
                delflag = True
                deltasks.append(self.settings[task])
            else:
                taskstr += f'{task}\n'

        # Remove tasks from settings after iteration is complete so size doesn't change during
        for task in deltasks:
            print(f'Deleting task {task.get_name()}')
            del self.settings[task.get_name()]
        
        # Rewrite task file without deleted tasks
        if delflag:
            with open('tasks.txt', 'w') as wf:
                for task in self.settings:
                    wf.write(task)

        self.tasks_text.config(text=taskstr)


        self.after(1000, self.update)

    def get_settings_menu(self, root, exiting=False):
        return ConfigMenu(root, self, exiting, title='Tasks todo')

    def get_settings(self):
        return self.settings

    def set_settings(self, new_settings):
        self.settings = new_settings
