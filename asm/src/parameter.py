class Parameter:
    def __init__(self, qname, doc_text):
        self.qname = qname
        self.doc_text = doc_text

    def get_short_doc(self):
        return '{}'.format(self.qname.lower())

    def get_full_doc(self):
        return '> {} - {}'.format(self.qname.lower(), self.doc_text)
