import clock
from consts import *

import tkinter as tk


COLS = 1
ROWS = 3

class MirrorUI(tk.Tk):

    # First argument is the widget to modify, second is a boolean value as follows:
    #   True to turn on the selection border, false to hide it
    def set_border(self, widget, state):
        if widget:
            if state:
                widget.config(highlightbackground=BRDRCOL, highlightcolor=BRDRCOL, highlightthickness=BRDRWID)
            else:
                widget.config(highlightbackground=BGCOL, highlightcolor=BGCOL, highlightthickness=BRDRWID)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.active_widget_loc = {'row': 0, 'col': 0}
        self.active_widget = None

        # Create window
        self.attributes('-fullscreen', True)
        self.configure(bg=BGCOL, cursor='none')

        # Black background so as not to interfere with the functionaly of the mirror
        self.content = tk.Frame(self, bg=BGCOL)
        self.content.pack(expand=True, fill='both')
        self.content.rowconfigure(ROWS)
        self.content.columnconfigure(COLS)

        self.content.bind('<A>', self.test)
        self.content.focus_set()

        self.bind_main_inputs()

    def test(self):
        print('test')

    def bind_main_inputs(self):
        # Configure input listeners
        self.bind('<Up>', self.navigate)
        self.bind('<Left>', self.navigate)
        self.bind('<Down>', self.navigate)
        self.bind('<Right>', self.navigate)
        self.bind('<Return>', self.open_menu)

    def unbind_main_inputs(self):
        self.unbind('<Up>')
        self.unbind('<Left>')
        self.unbind('<Down>')
        self.unbind('<Right>')
        self.unbind('<Return>')

    def open_menu(self, event):
        self.unbind_main_inputs()
        self.content.pack_forget()
        
        self.active_widget.get_settings_menu(self).pack(expand=True, fill='both')

    # Returns the widget at the given location within the grid
    def get_widget_from_coords(self, row, column):
        for widget in self.content.children.values():
            info = widget.grid_info()
            if info['row'] == row and info['column'] == column:
                return widget
        return None

    def navigate(self, event):
        old_widget = self.active_widget

        moveflag = False
        
        if event.keysym == 'Up' and self.active_widget_loc['row'] > 0:
            self.active_widget_loc['row'] -= 1
            moveflag = True
        elif event.keysym == 'Down' and self.active_widget_loc['row'] < ROWS-1:
            self.active_widget_loc['row'] += 1
            moveflag = True
        elif event.keysym == 'Left' and self.active_widget_loc['col'] > 0:
            self.active_widget_loc['col'] -= 1
            moveflag = True
        elif event.keysym == 'Right' and self.active_widget_loc['col'] < COLS-1:
            self.active_widget_loc['col'] += 1
            moveflag = True

        if moveflag:
            self.active_widget = self.get_widget_from_coords(
                    self.active_widget_loc['row'],
                    self.active_widget_loc['col'])
            
            self.set_border(old_widget, False)
            self.set_border(self.active_widget, True)

        if DEBUG:
            print(f'{self.active_widget_loc["row"]}, {self.active_widget_loc["col"]}, {self.active_widget}')


if __name__ == '__main__':
    mui = MirrorUI()


    # Clock widget
    clockwidget = clock.ClockWidget(mui.content)
    clockwidget.config(bg=BGCOL, fg=FGCOL, font=FONT)
    clockwidget.config(highlightbackground=BGCOL, highlightcolor=BGCOL, highlightthickness=BRDRWID)
    clockwidget.update()
    clockwidget.grid(row=0, column=0)

    # test
    clockwidget2 = clock.ClockWidget(mui.content)
    clockwidget2.config(bg=BGCOL, fg=FGCOL, font=FONT)
    clockwidget2.config(highlightbackground=BGCOL, highlightcolor=BGCOL, highlightthickness=BRDRWID)
    clockwidget2.update()
    clockwidget2.grid(row=1, column=0)

    # test
    clockwidget3 = clock.ClockWidget(mui.content)
    clockwidget3.config(bg=BGCOL, fg=FGCOL, font=FONT)
    clockwidget3.config(highlightbackground=BGCOL, highlightcolor=BGCOL, highlightthickness=BRDRWID)
    clockwidget3.update()
    clockwidget3.grid(row=2, column=0)

    mui.mainloop()
