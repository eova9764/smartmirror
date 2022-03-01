import configparser
import tkinter as tk

from consts import *
from keyframe import Keyframe
from spinlist import Spinlist

class ConfigMenu(Keyframe):
    def __init__(self, root, widget, *args, **kwargs):
        # 1 row for title and 2 for settings (1 name, 1 value), 1 column per setting
        self.titlestr = kwargs.pop('title')

        # Instance variables
        self.root = root
        self.widget = widget

        self.settings = widget.get_settings()
        self.settings_widgets = {}

        super().__init__(root, *args, **kwargs, columns=20, rows=len(self.settings)+19)

        
        # Allow only vertical nav (horizontal arrows change setting value)
        self.set_nav_axes('v')

        # Add menu title
        self.title = tk.Label(self, text=self.titlestr, bg=BGCOL, fg=FGCOL, font=FONT)
        self.add_widget(self.title, 0, 0)

        # Add spinlist widgets and labels for each setting
        idx = 0
        for item in self.settings:
            entry = self.settings[item]

            # Setting name
            setting_name = tk.Label(self, text=entry.name, bg=BGCOL, fg=FGCOL, font=FONT)
            self.add_widget(setting_name, 0, idx+1)
            
            # Spinlist
            new_widget = Spinlist(self)
            new_widget.add_items(entry.values)
            new_widget.set_circular(entry.circular)
            new_widget.set_item(self.settings[item].get_value())
            self.settings_widgets[item] = new_widget
            self.add_widget(new_widget, 1, idx+1)
            idx += 1

        # Select the first Spinlist (row 0 has title, col 0 has settings names)
        self.active_widget_loc['col'] = 1
        self.active_widget_loc['row'] = 1
        self.select_at(1, 1)

        # Add keybinds not taken care of by Keyframe superclass
        self.add_bind('<Right>', self.setting_change)
        self.add_bind('<Left>', self.setting_change)
        self.add_bind('<Return>', self.exit)

    # Exit the menu
    def exit(self, event):
        cfg = configparser.ConfigParser()
        cfg[self.titlestr] = {}
        # Update settings
        for item in self.settings_widgets:
            self.settings[item].set_value(self.settings_widgets[item].get_value())
            cfg[self.titlestr][self.settings[item].get_name()] = self.settings_widgets[item].get_value()

        with open(CFG_LOC, 'w') as cfile:
            cfg.write(cfile)

        self.root.set_main_contents()
        self.widget.set_settings(self.settings)

    # Event callback for changing an entry
    def setting_change(self, event):
        if event.keysym == 'Right':
            self.active_widget.prev_item()
        elif event.keysym == 'Left':
            self.active_widget.next_item()
