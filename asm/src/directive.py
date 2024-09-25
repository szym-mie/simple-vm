from abstract_command import AbstractCommandPrototype, AbstractCommand


class DirectivePrototype(AbstractCommandPrototype):
    def __init__(self, qname, doc_text, func, param_list):
        super().__init__(qname, doc_text, param_list)
        self.func = func


class Directive(AbstractCommand):
    def __init__(self, qname, val_list):
        super().__init__(qname, val_list)

    def execute(self, parser_context, row):
        return self.prototype.func(parser_context, self.val_list, row)