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
        
        self.label = tk.Label(self, text='Today\'s calendar')
        self.label.config(bg=BGCOL, fg=FGCOL, font=FONT_M)
        self.label.pack()

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
            lines.sort()

        year = int(datetime.datetime.now(tz=zoneinfo.ZoneInfo(self.settings['tz'].get_value())).strftime('%Y'))
        month = int(datetime.datetime.now(tz=zoneinfo.ZoneInfo(self.settings['tz'].get_value())).strftime('%m'))
        day = int(datetime.datetime.now(tz=zoneinfo.ZoneInfo(self.settings['tz'].get_value())).strftime('%d'))
        hour = int(datetime.datetime.now(tz=zoneinfo.ZoneInfo(self.settings['tz'].get_value())).strftime('%H'))
        minute = int(datetime.datetime.now(tz=zoneinfo.ZoneInfo(self.settings['tz'].get_value())).strftime('%M'))


        for line in lines:
            result = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})T(\d{1,2}):(\d{2})-(\d{1,2}):(\d{2}) (.*)', line)
            if int(result.group(1)) == year and int(result.group(2)) == month and int(result.group(3)) == day and int(result.group(4)) >= hour:
                event_str = f'{int(result.group(4)):02.0f}:{int(result.group(5)):02.0f}-{int(result.group(6)):02.0f}:{int(result.group(7)):02.0f} {result.group(8)}'
                if event_str not in self.events:
                    self.events.append(event_str)

        self.event_text.config(text='\n'.join(self.events))
        
        self.after(1000, self.update)

    def get_settings_menu(self, _, exiting=False):
        return None
