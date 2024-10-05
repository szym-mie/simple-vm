class Parameter:
    def __init__(self, name, doc_text):
        self.name = name
        self.doc_text = doc_text

    def get_short_doc(self):
        return '{}'.format(self.name.lower())

    def get_full_doc(self):
        return '> {} - {}'.format(self.name.lower(), self.doc_text)
