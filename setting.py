class Setting():
    def __init__(self, name, values, circular=True, current_val_idx=0, current_val=None):
        self.name = name
        self.values = values
        if current_val:
            self.current_val_idx = self.values.index(current_val)
        else:
            self.current_val_idx = current_val_idx
        self.circular = circular

    def get_value(self):
        return self.values[self.current_val_idx]

    def set_value(self, value):
        self.current_val_idx = self.values.index(value)

    def get_name(self):
        return self.name

