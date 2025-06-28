from directive import DirectivePrototype
from parameter import Parameter


def directive_import(parser_context, vals):
    filename, *_rest = vals
    child_parser_context = parser_context.new_child_context(filename)
    child_parser_context.substitute()
    parser_context.add_text_source(child_parser_context.text_elements)

def directive_define(parser_context, vals):
    name, replacement, *_rest = vals
    parser_context.define_symbol(name, replacement)

def directive_meta(parser_context, vals):
    meta_key, meta_value, *_rest = vals
    parser_context.set_meta_attr(meta_key, meta_value)

def directive_start(parser_context, vals):
    pass

def directive_struct(parser_context, vals):
    struct_name, *fields = vals
    offset = 0
    for field in fields:
        field_name, field_size = field.split(':')
        name = f'{struct_name}.{field_name}'
        parser_context.define_symbol(name, offset)
        offset += int(field_size)

directives = [
    DirectivePrototype(
                        '@import',
                        'include complete source code:\n' \
                        '@import code.svm',
                        directive_import,
                        [Parameter('file', 'filename to be included')]),
    DirectivePrototype(
                        '@define',
                        'replace symbols after define with value:\n' \
                        '@define a 0x56',
                        directive_define,
                        [
                            Parameter('name', 'name to be replaced'),
                            Parameter('value', 'replacement string')
                        ]),
    DirectivePrototype(
                        '@meta',
                        'define meta attribute:\n' \
                        '@meta name "EXAMPLE"',
                        directive_meta,
                        [
                            Parameter('key', 'attribute key'),
                            Parameter('value', 'attribute value string')
                        ]),
    DirectivePrototype(
                        '@start', 
                        'set entrypoint label:\n' \
                        '@start _main',
                        directive_start,
                        [Parameter('label', 'label name')]),
    DirectivePrototype(
                        '@struct',
                        'create struct address offsets macros\n' \
                        '@struct data a:4 b:1',
                        directive_struct,
                        [
                            Parameter('name', 'name of struct'),
                            Parameter('...fields', 'field as <name>:<bytes>')
                        ])
]
