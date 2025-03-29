import re
from pathlib import Path
from textwrap import indent

from src_struct import Symbol, Label, Immediate
from src_line import SourceLine

from directive import Directive
from directives import directives
from instruction import Instruction


class Parser:
    def __init__(self, instruction_set, **kwargs):
        self.instruction_set = instruction_set

        self.instructions = {}
        for instruction in instruction_set.instructions:
            self.instructions[instruction.name] = instruction

        self.directives = {}
        for directive in directives:
            self.directives[directive.name] = directive

        self.no_substitute = kwargs.get('no_substitute', False)
        self.no_redefine = kwargs.get('no_redefine', False)

    def new_context(self, filename):
        return ParserContext(self, filename)

    def parse(self, filename):
        context = self.new_context(filename)
        context.substitute()
        # for i in context.text_elements:
        #     print(i.filename, i.row, i.body)
        context.build()
        return context

    def get_full_manual(self):
        buffer = 'SVM Full Manual\n'

        buffer += '\n# Instructions\n\n'

        for instruction in self.instructions.values():
            buffer += indent(instruction.full_doc, '  ')
            buffer += '\n\n'

        buffer += '\n# Directives\n\n'

        for directive in self.directives.values():
            buffer += indent(directive.full_doc, '  ')
            buffer += '\n\n'

        return buffer

    @classmethod
    def strip_comment(cls, line):
        comment_start = line.find('//')
        if comment_start == -1:
            return line
        return line[:comment_start]

    @classmethod
    def tokenize_line(cls, line):
        line_content = cls.strip_comment(line)
        is_quoted = False
        token_acc = ''
        token_list = []
        last_char = ''

        for char in line_content:
            if char in (' ', '\n') and not is_quoted:
                if len(token_acc) > 0:
                    token_list.append(token_acc)
                token_acc = ''
            elif last_char != '\\' and char == '"':
                is_quoted = not is_quoted
            else:
                token_acc += char
            last_char = char

        if len(token_acc) > 0:
            token_list.append(token_acc)

        return token_list

    @classmethod
    def join_line(cls, line_tokens):
        return ' '.join(line_tokens)

    @classmethod
    def is_directive(cls, name):
        return Parser._directive_filter.fullmatch(name) is not None

    @classmethod
    def is_label(cls, name):
        return Parser._label_filter.fullmatch(name) is not None

    @classmethod
    def is_instruction(cls, name):
        return Parser._instruction_filter.fullmatch(name) is not None

    @classmethod
    def is_int(cls, value):
        return Parser._int_filter.fullmatch(value) is not None

    @classmethod
    def is_float(cls, value):
        return Parser._float_filter.fullmatch(value) is not None

    @classmethod
    def is_str(cls, value):
        return Parser._str_filter.fullmatch(value) is not None

    @classmethod
    def is_value(cls, value):
        return cls.is_int(value) or cls.is_float(value) or cls.is_str(value)

    _directive_filter = re.compile('^@[a-zA-Z0-9_]+$')
    _label_filter = re.compile('^[a-zA-Z0-9_]+:$')
    _instruction_filter = re.compile('^[a-zA-Z0-9_./!?>=<]+$')
    _int_filter = re.compile('^-?(([0-9]+)|(0x[0-9a-fA-F]+)|(0b[0-1]+))$')
    _float_filter = re.compile('^-?([0-9]*\\.[0-9]+)$')
    _str_filter = re.compile('^"((\\\\")|[^"])*"$')


class ParserContext:
    def __init__(self, parser, filename, parent=None):
        self.parser = parser
        self.filename = filename
        self.base_path = Path(filename).parent
        self.parent = parent

        # TODO update source info
        self.current_row = 0
        self.current_source_info = None
        self.current_loc = 0

        self.defined_symbols = {}
        self.defined_labels = {}
        self.defined_meta_attrs = {}

        if self.has_cycles():
            ParserError.just('import cycle detected', self.filename)

        self.text_source = self.read_text_lines(self.filename)
        self.text_elements = []
        self.instructions_out = []

    def raise_error(self, message, target):
        if self.current_source_info is not None:
            ParserError.with_source(message, target, self.current_source_info)
        else:
            ParserError.just(message, target)

    def get_root(self):
        ctx = self
        while ctx.parent is not None:
            ctx = ctx.parent
        return ctx

    def set_meta_attr(self, key, value):
        self.defined_meta_attrs[key] = value

    def get_meta_attr(self, key):
        ctx = self
        while ctx.parent is not None:
            try:
                return ctx.defined_meta_attrs[key]
            except KeyError:
                ctx = ctx.parent
        return None

    def new_child_context(self, filename):
        context = ParserContext(self.parser, filename, self)
        context.reset(self.current_loc)
        return context

    def update_parent(self):
        if self.parent is not None:
            self.parent.current_loc += self.current_loc

    def has_symbol_or_label(self, name):
        return name in self.defined_symbols or name in self.defined_labels

    def define_symbol(self, name, text):
        if name in self.defined_symbols:
            self.raise_error('redefined symbol', name)
        if self.has_symbol_or_label(name):
            self.raise_error('label with this name already defined', name)
        self.defined_symbols[name] = Symbol(name, text)

    def defer_label(self, name):
        if name in self.defined_labels:
            label = self.defined_labels[name]
            if label.is_bound():
                self.raise_error('duplicate label', name)
            return label
        elif self.has_symbol_or_label(name):
            self.raise_error('symbol with this name already defined', name)
        else:
            label = Label(name, None)
            self.defined_labels[name] = label
            return label

    def define_label(self, name):
        if name in self.defined_labels:
            label = self.defined_labels[name]
            if label.is_bound():
                self.raise_error('duplicate label', name)
            else:
                label.loc = self.current_loc
        elif self.has_symbol_or_label(name):
            self.raise_error('symbol with this name already defined', name)
        else:
            self.defined_labels[name] = Label(name, self.current_loc)

    def get_instruction_prototype(self, name):
        try:
            return self.parser.instructions[name]
        except KeyError:
            self.raise_error('unknown instruction', name)

    def get_directive_prototype(self, name):
        try:
            return self.parser.directives[name]
        except KeyError:
            self.raise_error('unknown directive', name)

    def reset(self, prev_loc=0):
        self.current_row = 0
        self.current_loc = prev_loc

    def add_text_source(self, source_lines):
        row = self.current_row + 1
        for source_line in source_lines:
            self.text_source.insert(row, source_line)
            row += 1

    def substitute(self):
        for line in self.text_source:
            if not line.is_final:
                # if not substituted already
                tokens = self.parser.tokenize_line(line.text)
                if len(tokens) > 0:
                    name, *params = tokens
                    if Parser.is_directive(name):
                        # on directive
                        directive_prototype = self.get_directive_prototype(name)
                        directive = Directive(name, params, directive_prototype)
                        directive.prototype = directive_prototype
                        if not directive.verify():
                            self.raise_error('invalid parameters passed', name)
                        directive.execute(self)
                    elif Parser.is_label(name):
                        # on label link program location to label
                        self.define_label(name)
                    else:
                        # on instruction expand parameters lazily
                        params_expanded = []
                        for param in params:
                            symbol = self.defined_symbols.get(param)
                            label = self.defined_labels.get(param)
                            if label is not None:
                                # found a known label (might be empty)
                                params_expanded.append(label)
                            elif symbol is not None:
                                # found a symbol
                                params_expanded.append(symbol)
                            elif Parser.is_value(param):
                                # found just a value
                                params_expanded.append(Immediate(param))
                            elif Parser.is_label(param):
                                # new label, defer define it (leave empty)
                                params_expanded.append(self.defer_label(param))
                            else:
                                # else just some unknown symbol
                                self.raise_error('unknown symbol', param)

                        imm = Immediate(name)
                        line_elements = [imm] + params_expanded
                        self.text_elements.append(line.map(line_elements))

                    if Parser.is_instruction(name):
                        self.current_loc += 1
            else:
                # already expanded in offspring context
                name, *params = line.body
                self.text_elements.append(line)
                if Parser.is_instruction(name.value):
                    self.current_loc += 1
            self.current_row += 1

    def parse_val(self, token):
        try:
            if type(token) is int:
                return token
            elif type(token) is str:
                return int(token, base=0)
            else:
                self.raise_error('not an int/str', token)
        except ValueError:
            self.raise_error('cannot parse int', token)

    def build(self):
        for line in self.text_elements:
            name, *params = line.body
            vals = [self.parse_val(param.value) for param in params]
            instruction_prototype = self.get_instruction_prototype(name.value)
            instruction = Instruction(name.value, vals, instruction_prototype)
            # TODO add reliable row information
            if not instruction.verify():
                self.raise_error('invalid parameters passed', name)
            self.instructions_out.append(instruction)

    def get_summary(self):
        buffer = 'Build Summary\n'

        buffer += '\nInstruction Stream:\n'
        buffer += '@loc       | instruction\n'
        loc = 0
        for line in self.text_elements:
            buffer += '0x{:08x} | {}\n'.format(loc, line.body_text)
            loc += 1

        return buffer

    def read_text_lines(self, filename):
        path = Path('.') if self.parent is None else self.parent.base_path
        with open(path.joinpath(filename), mode='r', encoding='ascii') as fp:
            return [SourceLine(filename, text, row)
                    for row, text in enumerate(fp.readlines())]

    def has_cycles(self):
        context = self.parent
        while context is not None:
            if self.filename == context.filename:
                return True
            context = context.parent
        return False


class ParserError(Exception):
    def __init__(self, message, target, extra_info, text):
        super().__init__(text)
        self.message = message
        self.target = target
        self.extra_info = extra_info

    @classmethod
    def just(cls, message, target):
        raise cls(message, target, None, '{}: {}\n'.format(
                message, target))

    @classmethod
    def with_source(cls, message, target, source_info):
        info = source_info.get_long_info()
        text = indent(source_info.to_text(), '    ')

        raise cls(message, target, source_info, '{}: {} - {}\n{}'.format(
            message, target, info, text))

    @classmethod
    def with_any(cls, message, target, extra):
        raise cls(message, target, extra, '{}: {}\n  extra: \n'.format(
            message, target, str(extra)))