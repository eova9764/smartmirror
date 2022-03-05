import tkinter as tk
from PIL import ImageTk, Image

from configmenu import ConfigMenu
from consts import *
from setting import Setting

class OutWeather(tk.Label):

    def __init__(self, *args, cfg=None, **kwargs):
        super().__init__(*args, **kwargs)

        if cfg: print('cfg')
        self.settings = {
                'unit':Setting('Unit', ['Farenheit', 'Celcius'],
                        current_val=cfg['unit'] if cfg else 'Farenheit')
        }

        icons_img = Image.open('img/weather-sm.png')
        width, height = icons_img.size

        self.icon_locs = {
                'cloudy': (0, 0),
                'rain': (1, 0),
                'partly cloudy': (2, 0),
                'sunny': (0, 1),
                'thunderstorm': (4, 1),
                'snow': (4, 2)
        }

        self.icons = {}
        for item in self.icon_locs:
            img = icons_img.crop([
                width/5 * self.icon_locs[item][0],
                height/4 * self.icon_locs[item][1],
                width/5 * (self.icon_locs[item][0]+1),
                height/4 * (self.icon_locs[item][1]+1)
            ])
            self.icons[item] = ImageTk.PhotoImage(img)
        
        self.icon = tk.Label(self)
        self.icon.config(bg=BGCOL)
        self.icon.pack()

        self.temp = tk.Label(self)
        self.temp.config(bg=BGCOL, fg=FGCOL, font=FONT_SM)
        self.temp.place(relx=.25, rely=.7)

        self.config(bg=BGCOL)
        self.update()

    def update(self):
        # TODO: update with actual values from Stephen's app
        temp = 54
        percip = 'snow'

        # Update text and icon
        self.icon.config(image=self.icons[percip])
        self.temp.config(text=f'{temp} °F' if self.settings['unit'].get_value() == 'Farenheit' else '12.2 °C')

        # Update every 10 minutes
        self.after(1000 * 60 * 10, self.update)

