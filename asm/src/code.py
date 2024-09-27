from textwrap import indent

from directive import Directive
from instruction import Instruction


class CodeParser:
    def __init__(self, instruction_prototype_list, directive_list):
        self.instruction_prototype_list = instruction_prototype_list
        self.directive_list = directive_list

        self.instruction_prototype_dict = {}
        self.directive_dict = {}

        for instruction_prototype in instruction_prototype_list:
            qname = instruction_prototype.qname
            self.instruction_prototype_dict[qname] = instruction_prototype

        for directive in directive_list:
            qname = directive.qname
            self.directive_dict[qname] = directive

    def get_full_manual(self):
        buffer = 'SVM Full Manual\n'

        buffer += '\n# Instructions\n\n'

        for instruction_prototype in self.instruction_prototype_list:
            buffer += indent(instruction_prototype.get_full_doc(), '  ')
            buffer += '\n\n'

        buffer += '\n# Directives\n\n'

        for directive in self.directive_list:
            buffer += indent(directive.get_full_doc(), '  ')
            buffer += '\n\n'

        return buffer

    @staticmethod
    def try_find_prototype(command, prototype_dict, row):
        try:
            prototype = prototype_dict[command.qname]
            if command.is_of_prototype(prototype):
                command.prototype = prototype
            else:
                raise CodeParseError(
                    'invalid number of parameters',
                    'expected {}, actual {}'.format(
                        len(command.val_list),
                        len(prototype.param_list)
                    ),
                    row
                )
        except KeyError:
            raise CodeParseError(
                'unknown name',
                command.qname,
                row
            )

    @staticmethod
    def filter_comment(line):
        comment_start_index = line.find('//')
        if comment_start_index == -1:
            return line
        return line[:comment_start_index]

    @staticmethod
    def is_directive(first_token):
        return first_token.find('@') == 0 and len(first_token) > 1


class CodeParserContext:
    def __init__(self, parser, filename, parent_context=None,
                 no_directives=False):
        self.parser = parser
        self.filename = filename
        self.parent_context = parent_context
        self.symbols_dict = {}
        self.no_directives = no_directives

    def create_inner(self, filename):
        return CodeParserContext(self.parser, filename, self,
                                 self.no_directives)

    def parse(self):
        with open(self.filename, mode='r', encoding='utf-8') as in_fp:
            row = 0
            while True:
                line = in_fp.readline()
                row += 1
                if not line:
                    break
                instruction = self.parse_line(line, row)
                if instruction:
                    yield from instruction

    def parse_line(self, line, row):
        tokens = CodeParser.filter_comment(line).split()
        if len(tokens) > 0:
            if CodeParser.is_directive(tokens[0]):
                if not self.no_directives:
                    yield from self.parse_directive(tokens, row)
            else:
                yield from self.parse_instruction(tokens, row)

    def parse_instruction(self, tokens, row):
        qname, *param_list = tokens
        val_list = [self.parse_val(token, row) for token in param_list]
        instruction = Instruction(qname, val_list)
        CodeParser.try_find_prototype(instruction,
                                      self.parser.instruction_prototype_dict,
                                      row)
        yield instruction

    def parse_directive(self, tokens, row):
        qname, *param_list = tokens
        directive = Directive(qname, param_list)
        CodeParser.try_find_prototype(directive,
                                      self.parser.directive_dict,
                                      row)
        yield from directive.execute(self, row)

    def parse_val(self, token, row):
        # later parse labels
        # try parsing as integer
        try:
            return int(token, base=0)
        except ValueError:
            try:
                return int(self.symbols_dict[token])
            except ValueError:
                raise CodeParseError(
                    'cannot parse int',
                    token,
                    row
                )
            except KeyError:
                raise CodeParseError(
                    'unknown symbol',
                    token,
                    row
                )

    def check_if_cyclic(self):
        context = self.parent_context
        while context is not None:
            if self.filename == context.filename:
                return True
        return False


class CodeParseError(Exception):
    def __init__(self, message, target, row):
        super().__init__('{}: \'{}\' - at line {}'.format(message, target, row))
        self.target = target
        self.row = row
