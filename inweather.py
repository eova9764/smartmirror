from IO import BME280
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

        self.tempsens = BME280.BME_Init()

        self.update()

    def update(self):
        if self.tempsens:
            raw_temp_val = self.tempsens.get_temperature()
            humidity = self.tempsens.get_humidity()
            pressure = self.tempsens.get_pressure()
            unit = 'C'
            
            if self.settings['unit'].get_value() == 'Farenheit':
                temp_val = raw_temp_val * (9/5) + 32
                unit = 'F'

            self.temp.config(text=f'{temp_val:5.1f} {unit}')
            self.humid.config(text=f'{humidity:5.1f} %rh')
            self.press.config(text=f'{pressure:5.1f} hPa')
            with open('inweather.csv', 'w') as wf:
                wf.write(f'{raw_temp_val:5.1f},{humidity:5.1f},{pressure:5.1f}')
        else:
            self.temp.config(text=f'Could not')
            self.humid.config(text=f'connect to')
            self.press.config(text=f'sensor')

        self.after(1000, self.update)

    def get_settings_menu(self, root, exiting=False):
        return ConfigMenu(root, self, exiting, title='Weather settings')

    def get_settings(self):
        return self.settings

    def set_settings(self, new_settings):
        self.settings = new_settings
