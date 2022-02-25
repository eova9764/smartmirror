import clock
from consts import *
import greeting
from keyframe import Keyframe

import configparser
import os
import tkinter as tk

COLS = 1
ROWS = 3

class MirrorUI(tk.Tk):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set fullscreen, hide mouse cursor
        self.attributes('-fullscreen', True)
        self.configure(bg=BGCOL, cursor='none')

        self.content = None
        self.menu = None


    # Bind all of the keys that the keyframe passed in needs
    def bind_keyframe_inputs(self, keyframe):
        kfbinds = keyframe.get_binds()
        for kfbind in kfbinds:
            self.bind(kfbind, kfbinds[kfbind])

    # Unbind all keys except blackout, which can be used anywhere
    def unbind_main_inputs(self):
        self.unbind('<Up>')
        self.unbind('<Left>')
        self.unbind('<Down>')
        self.unbind('<Right>')
        self.unbind('<Return>')

    # Replaces the current screen with the menu of the currently selected widget
    # Event argument is not used but is automatically passed in by tkinter
    def open_menu(self, event=None):

        # Unbind and hide main screen
        self.unbind_main_inputs()
        self.content.pack_forget()
        
        # Pack and bind the new menu
        self.menu = self.content.active_widget.get_settings_menu(self)
        self.menu.pack(expand=True, fill='both')
        self.menu.focus_set()
        self.bind_keyframe_inputs(self.menu)
        

    # Set the main menu and display.
    # If contents is empty, return to stored main menu (as in after returning from a settings menu)
    def set_main_contents(self, contents=None):
        # Remove current menu if needed
        if self.menu != None:
            self.menu.pack_forget()
            self.menu.destroy()
            del(self.menu)
            self.menu = None

        if contents != None:
            # Add contents to the window
            self.content = contents
            self.content.pack(expand=True, fill='both')
            self.bind_keyframe_inputs(self.content)
        else:
            # Restore last contents
            self.content.pack(expand=True, fill='both')
            self.bind_keyframe_inputs(self.content)


if __name__ == '__main__':
    mui = MirrorUI()

    content = Keyframe(mui, rows=ROWS, columns=COLS)

    cfg = None
    if os.path.exists(CFG_LOC):
        cfg = configparser.ConfigParser()
        cfg.read(CFG_LOC)

    # Clock widget and greeting
    if cfg and 'Clock Settings' in cfg:
        clockwidget = clock.ClockWidget(content, cfg=cfg['Clock Settings'])
        greetingwidget = greeting.GreetingWidget(content, cfg=cfg['Clock Settings'])
    else:
        clockwidget = clock.ClockWidget(content)
        greetingwidget = greeting.GreetingWidget(content)

    content.add_widget(clockwidget, 0, 0)
    content.add_widget(greetingwidget, 0, 1)

    # Setup keyboard input
    content.set_nav_axes('vh')
    content.add_bind('<Return>', mui.open_menu)

    mui.set_main_contents(content)

    mui.mainloop()
