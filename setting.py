class Setting():
    def __init__(self, name, values, circular=True, current_val_idx=0):
        self.name = name
        self.values = values
        self.current_val_idx = current_val_idx
        self.circular = circular

    def get_value(self):
        return self.values[self.current_val_idx]

    def set_value(self, value):
        self.current_val_idx = self.values.index(value)

