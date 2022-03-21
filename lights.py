import tkinter as tk
import threading

from configmenu import ConfigMenu
from consts import *
from keyframe import Keyframe
import IO.NeoPixels as led
from setting import Setting

class LightsWidget(tk.Label):

    def __init__(self, *args, cfg=None, **kwargs):
        super().__init__(*args, **kwargs)

        col_rng = list(range(256))
        col_rng.reverse()
        self.settings = {
                'on': Setting('LED power', ['On', 'Rainbow', 'Off'], 'On'),
                'r': Setting('Red', col_rng, current_val=70),
                'g': Setting('Green', col_rng, current_val=240),
                'b': Setting('Blue', col_rng, current_val=120)
        }

        self.config(bg=BGCOL, fg=FGCOL, highlightcolor=BGCOL, highlightthickness=BRDRWID)

        self.label = tk.Label(self, text='LED colors')
        self.label.config(fg=FGCOL, bg=BGCOL, font=FONT_M)
        self.label.pack()

        self.strip = None

        self.update()

    def current_colors(self):
        r = self.settings['r'].get_value()
        g = self.settings['g'].get_value()
        b = self.settings['b'].get_value()
        return [r,g,b]

    def set_strip(self, strip):
        self.strip = strip
        self.update()

    def update(self):
        if self.strip:
            if self.settings['on'].get_value() == 'On':

                ledthread = threading.Thread(target=led.colorWipe, args=[self.strip, self.current_colors(), 10])
            elif self.settings['on'].get_value() == 'Rainbow':
                ledthread = threading.Thread(target=led.rainbowCycle, args=[self.strip, 10, 0])
            else:
                ledthread = threading.Thread(target=led.colorWipe, args=[self.strip, [0, 0, 0], 10])

            ledthread.start()

    def get_settings_menu(self, root, exiting=False):
        return ConfigMenu(root, self, exiting, title='LED settings')

    def get_settings(self):
        return self.settings

    def set_settings(self, new_settings):
        self.settings = new_settings
        self.update()
