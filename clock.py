import datetime
from time import strftime
import tkinter as tk
import zoneinfo

from configmenu import ConfigMenu
from consts import *
from keyframe import Keyframe
from setting import Setting
from spinlist import Spinlist

class ClockWidget(tk.Label):

    def __init__(self, *args, cfg=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.config(bg=BGCOL, fg=FGCOL, font=FONT)
        self.config(highlightbackground=BGCOL, highlightcolor=BGCOL, highlightthickness=BRDRWID)

        # Get list of available time zones
        tzs = list(zoneinfo.available_timezones())
        tzs.sort()

        self.settings = {
                'hr':Setting('Hour format', ['12 hour', '24 hour'],
                        current_val=cfg['hour format'] if cfg else None ),
                'tz':Setting('Time zone', tzs,
                        current_val=cfg['time zone'] if cfg else 'US/Michigan'),
        }

        # No longer needed after being stored in settings
        del(tzs)

        self.update()

    def update(self):
        timestr = ''
        timestr += '%I' if self.settings['hr'].get_value() == '12 hour' else '%H'
        timestr += ':%M:%S' if self.settings['hr'].get_value() == '24 hour' else ':%M:%S %p'
        time = datetime.datetime.now(tz=zoneinfo.ZoneInfo(self.settings['tz'].get_value())).strftime(timestr)
        self.config(text=time)
        self.after(1000, self.update)

    def get_settings_menu(self, root, exiting=False):
        return ConfigMenu(root, self, exiting, title='Clock Settings')

    def get_settings(self):
        return self.settings

    def set_settings(self, new_settings):
        self.settings = new_settings
