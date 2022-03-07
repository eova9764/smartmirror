import datetime
import os
import re
import tkinter as tk
import zoneinfo

from consts import *
from setting import Setting

class Calendar(tk.Label):

    def __init__(self, *args, cfg=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.config(bg=BGCOL, fg=FGCOL, font=FONT)
        self.config(highlightbackground=BGCOL, highlightcolor=BGCOL, highlightthickness=BRDRWID)

        tzs = list(zoneinfo.available_timezones())
        self.settings = {'tz':Setting('Time zone', tzs,
                current_val=cfg['time zone'] if cfg else 'US/Michigan')}
        
        self.event_text = tk.Label(self)
        self.event_text.config(bg=BGCOL, fg=FGCOL, font=FONT_SM)
        self.event_text.pack()

        self.events = []
        self.update()

    def update(self):
        if not os.path.exists('calendar.txt'):
            with open('calendar.txt', 'w') as calfile:
                calfile.write('')

        with open('calendar.txt') as calfile:
            lines = calfile.readlines()

        hour = int(datetime.datetime.now(tz=zoneinfo.ZoneInfo(self.settings['tz'].get_value())).strftime('%H'))
        minute = int(datetime.datetime.now(tz=zoneinfo.ZoneInfo(self.settings['tz'].get_value())).strftime('%M'))

        for line in lines:
            result = re.search(r'(\d{1,2}):(\d{2})-(\d{1,2}):(\d{2}) (.*)', line)
            if int(result.group(1)) > hour:
                if result.string not in self.events:
                    self.events.append(result.string)

        self.event_text.config(text='\n'.join(self.events))
        
        self.after(1000, self.update)
