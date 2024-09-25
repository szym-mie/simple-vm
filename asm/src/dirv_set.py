from directive import DirectivePrototype
from parameter import Parameter


def dirv_import(parser_context, val_list, row):
    filename, *_rest = val_list
    yield from parser_context.create_inner(filename).parse()

def dirv_define(parser_context, val_list, row):
    print('@define TODO')
    pass

dirv_set = [
    DirectivePrototype('@import',
                       'include complete code source',
                       dirv_import,
                       [Parameter('file', 'filename to be included')]),
    DirectivePrototype('@define',
                       'replace names in this file (also imported) with value',
                       dirv_define,
                       [
                           Parameter('name', 'name to be replaced'),
                           Parameter('value', 'replacement string')
                       ])
]
