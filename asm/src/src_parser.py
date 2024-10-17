import re
from pathlib import Path
from textwrap import indent

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
        context.build()
        return context

    def get_full_manual(self):
        buffer = 'SVM Full Manual\n'

        buffer += '\n# Instructions\n\n'

        for instruction in self.instructions:
            buffer += indent(instruction.get_full_doc(), '  ')
            buffer += '\n\n'

        buffer += '\n# Directives\n\n'

        for directive in self.directives:
            buffer += indent(directive.get_full_doc(), '  ')
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
        return Parser.directive_filter.search(name) is not None

    @classmethod
    def is_label(cls, name):
        return Parser.label_filter.search(name) is not None

    @classmethod
    def is_instruction(cls, name):
        return Parser.instruction_filter.search(name) is not None

    directive_filter = re.compile('^@[a-zA-Z0-9_]+$')
    label_filter = re.compile('^[a-zA-Z0-9_]+:$')
    instruction_filter = re.compile('^[a-zA-Z0-9_./!?>=<]+$')


class ParserContext:
    def __init__(self, parser, filename, parent=None):
        self.parser = parser
        self.filename = filename
        self.base_path = Path(filename).parent
        self.parent = parent

        self.current_row = 0
        self.current_loc = 0

        self.defined_symbols = {}
        self.defined_labels = {}
        self.defined_meta_attrs = {}

        if self.has_cycles():
            self.raise_error('import cycle detected', self.filename)

        self.text_source = self.read_text_lines(self.filename)
        self.text_expanded = []
        self.instructions_out = []

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

    def raise_error(self, message, target):
        raise ParserError(message, target, self.filename, self.current_row)

    def has_symbol_or_label(self, name):
        return name in self.defined_symbols or name in self.defined_labels

    def define_symbol(self, symbol, text):
        if symbol in self.defined_symbols:
            self.raise_error('redefined symbol', symbol)
        if self.has_symbol_or_label(symbol):
            self.raise_error('label with this name already defined', symbol)
        self.defined_symbols[symbol] = text

    def define_label(self, label):
        if label in self.defined_labels:
            self.raise_error('duplicate label', label)
        if self.has_symbol_or_label(label):
            self.raise_error('symbol with this name already defined', label)
        self.defined_labels[label] = self.current_loc

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

    def add_text_source(self, lines):
        row = self.current_row + 1
        for line in lines:
            self.text_source.insert(row, line)
            row += 1

    def substitute(self):
        for line in self.text_source:
            tokens = self.parser.tokenize_line(line)
            if len(tokens) > 0:
                name, *params = tokens
                if self.parser.is_directive(name):
                    directive_prototype = self.get_directive_prototype(name)
                    directive = Directive(name, params, directive_prototype)
                    directive.prototype = directive_prototype
                    if not directive.verify():
                        self.raise_error('invalid parameters passed', name)
                    directive.execute(self)
                elif self.parser.is_label(name):
                    self.define_label(name)
                else:
                    params_expanded = []
                    for param in params:
                        symbol = self.defined_symbols.get(param)
                        label = self.defined_labels.get(param)
                        if label is not None:
                            params_expanded.append(str(label))
                        elif symbol is not None:
                            params_expanded.append(str(symbol))
                        else:
                            params_expanded.append(param)

                    line = self.parser.join_line([name] + params_expanded)
                    self.text_expanded.append(line)

                if self.parser.is_instruction(name):
                    self.current_loc += 1
            self.current_row += 1

    def parse_val(self, token):
        try:
            return int(token, base=0)
        except ValueError:
            self.raise_error('cannot parse int', token)

    def build(self):
        for line in self.text_expanded:
            tokens = self.parser.tokenize_line(line)
            name, *params = tokens
            vals = [self.parse_val(param) for param in params]
            instruction_prototype = self.get_instruction_prototype(name)
            instruction = Instruction(name, vals, instruction_prototype)
            # TODO add reliable row information
            if not instruction.verify():
                self.raise_error('invalid parameters passed', name)
            self.instructions_out.append(instruction)

    def get_summary(self):
        buffer = 'Build Summary\n'

        buffer += '\nInstruction Stream:\n'
        buffer += '@loc | instruction\n'
        loc = 0
        for line in self.text_expanded:
            buffer += '{:4} | {}\n'.format(loc, line)
            loc += 1

        return buffer

    def read_text_lines(self, filename):
        path = Path('.') if self.parent is None else self.parent.base_path
        with open(path.joinpath(filename), mode='r', encoding='ascii') as fp:
            return fp.readlines()

    def has_cycles(self):
        context = self.parent
        while context is not None:
            if self.filename == context.filename:
                return True
            context = context.parent
        return False


class ParserError(Exception):
    def __init__(self, message, target, file, row):
        super().__init__('{}: {} - \'{}\' at line {}'.format(
            message, target, file, row))
        self.target = target
        self.file = file
        self.row = row
