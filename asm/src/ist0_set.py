from instruction import InstructionPrototype
from parameter import Parameter


ist0_set = [
    InstructionPrototype(0x00, 'nop',
                         'no operation',
                         [],
                         0, 0),
    InstructionPrototype(0x01, 'i32',
                         'put one 32 bit integer on stack',
                         [Parameter('val', 'integer value')],
                         0, 1),
    InstructionPrototype(0x02, 'add',
                         'add two 32 bit integers',
                         [],
                         2, 1),
    InstructionPrototype(0x10, 'eq?',
                         'test if two 32 bit integers, producing 0/1 value',
                         [],
                         2, 1),
    InstructionPrototype(0x20, 'jm0',
                         'jump to address if 0 is next value off stack',
                         [Parameter('addr', 'jump address')],
                         1, 0),
    InstructionPrototype(0x21, 'jm1',
                         'jump to address if 1 is next value off stack',
                         [Parameter('addr', 'jump address')],
                         1, 0)
]
