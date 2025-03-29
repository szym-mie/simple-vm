from abstract_command import AbstractCommandPrototype, AbstractCommand


class DirectivePrototype(AbstractCommandPrototype):
    def __init__(self, name, doc, func, params):
        super().__init__(name, doc, params)
        self.func = func

    @property
    def short_doc(self):
        return '{} {}'.format(
            self.name,
            ' '.join([param.short_doc for param in self.params])
        )

    @property
    def full_doc(self):
        return '{} {}\n\n{}\n{}'.format(
            self.name,
            ' '.join([param.short_doc for param in self.params]),
            self.doc,
            '\n'.join([param.full_doc for param in self.params])
        )


class Directive(AbstractCommand):
    def __init__(self, name, val_list, prototype):
        super().__init__(name, val_list, prototype)

    def execute(self, parser_context):
        return self.prototype.func(parser_context, self.val_list)