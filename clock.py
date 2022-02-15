from time import strftime
import tkinter as tk

class ClockWidget(tk.Label):
    
    def update(self):
        timestr = strftime('%-I:%M:%S %p')
        self.config(text=timestr)
        self.after(1000, self.update)

class ClockConfig(tk.Frame):
    def __init__(self, widget, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tk.Label(self, 'test').pack()
