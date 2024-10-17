from argparse import ArgumentParser

from instruction_set import InstructionSet
from c_file import CInstructionTemplateWriter, CCodeStyle

if __name__ == '__main__':
    arg_parser = ArgumentParser(prog='svm-asm',
                                description='Assembler for SVM')

    arg_parser.add_argument('-i',
                            dest='input_filename',
                            metavar='input',
                            help='SVM code filename',
                            default=None)
    arg_parser.add_argument('-m', '--man',
                            action='store_true',
                            dest='show_man',
                            help='show full instruction and directive manual',
                            default=False)
    arg_parser.add_argument('-o',
                            dest='output_filename',
                            metavar='output',
                            nargs=1,
                            help='assembled SVM binary filename',
                            default='aaa.svm.out')
    arg_parser.add_argument('--val-size',
                            dest='val_byte_size',
                            metavar='byte_size',
                            help='override value byte size',
                            default=4)
    arg_parser.add_argument('--byte-order',
                            dest='byte_order',
                            metavar='le/be',
                            help='specify which byte order to use (le/be)',
                            default='le')

    args = arg_parser.parse_args()

    if args.input_filename is None:
        print('No input file specified')
        exit(2)

    instruction_set = InstructionSet(args.input_filename)
    instruction_set.load()

    code_style = CCodeStyle()

    with open(args.output_filename, mode='w') as out_fp:
        template_writer = CInstructionTemplateWriter('test', code_style)
        template_writer.write(instruction_set)

    exit(0)
