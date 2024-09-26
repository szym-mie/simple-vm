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
    InstructionPrototype(0x03, 'dec',
                         'decrement top of the stack',
                         [],
                         0, 0),
    InstructionPrototype(0x10, 'eq?',
                         'test if two 32 bit integers, producing 0/1 value',
                         [],
                         2, 1),
    InstructionPrototype(0x11, 'ez?',
                         'test if top of stack is zero, producing 0/1 value',
                         [],
                         0, 1),
    InstructionPrototype(0x20, 'jez',
                         'jump to address if 0 is popped from the stack',
                         [Parameter('addr', 'jump address')],
                         1, 0),
    InstructionPrototype(0x21, 'jnz',
                         'jump to address if 1 is popped from the stack',
                         [Parameter('addr', 'jump address')],
                         1, 0)
]
