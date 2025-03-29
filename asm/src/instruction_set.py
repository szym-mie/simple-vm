from json import load

from parameter import Parameter
from instruction import InstructionPrototype


class InstructionSet:
    def __init__(self, filename):
        self.filename = filename
        self.name = None
        self.author = None
        self.instructions = []

    @property
    def max_bin_id(self):
        return max([instr.bin_id for instr in self.instructions])

    @property
    def slot_count(self):
        return self.max_bin_id + 1

    def load(self):
        with open(self.filename, 'r') as fp:
            raw_json = load(fp)
            self.name = raw_json.get('name', 'UNKNOWN')
            self.author = raw_json.get('author', 'UNKNOWN')
            raw_instructions = raw_json.get('instructions', [])

            if len(raw_instructions) == 0:
                raise ValueError('instruction set is empty')

            for raw_instruction in raw_instructions:
                def try_get_instruction_property(key):
                    try:
                        return raw_instruction[key]
                    except KeyError:
                        instruction_name = raw_instruction.get('name', '')
                        message = 'missing \'{}\' property'.format(key)
                        raise InstructionLoadError(message, instruction_name)

                def get_params(raw_params):
                    params = []
                    for raw_param in raw_params:
                        def try_get_param_property(key):
                            try:
                                return raw_param[key]
                            except KeyError:
                                param_name = raw_param.get('name', '')
                                message = 'missing \'{}\' property'.format(key)
                                raise InstructionLoadError(message, param_name)

                        param = Parameter(
                            try_get_param_property('name'),
                            try_get_param_property('doc')
                        )
                        params.append(param)
                    return params

                instruction = InstructionPrototype(
                    try_get_instruction_property('id'),
                    try_get_instruction_property('name'),
                    try_get_instruction_property('doc'),
                    get_params(try_get_instruction_property('params')),
                    get_params(try_get_instruction_property('consumed')),
                    get_params(try_get_instruction_property('produced'))
                )
                self.instructions.append(instruction)


class InstructionLoadError(Exception):
    def __init__(self, instruction_name, message):
        super().__init__('{}: {}'.format(
            message, instruction_name))
        self.instruction_name = instruction_name
        self.message = message