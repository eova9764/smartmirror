import clock

import tkinter as tk

BGCOL = 'black'
FGCOL = 'white'
BRDRWID = 2
BRDRCOL = 'white'

class MirrorUI(tk.Tk):

    # First argument is the widget to modify, second is a boolean value as follows:
    #   True to turn on the selection border, false to hide it
    def set_border(self, widget, state):
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
        self.configure(bg=BGCOL)

        # Black background so as not to interfere with the functionaly of the mirror
        self.content = tk.Frame(self, bg=BGCOL)
        self.content.pack(expand=True, fill='both')
        self.content.rowconfigure(2)
        self.content.columnconfigure(2)

        # Configure input listeners
        self.bind('<Up>', self.navigate)
        self.bind('<Left>', self.navigate)
        self.bind('<Down>', self.navigate)
        self.bind('<Right>', self.navigate)

    # Returns the widget at the given location within the grid
    def get_widget_from_coords(self, row, column):
        for widget in self.content.children.values():
            info = widget.grid_info()
            if info['row'] == row and info['column'] == column:
                return widget
        return None

    def navigate(self, event):
        old_widget = self.active_widget
        
        if event.keysym == 'Up':
            self.active_widget_loc['row'] -= 1
        elif event.keysym == 'Down':
            self.active_widget_loc['row'] += 1
        if event.keysym == 'Left':
            self.active_widget_loc['col'] -= 1
        elif event.keysym == 'Right':
            self.active_widget_loc['col'] += 1

        self.active_widget = self.get_widget_from_coords(
                self.active_widget_loc['row'],
                self.active_widget_loc['col'])
        
        self.set_border(old_widget, False)
        self.set_border(self.active_widget, True)

        print(f'{self.active_widget_loc["row"]}, {self.active_widget_loc["col"]}, {self.active_widget}')


if __name__ == '__main__':
    mui = MirrorUI()


    # Clock widget
    clockwidget = clock.ClockWidget(mui.content)#, highlightthickness=BRDRWID)
    clockwidget.config(bg=BGCOL, fg=FGCOL, font=('Arial, 40'))#, highlightbackground=BRDRCOL, highlightcolor=BRDRCOL)
    clockwidget.update()
    clockwidget.grid(row=0, column=0)

    # test
    clockwidget2 = clock.ClockWidget(mui.content)#, highlightthickness=BRDRWID)
    clockwidget2.config(bg=BGCOL, fg=FGCOL, font=('Arial, 40'))#, highlightbackground=BRDRCOL, highlightcolor=BRDRCOL)
    clockwidget2.update()
    clockwidget2.grid(row=1, column=0)

    mui.mainloop()
