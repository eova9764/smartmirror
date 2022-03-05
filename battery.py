import tkinter as tk
from PIL import ImageTk, Image

from configmenu import ConfigMenu
from consts import *
from setting import Setting

class BatteryWidget(tk.Label):

    def __init__(self, *args, cfg=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings = {}

        batt_img = Image.open('img/battery-xsm.png').convert('RGBA')
        width, height = batt_img.size

        ## Charge level images
        # Full
        self.batt_full = batt_img.crop([0, 0, width/6, height])
        self.batt_full_tk = ImageTk.PhotoImage(self.batt_full)
        # 80%
        self.batt_80 = batt_img.crop([width/6, 0, width/6*2, height])
        self.batt_80_tk = ImageTk.PhotoImage(self.batt_80)
        # 60%
        self.batt_60 = batt_img.crop([width/6*2, 0, width/6*3, height])
        self.batt_60_tk = ImageTk.PhotoImage(self.batt_60)
        # 40%
        self.batt_40 = batt_img.crop([width/6*3, 0, width/6*4, height])
        self.batt_40_tk = ImageTk.PhotoImage(self.batt_40)
        # 20%
        self.batt_20 = batt_img.crop([width/6*4, 0, width/6*5, height])
        self.batt_20_tk = ImageTk.PhotoImage(self.batt_20)
        # Charging
        self.batt_chrg = batt_img.crop([width/6*5, 0, width, height])
        self.batt_chrg_tk = ImageTk.PhotoImage(self.batt_chrg)

        # Numeral value
        self.value = tk.Label(self)
        self.value.config(bg=BGCOL, fg=FGCOL, font=FONT)
        self.value.pack()

        # Image representation
        self.image = tk.Label(self)
        self.image.config(image=self.batt_chrg_tk, bg=BGCOL)
        self.image.pack()

        self.config(bg=BGCOL)
        self.update()

    def update(self):
        # TODO: update with actual battery reading from Joey's IO module
        batt_perc = 0
        self.value.config(text=f'{batt_perc}%')

        if 100 >= batt_perc > 80:
            self.image.config(image=self.batt_full_tk)
        elif 80 >= batt_perc > 60:
            self.image.config(image=self.batt_80_tk)
        elif 60 >= batt_perc > 40:
            self.image.config(image=self.batt_60_tk)
        elif 40 >= batt_perc > 20:
            self.image.config(image=self.batt_40_tk)
        elif 20 >= batt_perc >= 0:
            self.image.config(image=self.batt_20_tk)
        elif batt_perc == 'charging':
            self.image.config(image=self.batt_chrg_tk)


        # Update every 1 minute
        self.after(1000 * 60, self.update)
