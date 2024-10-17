class AbstractCommandPrototype:
    def __init__(self, name, doc_text, param_list):
        self.name = name
        self.doc_text = doc_text
        self.param_list = param_list

    def get_short_doc(self):
        return '{} {}'.format(
            self.name,
            ' '.join([param.get_short_doc() for param in self.param_list])
        )

    def get_full_doc(self):
        return '{} {}\n\n{}\n{}'.format(
            self.name,
            ' '.join([param.get_short_doc() for param in self.param_list]),
            self.doc_text,
            '\n'.join([param.get_full_doc() for param in self.param_list])
        )

class AbstractCommand:
    def __init__(self, name, val_list, prototype):
        self.name = name
        self.val_list = val_list
        self.prototype = prototype

    def verify(self):
        is_params_valid = len(self.prototype.param_list) == len(self.val_list)
        is_name_valid = self.prototype.name == self.name
        return is_params_valid and is_name_valid

