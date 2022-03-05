import tkinter as tk

from configmenu import ConfigMenu
from consts import *
from setting import Setting

class InWeather(tk.Label):
    
    def __init__(self, *args, cfg=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings = {
                'unit':Setting('Unit', ['Farenheit', 'Celcius'],
                        current_val=cfg['unit'] if cfg else 'Farenheit')
        }
        
        self.bgimg = tk.PhotoImage(file='img/indoor-sm.png')
        self.config(image=self.bgimg)
        self.config(highlightbackground=BGCOL, highlightcolor=BGCOL, highlightthickness=BRDRWID)

        self.temp = tk.Label(self)
        self.temp.config(bg=BGCOL, fg=FGCOL, font=FONT_SM)
        self.temp.place(relx=.35, rely=.3)

        self.humid = tk.Label(self)
        self.humid.config(bg=BGCOL, fg=FGCOL, font=FONT_SM)
        self.humid.place(relx=.35, rely=.5)

        self.press = tk.Label(self)
        self.press.config(bg=BGCOL, fg=FGCOL, font=FONT_SM)
        self.press.place(relx=.20, rely=.7)

        self.update()

    def update(self):
        # TODO: update with actual temp from Joey's IO module
        self.temp.config(text='69 F' if self.settings['unit'].get_value() == 'Farenheit' else '20.5 C')
        self.humid.config(text='69 %')
        self.press.config(text='1013.23 hPa')

        self.after(1000, self.update)

    def get_settings_menu(self, root, exiting=False):
        return ConfigMenu(root, self, exiting, title='Weather settings')

    def get_settings(self):
        return self.settings

    def set_settings(self, new_settings):
        self.settings = new_settings
