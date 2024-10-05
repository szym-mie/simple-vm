from abstract_command import AbstractCommand, AbstractCommandPrototype


class InstructionPrototype(AbstractCommandPrototype):
    def __init__(self, bin_id, name, doc_text, param_list, consumed, produced):
        super().__init__(name, doc_text, param_list)
        self.bin_id = int(bin_id, 0)
        self.consumed = consumed
        self.produced = produced


class Instruction(AbstractCommand):
    def __init__(self, name, val_list, prototype):
        super().__init__(name, val_list, prototype)
