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

        super().__init__(root, *args, **kwargs, rows=3, columns=len(self.settings))

        
        # Allow only horizontal nav (vertical arrows change setting value)
        self.set_nav_axes('h')

        # Add menu title
        self.title = tk.Label(self, text=self.titlestr, bg=BGCOL, fg=FGCOL, font=FONT)
        self.add_widget(self.title, 0, 0)

        # Add spinlist widgets and labels for each setting
        idx = 0
        for item in self.settings:
            entry = self.settings[item]

            # Setting name
            setting_name = tk.Label(self, text=entry.name, bg=BGCOL, fg=FGCOL, font=FONT)
            self.add_widget(setting_name, idx, 1)
            
            # Spinlist
            new_widget = Spinlist(self)
            new_widget.add_items(entry.values)
            new_widget.set_circular(entry.circular)
            new_widget.set_item(self.settings[item].get_value())
            self.settings_widgets[item] = new_widget
            self.add_widget(new_widget, idx, 2)
            idx += 1

        # 1st row has title only, select third row
        self.active_widget_loc['row'] = 1
        self.select_at(0, 2)

        # Add keybinds not taken care of by Keyframe superclass
        self.add_bind('<Up>', self.setting_change)
        self.add_bind('<Down>', self.setting_change)
        self.add_bind('<Return>', self.exit)


    # Exit the menu
    def exit(self, event):
        # Update settings
        for item in self.settings_widgets:
            self.settings[item].set_value(self.settings_widgets[item].get_value())
        self.root.set_main_contents()
        self.widget.set_settings(self.settings)

    # Event callback for changing an entry
    def setting_change(self, event):
        if event.keysym == 'Up':
            self.active_widget.prev_item()
        elif event.keysym == 'Down':
            self.active_widget.next_item()
