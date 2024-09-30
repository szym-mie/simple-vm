from directive import DirectivePrototype
from parameter import Parameter


def dirv_import(parser_context, val_list):
    filename, *_rest = val_list
    child_parser_context = parser_context.child_context(filename)
    child_parser_context.substitute()
    parser_context.add_text_source(child_parser_context.text_expanded)

def dirv_define(parser_context, val_list):
    name, replacement, *_rest = val_list
    parser_context.define_symbol(name, replacement)

dirv_set = [
    DirectivePrototype('@import',
                       'include complete code source',
                       dirv_import,
                       [Parameter('file', 'filename to be included')]),
    DirectivePrototype('@define',
                       'replace symbols after define with value',
                       dirv_define,
                       [
                           Parameter('name', 'name to be replaced'),
                           Parameter('value', 'replacement string')
                       ])
]
