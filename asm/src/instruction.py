from abstract_command import AbstractCommand, AbstractCommandPrototype


class InstructionPrototype(AbstractCommandPrototype):
    def __init__(self, bin_id, name, doc, params, consumes, produces):
        super().__init__(name, doc, params)
        self.bin_id = int(bin_id, 0)
        self.consumes = consumes
        self.produces = produces

    @property
    def consume_count(self):
        return len(self.consumes)

    @property
    def produce_count(self):
        return len(self.produces)

    @property
    def short_doc(self):
        return '{} {} -{} +{}'.format(
            self.name,
            ' '.join([p.get_short_doc() for p in self.params]),
            len(self.consumes),
            len(self.produces)
        )

    @property
    def full_doc(self):
        def get_param_short_doc(ps):
            return ' '.join([p.short_doc for p in ps])

        def get_param_full_doc(ps,before):
            return ''.join([before + p.full_doc + '\n' for p in ps])

        return '{} {} {{ -[{}] +[{}] }}\n{}\n{}{}{}'.format(
            self.name,
            get_param_short_doc(self.params),
            get_param_short_doc(self.consumes),
            get_param_short_doc(self.produces),
            self.doc,
            get_param_full_doc(self.params, '> '),
            get_param_full_doc(self.consumes, '- '),
            get_param_full_doc(self.produces, '+ ')
        )


class Instruction(AbstractCommand):
    def __init__(self, name, vals, prototype):
        super().__init__(name, vals, prototype)

    @property
    def consumed(self):
        return self.prototype.consumed