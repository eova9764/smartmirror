import datetime
import os
import tkinter as tk
import zoneinfo

from consts import *
from setting import Setting

class GreetingWidget(tk.Label):

    def __init__(self, *args, cfg=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.config(bg=BGCOL, fg=FGCOL, font=FONT)
        self.config(highlightbackground=BGCOL, highlightcolor=BGCOL, highlightthickness=BRDRWID)

        tzs = list(zoneinfo.available_timezones())
        tzs.sort()

        self.settings = {'tz':Setting('Time zone', tzs,
                current_val=cfg['time zone'] if cfg else 'US/Michigan')}

        self.update()

    def update(self):
        if not os.path.exists('username.txt'):
            with open('username.txt', 'w') as wf:
                wf.write('')
                username = None
        else:
            with open('username.txt', 'r') as rf:
                try:
                    username = rf.readlines()[0]
                except IndexError:
                    username = None

        hour = int(datetime.datetime.now(tz=zoneinfo.ZoneInfo(self.settings['tz'].get_value())).strftime('%H'))
        if 5 <= hour < 12:
            time_of_day = 'morning'
        elif 12 <= hour < 17:
            time_of_day = 'afternoon'
        elif 17 <= hour < 21:
            time_of_day = 'evening'
        else:
            time_of_day = 'night'

        if username:
            self.config(text=f'Good {time_of_day}, {username}')
        else:
            self.config(text=f'Good {time_of_day}')

        ## Update every second
        self.after(1000, self.update)

    def get_settings_menu(self, _):
        return None
