import battery
import calendar
import clock
from consts import *
import greeting
import inweather
from keyframe import Keyframe
import lights
import outweather
import tasks
from IO import MotSense
from IO import NeoPixels as led

import configparser
import os
import signal
import sys
import threading
import tkinter as tk

import traceback

COLS = 4
ROWS = 4

def close_cleanup():

    # Open each menu with the exiting flag set to true to force them to write
    # out their current config
    print('Starting safe exit procedure...')
    mui.open_menu(clockwidget.get_settings_menu(mui, exiting=True))
    mui.open_menu(inweatherwidget.get_settings_menu(mui, exiting=True))
    global strip
    led.colorWipe(strip, [0, 0, 0], 10)
    print('Done')
    exit()

class MirrorUI(tk.Tk):

    # Only call from toggle_ui_hide: hides the ui
    def _hide_ui(self):
        self.blank = tk.Frame(self)
        self.blank.config(bg=BGCOL)
        self.blank.place(x=0, y=0, width=self.winfo_screenwidth(), height=self.winfo_screenheight())
        self.blank.tkraise()
        global strip
        ledthread = threading.Thread(target=led.colorWipe, args=[strip, [0,0,0], 10])
        ledthread.start()
        self.ui_visible = False

    # Only call from toggle_ui_hide: show previously hidden ui
    def _show_ui(self):
        traceback.print_stack()
        self.last_motion = 0
        self.blank.destroy()
        self.update()
        global lightswidget
        ledthread = threading.Thread(target=lightswidget.update)
        ledthread.start()
        self.ui_visible = True
        
    # Called when sleep button is pressed to hide/show the ui
    def toggle_ui_hide(self, force_state=None, _=None):
        if force_state == None:
            if self.ui_visible:
                self._hide_ui()
                self.last_motion = -self.motion_timeout
            else:
                self._show_ui()
        elif force_state == 'show' and not self.ui_visible:
            self._show_ui()
        elif force_state == 'hide' and self.ui_visible:
            self._hide_ui()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set fullscreen, hide mouse cursor, set exit method
        self.attributes('-fullscreen', True)
        self.configure(bg=BGCOL, cursor='none')
        self.wait_visibility(self)
        self.protocol("WM_DELETE_WINDOW", close_cleanup)

        self.content = None
        self.menu = None

        self.ui_visible = True
        self.bind('<n>', lambda _:self.toggle_ui_hide(None))

        self.motion_timeout = 10000 # 10 seconds
        self.last_motion = 0
        self.check_motion()

    # Polls the motion sensor to see if we need to sleep/wake
    def check_motion(self):
        timer_period = 100 # every 250 ms
        
        # Get motion state
        if MotSense.get() and self.last_motion >= 0:
            self.last_motion = 0
            self.toggle_ui_hide(force_state='show')
        else:
            self.last_motion += timer_period
        if self.last_motion % 1000 == 0:
            print(f'Auto sleep in {self.motion_timeout / 1000 - self.last_motion / 1000} seconds, current timer value: {self.last_motion}')
        
        # Hide/show window based on current and previous states
        if self.last_motion >= self.motion_timeout:
            self.toggle_ui_hide(force_state='hide')
        #elif self.last_motion >= 0:
        #    self.toggle_ui_hide(force_state='show')

        self.after(timer_period, self.check_motion)

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

        if self.content.active_widget != None:
            self.menu = self.content.active_widget.get_settings_menu(self)

            if self.menu != None:
                # Unbind and hide main screen
                self.unbind_main_inputs()
                self.content.pack_forget()
                
                # Pack and bind the new menu
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

def sigint_handler(signal, frame):
    print('KeyboardInterrupt... exiting')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    strip = led.setup()

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
        calendarwidget = calendar.Calendar(content, cfg=cfg['Clock Settings'])
    else:
        clockwidget = clock.ClockWidget(content)
        greetingwidget = greeting.GreetingWidget(content)
        calendarwidget = calendar.Calendar(content)

    # Weather widgets
    if cfg and 'Weather settings' in cfg:
        inweatherwidget = inweather.InWeather(content, cfg=cfg['Weather settings'])
        outweatherwidget = outweather.OutWeather(content, cfg=cfg['Weather settings'])
    else:
        inweatherwidget = inweather.InWeather(content)
        outweatherwidget = outweather.OutWeather(content)

    # Battery widget
    if cfg and 'Battery setttings' in cfg:
        battwidget = battery.BatteryWidget(content, cfg=cfg['Battery setttings'])
    else:
        battwidget = battery.BatteryWidget(content)

    # Lights widget
    global lightswidget
    lightswidget = lights.LightsWidget(content)
    lightswidget.set_strip(strip)

    taskwidget = tasks.Tasks(content)


    # Clear config file so that write operation on exit will not cause
    # duplicate sections to be present
    with open(CFG_LOC, 'w') as cfgfile:
        cfgfile.write('')

    content.add_widget(clockwidget, 0, 0)
    content.add_widget(greetingwidget, 1, 3)
    content.add_widget(inweatherwidget, 1, 0)
    content.add_widget(battwidget, 3, 0)
    content.add_widget(outweatherwidget, 2, 0)
    content.add_widget(taskwidget, 0, 1)
    content.add_widget(calendarwidget, 0, 2)
    content.add_widget(lightswidget, 0, 3)


    # Setup keyboard input
    content.set_nav_axes('vh')
    content.add_bind('<Return>', mui.open_menu)

    mui.set_main_contents(content)

    mui.mainloop()
