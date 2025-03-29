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
        for i in context.text_elements:
            print(i.filename, i.row, i.body)
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


class Immediate:
    def __init__(self, text):
        self.text = text

    @property
    def value(self):
        return self.text

    def __repr__(self):
        return 'imm {{ "{}" }}'.format(self.text)


class Symbol:
    def __init__(self, name, text):
        self.name = name
        self.text = text

    @property
    def value(self):
        return self.text

    def __repr__(self):
        return 'sym {{ {}="{}" }}'.format(self.name, self.text)

class Label:
    def __init__(self, name, loc):
        self.name = name
        self.loc = loc

    @property
    def value(self):
        return self.loc

    def is_bound(self):
        return self.loc is not None

    def __str__(self):
        return 'label {{ {} 0x{:08x} }}'.format(self.name, self.loc)

    def __repr__(self):
        return self.__str__()


class MetaAttrEntry:
    def __int__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return 'meta {{ {}="{}" }}'.format(self.key, self.value)

    def __repr__(self):
        return self.__str__()


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
            print('body:' + str(line.body))
            tokens = self.parser.tokenize_line(line.body)
            if len(tokens) > 0:
                name, *params = tokens
                if Parser.is_directive(name):
                    directive_prototype = self.get_directive_prototype(name)
                    directive = Directive(name, params, directive_prototype)
                    directive.prototype = directive_prototype
                    if not directive.verify():
                        self.raise_error('invalid parameters passed', name)
                    directive.execute(self)
                elif Parser.is_label(name):
                    self.define_label(name)
                else:
                    params_expanded = []
                    for param in params:
                        print(param)
                        symbol = self.defined_symbols.get(param)
                        label = self.defined_labels.get(param)
                        print(symbol)
                        print(label)
                        if label is not None:
                            params_expanded.append(label)
                        elif symbol is not None:
                            params_expanded.append(symbol)
                        elif Parser.is_value(param):
                            params_expanded.append(Immediate(param))
                        elif Parser.is_label(param):
                            params_expanded.append(self.defer_label(param))
                        else:
                            self.raise_error('unknown symbol', param)

                    imm = Immediate(name)
                    line_elements = [imm] + params_expanded
                    self.text_elements.append(line.map(line_elements))

                if self.parser.is_instruction(name):
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
            print(name, params)
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
            buffer += '0x{:08x} | {}\n'.format(loc, line.text)
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


class SourceLine:
    def __init__(self, filename, body, row):
        self.filename = filename
        self.body = body
        self.row = row

    def map(self, new_text):
        return SourceLine(self.filename, new_text, self.row)

    def get_short_info(self):
        return '{}:{}'.format(self.filename, self.row)

    def get_long_info(self):
        return 'in \'{}\' at line {}'.format(self.filename, self.row)

    @property
    def text(self):
        return ' '.join([str(elem) for elem in self.body])


class SourceLinePart(SourceLine):
    def __init__(self, source_line, col_start=None, col_end=None):
        super().__init__(
            source_line.filename, source_line.body, source_line.row)
        self.col_start = col_start
        self.col_end = col_end
        if self.col_start is None or self.col_end is None:
            self.col_len = 0
        else:
            self.col_len = col_end - col_start

    @property
    def text(self):
        return '{}\n{}'.format(self.body, self.get_underline('~'))

    def get_underline(self, char):
        space = ' ' * self.col_start
        underline = char * self.col_len
        return space + underline

    @classmethod
    def of_whole_line(cls, source_line):
        return cls(source_line)

    @classmethod
    def of_line_part(cls, source_line, col_start, col_end):
        return cls(source_line, col_start, col_end)

    @classmethod
    def of_line_word(cls, source_line, word):
        word_len = len(word)
        word_col_start = source_line.body.find(word)
        word_col_end = word_col_start + word_len
        if word_col_start == -1:
            return cls.of_whole_line(source_line)
        return cls.of_line_part(source_line, word_col_start, word_col_end)


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