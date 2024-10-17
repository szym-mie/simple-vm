from directive import DirectivePrototype
from parameter import Parameter


def directive_import(parser_context, val_list):
    filename, *_rest = val_list
    child_parser_context = parser_context.new_child_context(filename)
    child_parser_context.substitute()
    parser_context.add_text_source(child_parser_context.text_expanded)

def directive_define(parser_context, val_list):
    name, replacement, *_rest = val_list
    parser_context.define_symbol(name, replacement)

def directive_meta(parser_context, val_list):
    meta_key, meta_value, *_rest = val_list
    parser_context.set_meta_attr(meta_key, meta_value)

directives = [
    DirectivePrototype('@import',
                       'include complete code source',
                       directive_import,
                       [Parameter('file', 'filename to be included')]),
    DirectivePrototype('@define',
                       'replace symbols after define with value',
                       directive_define,
                       [
                           Parameter('name', 'name to be replaced'),
                           Parameter('value', 'replacement string')
                           ]),
    DirectivePrototype('@meta',
                       'define meta attribute',
                       directive_meta,
                       [
                           Parameter('key', 'attribute key'),
                           Parameter('value', 'attribute value string')
                           ])
]
