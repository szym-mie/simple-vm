class Parameter:
    def __init__(self, name, doc):
        self.name = name
        self.doc = doc

    @property
    def short_doc(self):
        return '{}'.format(self.name.lower())

    @property
    def full_doc(self):
        return '{} : {}'.format(self.name.lower(), self.doc)
