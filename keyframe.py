from consts import *

import tkinter as tk

class Keyframe(tk.Frame):
    def __init__(self, *args, **kwargs):
        self.rows = kwargs.pop('rows')
        self.columns = kwargs.pop('columns')
        super().__init__(*args, **kwargs)

        self.widget_count = 0
        self.active_widget_loc = {'row': 0, 'col': 0}
        self.active_widget = None
        self.widgets = [[None for i in range(self.rows)] for j in range(self.columns)]
        self.binds = {
            '<Up>': self.navigate,
            '<Left>': self.navigate,
            '<Down>': self.navigate,
            '<Right>': self.navigate,
        }

        for i in range(self.rows):
            self.rowconfigure(i, weight=1)
        for i in range(self.columns):
            self.columnconfigure(i, weight=1)
        # Black background so as not to interfere with the functionaly of the mirror
        self.config(bg=BGCOL)
        self.nav = {'u': 1, 'l': 1, 'd': 1, 'r': 1}

    # Selects what axes for navigation this view supports. Default is all 4 directions.
    # Pass in a string for the argument as follows:
    # Empty string: no navigation supported
    # 'v' or 'y' included in string: navigation supported in up and down directions
    # 'h' or 'x' included in string: navigation supported in left and right directions
    def set_nav_axes(self, axes):
        if axes == None:
            for key in self.nav:
                self.nav[key] = 0
            return
        if 'v' in axes or 'y' in axes:
            self.nav['u'] = 1
            self.nav['d'] = 1
        else:
            self.nav['u'] = 0
            self.nav['d'] = 0

        if 'h' in axes or 'x' in axes:
            self.nav['l'] = 1
            self.nav['r'] = 1
        else:
            self.nav['l'] = 0
            self.nav['r'] = 0

    # Used to move the currently selected widget when the arrow keys are pressed
    def navigate(self, event):
        moveflag = False
        
        if event.keysym == 'Up' and self.active_widget_loc['row'] > 0:
            if self.nav['u']:
                self.active_widget_loc['row'] = self.find_next_suitable_grid(event.keysym)
                moveflag = True
        elif event.keysym == 'Down' and self.active_widget_loc['row'] < self.rows-1:
            if self.nav['d']:
                self.active_widget_loc['row'] = self.find_next_suitable_grid(event.keysym)
                moveflag = True
        elif event.keysym == 'Left' and self.active_widget_loc['col'] > 0:
            if self.nav['l']:
                self.active_widget_loc['col'] = self.find_next_suitable_grid(event.keysym)
                moveflag = True
        elif event.keysym == 'Right' and self.active_widget_loc['col'] < self.columns-1:
            if self.nav['r']:
                self.active_widget_loc['col'] = self.find_next_suitable_grid(event.keysym)
                moveflag = True

        if moveflag:
            self.select_at(self.active_widget_loc['col'], self.active_widget_loc['row'])

        if DEBUG:
            print(f'{self.active_widget_loc["col"]}, {self.active_widget_loc["row"]}, {self.active_widget}')

    # Find the next location that contains a widget in the direction specified,
    # otherwise returns the current location
    # Used to skip over empty spaces when navigation occurs
    def find_next_suitable_grid(self, direction):
        # Move up
        if direction == 'Up':
            for i in range(self.active_widget_loc['row']-1, -1, -1):
                if self.widgets[self.active_widget_loc['col']][i] != None:
                    return i
            return self.active_widget_loc['row']
        # Move down
        elif direction == 'Down':
            for i in range(self.active_widget_loc['row']+1, len(self.widgets)):
                if self.widgets[self.active_widget_loc['col']][i] != None:
                    return i
            return self.active_widget_loc['row']
        # Move left
        elif direction == 'Left':
            for i in range(self.active_widget_loc['col']-1, -1, -1):
                if self.widgets[i][self.active_widget_loc['row']] != None:
                    return i
            return self.active_widget_loc['col']
        # Move right
        elif direction == 'Right':
            for i in range(self.active_widget_loc['col']+1, len(self.widgets)):
                if self.widgets[i][self.active_widget_loc['row']] != None:
                    return i
            return self.active_widget_loc['col']



    # Select the widget at the given coordinates
    def select_at(self, column, row):
        old_widget = self.active_widget

        self.active_widget = self.get_widget_from_coords(column, row)
        
        self.set_border(old_widget, False)
        self.set_border(self.active_widget, True)



    # Returns the widget at the given location within the grid
    def get_widget_from_coords(self, column, row):
        return self.widgets[column][row]


    # First argument is the widget to modify, second is a boolean value as follows:
    #   True to turn on the selection border, false to hide it
    def set_border(self, widget, state):
        if widget:
            if state:
                widget.config(highlightbackground=BRDRCOL, highlightcolor=BRDRCOL, highlightthickness=BRDRWID)
            else:
                widget.config(highlightbackground=BGCOL, highlightcolor=BGCOL, highlightthickness=BRDRWID)

    def add_widget(self, widget, column, row):
        if DEBUG:
            print(f'<add_widget> Adding widget {widget} at {column}, {row}\n{self.widgets}\n\n')
        # Do not overwrite an existing widget
        if self.widgets[column][row] != None:
            print('Widget already exists there')
        else:
            self.widgets[column][row] = widget
            widget.grid(row=row, column=column)
            self.widget_count += 1

        if self.widget_count == 1:
            self.select_at(column, row)

    def add_bind(self, bind, function):
        self.binds[bind] = function

    def remove_bind(self, bind):
        self.binds.pop(bind)

    def get_binds(self):
        return self.binds
