from abstract_command import AbstractCommandPrototype, AbstractCommand


class DirectivePrototype(AbstractCommandPrototype):
    def __init__(self, name, doc_text, func, param_list):
        super().__init__(name, doc_text, param_list)
        self.func = func


class Directive(AbstractCommand):
    def __init__(self, name, val_list, prototype):
        super().__init__(name, val_list, prototype)

    def execute(self, parser_context):
        return self.prototype.func(parser_context, self.val_list)