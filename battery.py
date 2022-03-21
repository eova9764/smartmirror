import tkinter as tk
from PIL import ImageTk, Image

from configmenu import ConfigMenu
from consts import *
from setting import Setting

class BatteryWidget(tk.Label):

    def __init__(self, *args, cfg=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings = {'sim_batt':Setting('Simulated discharge', ['On', 'Off'], current_val='Off')}
        self.batt_perc = 100
        
        self.config(highlightbackground=BGCOL, highlightcolor=BGCOL, highlightthickness=BRDRWID)

        batt_img = Image.open('img/battery-xsm.png').convert('RGBA')
        width, height = batt_img.size

        ## Charge level images
        # Full
        batt_full = batt_img.crop([0, 0, width/6, height])
        self.batt_full_tk = ImageTk.PhotoImage(batt_full)
        # 80%
        batt_80 = batt_img.crop([width/6, 0, width/6*2, height])
        self.batt_80_tk = ImageTk.PhotoImage(batt_80)
        # 60%
        batt_60 = batt_img.crop([width/6*2, 0, width/6*3, height])
        self.batt_60_tk = ImageTk.PhotoImage(batt_60)
        # 40%
        batt_40 = batt_img.crop([width/6*3, 0, width/6*4, height])
        self.batt_40_tk = ImageTk.PhotoImage(batt_40)
        # 20%
        batt_20 = batt_img.crop([width/6*4, 0, width/6*5, height])
        self.batt_20_tk = ImageTk.PhotoImage(batt_20)
        # Charging
        batt_chrg = batt_img.crop([width/6*5, 0, width, height])
        self.batt_chrg_tk = ImageTk.PhotoImage(batt_chrg)

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
        if self.batt_perc > 0 and self.settings['sim_batt'].get_value() == 'On':
            self.batt_perc -= 1
        self.value.config(text=f'{self.batt_perc}%')

        if 100 >= self.batt_perc > 80:
            self.image.config(image=self.batt_full_tk)
        elif 80 >= self.batt_perc > 60:
            self.image.config(image=self.batt_80_tk)
        elif 60 >= self.batt_perc > 40:
            self.image.config(image=self.batt_60_tk)
        elif 40 >= self.batt_perc > 20:
            self.image.config(image=self.batt_40_tk)
        elif 20 >= self.batt_perc >= 0:
            self.image.config(image=self.batt_20_tk)
        elif self.batt_perc == 'charging':
            self.image.config(image=self.batt_chrg_tk)

        if self.batt_perc <= 20:
            self.quit()


        # Update every second
        self.after(1000, self.update)

    def get_settings_menu(self, root, exiting=False):
        return ConfigMenu(root, self, exiting, title='Battery Settings')

    def get_settings(self):
        return self.settings
    
    def set_settings(self, new_settings):
        self.settings = new_settings
