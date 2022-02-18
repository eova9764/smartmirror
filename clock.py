from time import strftime
import tkinter as tk

from consts import *
from keyframe import Keyframe
from spinlist import Spinlist

class ClockWidget(tk.Label):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config(bg=BGCOL, fg=FGCOL, font=FONT)
        self.config(highlightbackground=BGCOL, highlightcolor=BGCOL, highlightthickness=BRDRWID)

        self.settings = {'hr': 12}

        self.update()

    def update(self):
        timestr = ''
        timestr += '%I' if self.settings['hr'] == 12 else '%H'
        timestr += ':%M:%S' if self.settings['hr'] == 24 else ':%M:%S %p'
        #strftime('%I:%M:%S %p')
        time = strftime(timestr)
        self.config(text=time)
        self.after(1000, self.update)

    def get_settings_menu(self, root):
        return ClockConfig(root, self.settings)

class ClockConfig(Keyframe):
    settings_count = 1
    
    def __init__(self, root, settings, *args, **kwargs):
        # 1 row for title and one for settings, 1 column per setting
        super().__init__(root, *args, **kwargs, rows=2, columns=ClockConfig.settings_count)
        
        self.root = root
        self.settings = settings

        self.config(bg=BGCOL)
        self.set_nav_axes('h')

        self.title = tk.Label(self, text='Clock settings', bg=BGCOL, font=FONT, fg=FGCOL)
        self.add_widget(self.title, 0, 0)

        self.hr_format = Spinlist(self, name='hr')
        self.hr_format.add_items(['12 hour', '24 hour'])
        self.hr_format.set_circular(True)
        self.add_widget(self.hr_format, 0, 1)

        # 1st row has title only, select second row
        self.active_widget_loc['row'] = 1
        self.select_at(0, 1)

        self.add_bind('<Up>', self.setting_change)
        self.add_bind('<Down>', self.setting_change)
        self.add_bind('<Return>', self.exit)

    # Exit the menu
    def exit(self, event):
        self.root.set_main_contents()
        
        # Update settings
        if self.hr_format.get_value() == '12 hour':
            self.settings['hr'] = 12
        elif self.hr_format.get_value() == '24 hour':
            print('set 24')

        print(self.settings)
        
    # Event callback for changing an entry
    def setting_change(self, event):
        if event.keysym == 'Up':
            self.active_widget.prev_item()
        elif event.keysym == 'Down':
            self.active_widget.next_item()
