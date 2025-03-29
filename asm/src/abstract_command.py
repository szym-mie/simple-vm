class AbstractCommandPrototype:
    def __init__(self, name, doc, params):
        self.name = name
        self.doc = doc
        self.params = params


class AbstractCommand:
    def __init__(self, name, val_list, prototype):
        self.name = name
        self.val_list = val_list
        self.prototype = prototype

    def verify(self):
        is_params_valid = len(self.prototype.params) == len(self.val_list)
        is_name_valid = self.prototype.name == self.name
        return is_params_valid and is_name_valid

