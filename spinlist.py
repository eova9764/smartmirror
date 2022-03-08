import tkinter as tk

from consts import *

class Spinlist(tk.Label):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.items = []
        self.circular = False

        self.current_item = 0

        self.config(bg=BGCOL, fg=FGCOL, font=FONT)

    # Set which item is active (value must already exist in items)
    def set_item(self, value):
        self.current_item = self.items.index(value)
        self.update_text()

    # Set whether or not this is a circular list
    def set_circular(self, boolean):
        prev_val = self.circular
        self.circular = boolean
        if prev_val != self.circular:
            self.update_text()

    # Add several items (pass in a list)
    def add_items(self, items):
        self.items += items

        # Set current item to first entry if the list was previously empty
        if len(self.items) == len(items):
            self.update_text()
 
    # Add a single item
    def add_item(self, item):
        self.items += [item]

        # Set current item to this item if it is the first addition
        if len(self.items) == 1:
            self.config(text=items[0])
        
    # Removes an item
    def remove_item(self, item):
        self.items.remove(item)

    # Call after selecting an item. Updates text and adds arrows where necessary
    def update_text(self):
        # Arrows needed on both ends
        if self.circular:
            self.config(text=f'← {self.items[self.current_item]} →')
        else:
            # Only down arrow needed
            if self.current_item == 0:
                self.config(text=f'← {self.items[self.current_item]}')
            # Only up arrow needed
            elif self.current_item == self.item_count()-1:
                self.config(text=f'{self.items[self.current_item]} →')
            

    # Selects the next item
    def next_item(self):
        if self.current_item == len(self.items)-1: 
            # If this is a circular, loop around once the end is reached, otherwise do nothing
            if self.circular:
                self.current_item = 0
        else:
            self.current_item += 1
        self.update_text()

    # Selects the previous item
    def prev_item(self):
        if self.current_item == 0:
            # If this is a circular, loop around once the start is reached, otherwise do nothing
            if self.circular:
                self.current_item = len(self.items)-1
        else:
            self.current_item -=1
        self.update_text()

    # Returns the number of items this Spinlist has
    def item_count(self):
        return len(self.items)

    # Returns the current item
    def get_value(self):
        return self.items[self.current_item]
