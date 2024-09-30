from abstract_command import AbstractCommand, AbstractCommandPrototype


class InstructionPrototype(AbstractCommandPrototype):
    def __init__(self, iid, qname, doc_text, param_list, consumed, produced):
        super().__init__(qname, doc_text, param_list)
        self.iid = iid
        self.consumed = consumed
        self.produced = produced


class Instruction(AbstractCommand):
    def __init__(self, qname, val_list, prototype):
        super().__init__(qname, val_list, prototype)
