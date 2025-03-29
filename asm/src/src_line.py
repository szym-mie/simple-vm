class SourceLine:
    def __init__(self, filename, text, row):
        self.filename = filename
        self.text = text
        self.body = None
        self.row = row

    def map(self, body):
        self.body = body
        return self

    @property
    def is_final(self):
        return self.body is not None

    @property
    def short_info(self):
        return '{}:{}'.format(self.filename, self.row)

    @property
    def long_info(self):
        return 'in \'{}\' at line {}'.format(self.filename, self.row)

    @property
    def body_text(self):
        return ' '.join([str(elem) for elem in self.body])


class SourceLinePart(SourceLine):
    def __init__(self, source_line, col_start=None, col_end=None):
        super().__init__(
            source_line.filename, source_line.text, source_line.row)
        self.col_start = col_start
        self.col_end = col_end
        if self.col_start is None or self.col_end is None:
            self.col_len = 0
        else:
            self.col_len = col_end - col_start

    @property
    def highlight(self):
        return '{}\n{}'.format(self.text, self.get_underline('~'))

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
