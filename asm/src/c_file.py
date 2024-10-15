from pathlib import Path


class CInstructionTemplateWriter:
    def __init__(self, filename):
        self.filename = filename

        path_source = Path('{}.c'.format(filename))
        path_include = Path('{}.h'.format(filename))

        if path_source.exists():
            raise RuntimeError('file {} already exists'.format(path_source))
        if path_include.exists():
            raise RuntimeError('file {} already exists'.format(path_include))

        self.path_source = path_source
        self.path_include = path_include

    def write(self, instruction_set):
        instructions = instruction_set.instructions
        count = instruction_set.slot_count

        instr_array_ts = CTypeSpec('struct instr_def', count)
        instr_return_ts = CTypeSpec('void')
        instr_params = [
            CParam(CTypeSpec('loc_t', '*'), 'loc'),
            CParam(CTypeSpec('struct stack', '*'), 'st'),
            CParam(CTypeSpec('const word_t', '*'), 'pv')
        ]

        def create_instr_fn(instr):
            illegal_symbols = '=?!/.>-<'

            escaped_name = instr.name
            for symbol in illegal_symbols:
                escaped_name = escaped_name.replace(symbol, '_')

            return CFuncDefine(
                instr_return_ts,
                '{}_{:02x}'.format(escaped_name, instr.bin_id),
                instr_params,
                [
                    CComment('\'{}\' code here'.format(instr.name))
                ])

        instr_code = []
        entries = [
            {'fn': ('&', 'instr_no_such'), 'params_consumed': 0}
            for _ in range(count)
        ]
        for instruction in instructions:
            pc = instruction.consumed
            bin_id = instruction.bin_id
            fn = create_instr_fn(instruction)
            instr_code.append(fn)
            entries[bin_id] = {'fn': ('&', fn.name), 'params_consumed': pc}
            instr_code.append(Newline())

        code_source = CCode([
            CInclude(self.path_include, False),
            Newline(),
        ] + instr_code + [
            CVarDefine(instr_array_ts, 'ist_set', entries)
        ])

        code_include = CCode([
            CMacroGuard(self.path_include.stem, [
                Newline(),
                CInclude('stdint.h', True),
                Newline(),
                CInclude('instr.h', False),
                CInclude('program.h', False),
                Newline(),
                CVarDeclare(instr_array_ts, 'ist_set', 'extern'),
                Newline(),
            ])
        ])

        with open(self.path_source, mode='w') as fp_source:
            fp_source.write(code_source.get_code())
        with open(self.path_include, mode='w') as fp_include:
            fp_include.write(code_include.get_code())


class CElement:
    def __init__(self, element_name):
        self.element_name = element_name
        self.elements = []
        self.elements_indent = 0

    def __str__(self):
        return self.element_name

    def add_element(self, element):
        self.elements.append(element)

    def add_elements(self, elements):
        for element in elements:
            self.add_element(element)

    def get_elements_code(self):
        code = []
        for element in self.elements:
            code.extend(element.get_code())
        return code

    @staticmethod
    def get_c_value(value):
        if value is None:
            return 'NULL'
        value_t = type(value)
        if value_t is list:
            elements = [CElement.get_c_value(element) for element in value]
            return '{{\n    {}\n}}'.format(',\n    '.join(elements))
        if value_t is dict:
            pairs = [(k, CElement.get_c_value(v)) for k, v in value.items()]
            fields = ['.{} = {}'.format(*pair) for pair in pairs]
            return '{{ {} }}'.format(', '.join(fields))
        if value_t is str:
            return '"{}"'.format(value)
        if value_t is int or value_t is float:
            return str(value)
        if value_t is tuple:
            op, name = value
            return '{}{}'.format(op, name)

    def _get_pre_code(self):
        return []

    def _get_mid_code(self):
        return ['// TODO {}'.format(self.element_name)]

    def _get_post_code(self):
        return []

    def get_code(self):
        pre_code = self._get_pre_code()
        post_code = self._get_post_code()
        indent = lambda t: '{}{}'.format(' ' * self.elements_indent, t)
        mid_code = [indent(line) for line in self._get_mid_code()]

        return pre_code + mid_code + post_code


class Newline(CElement):
    def __init__(self):
        super().__init__('NEWLINE')

    def _get_mid_code(self):
        return ['']


class CCode(CElement):
    def __init__(self, body):
        super().__init__('ROOT')
        self.add_elements(body)

    def _get_mid_code(self):
        return self.get_elements_code()

    def get_code(self):
        return '\n'.join(super().get_code())


class CMacroGuard(CElement):
    def __init__(self, filename, body):
        super().__init__('MACRO_GUARD')
        self.filename = filename
        self.is_preprocessor = True
        self.define_name = '_{}_H_'.format(self.filename.upper())
        self.add_elements(body)

    def _get_mid_code(self):
        return self.get_elements_code()

    def _get_pre_code(self):
        return [
            '#ifndef {}'.format(self.define_name),
            '#define {}'.format(self.define_name)
        ]

    def _get_post_code(self):
        return [
            '#endif//{}'.format(self.define_name)
        ]


class CInclude(CElement):
    def __init__(self, filename, is_std):
        super().__init__('INCLUDE')
        self.filename = filename
        self.is_preprocessor = True
        self.is_std = is_std

    def _get_mid_code(self):
        fmt = ('<{}>' if self.is_std else '"{}"').format(self.filename)
        return ['#include {}'.format(fmt)]


class CComment(CElement):
    def __init__(self, text):
        super().__init__('COMMENT')
        self.text = text

    def _get_mid_code(self):
        return ['// {}'.format(line) for line in self.text.split('\n')]


class CTypeSpec:
    def __init__(self, *spec):
        self.type_name, *self.ptr_array_spec = spec

    def get_c_type(self, name=''):
        ptr_lvl = len([s for s in self.ptr_array_spec if s == '*'])
        ptr_spec = '*' * ptr_lvl
        array_spec = [s for s in self.ptr_array_spec if type(s) is int]
        dim_spec = ''.join(['[{}]'.format(dim) for dim in array_spec])
        return '{} {}{}{}'.format(self.type_name, ptr_spec, name, dim_spec)


class CParam:
    def __init__(self, type_spec, name):
        self.type_spec = type_spec
        self.name = name

    def get_param_text(self):
        return self.type_spec.get_c_type(self.name)

    @staticmethod
    def get_params_text(params):
        return ', '.join([param.get_param_text() for param in params])


class CStorage:
    def __init__(self, storage_spec):
        self.storage_spec = storage_spec

    def get_c_storage_token(self):
        if self.storage_spec is None:
            return ''
        else:
            return self.storage_spec + ' '


class CVarDeclare(CElement):
    def __init__(self, type_spec, name, storage=None):
        super().__init__('VAR_DECLARE')
        self.type_spec = type_spec
        self.name = name
        self.storage = storage + ' ' if storage is not None else ''

    def _get_mid_code(self):
        fmt = (self.storage, self.type_spec.get_c_type(self.name))
        return ['{}{};'.format(*fmt)]


class CVarDefine(CElement):
    def __init__(self, type_spec, name, value, storage=None):
        super().__init__('VAR_DEFINE')
        self.type_spec = type_spec
        self.name = name
        self.value = value
        self.storage = storage + ' ' if storage is not None else ''

    def _get_mid_code(self):
        val = CElement.get_c_value(self.value)
        fmt = (self.storage, self.type_spec.get_c_type(self.name), val)
        return ['{}{} = {};'.format(*fmt)]


class CFuncDefine(CElement):
    def __init__(self, type_spec, name, params, body):
        super().__init__('FUNC_DEFINE')
        self.type_spec = type_spec
        self.name = name
        self.params = params
        self.add_elements(body)
        self.elements_indent = 2

    def _get_pre_code(self):
        params_text = CParam.get_params_text(self.params)
        fmt = (self.type_spec.get_c_type(self.name), params_text)
        return ['{}({})'.format(*fmt), '{']

    def _get_post_code(self):
        return ['}']

    def _get_mid_code(self):
        return self.get_elements_code()

class CFuncCall(CElement):
    def __init__(self, name, params):
        super().__init__('FUNC_CALL')
        self.name = name
        self.params = params

    def _get_mid_code(self):
        params_text = CParam.get_params_text(self.params)
        fmt = (self.name, params_text)
        return ['{}({});'.format(*fmt)]
