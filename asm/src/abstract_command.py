class AbstractCommandPrototype:
    def __init__(self, qname, doc_text, param_list):
        self.qname = qname
        self.doc_text = doc_text
        self.param_list = param_list

    def get_short_doc(self):
        return '{} {}'.format(
            self.qname,
            ' '.join([param.get_short_doc() for param in self.param_list])
        )

    def get_full_doc(self):
        return '{} {}\n\n{}\n{}'.format(
            self.qname,
            ' '.join([param.get_short_doc() for param in self.param_list]),
            self.doc_text,
            '\n'.join([param.get_full_doc() for param in self.param_list])
        )

class AbstractCommand:
    def __init__(self, qname, val_list, prototype):
        self.qname = qname
        self.val_list = val_list
        self.prototype = prototype

    def verify(self):
        is_params_valid = len(self.prototype.param_list) == len(self.val_list)
        is_q_name_valid = self.prototype.qname == self.qname
        return is_params_valid and is_q_name_valid

