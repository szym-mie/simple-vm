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
        return 'lbl {{ {} 0x{:08x} }}'.format(self.name, self.loc)

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

