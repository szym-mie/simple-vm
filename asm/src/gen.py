from argparse import ArgumentParser

from instruction_set import InstructionSet
from c_file import CInstructionTemplateWriter, CCodeStyle

if __name__ == '__main__':
    arg_parser = ArgumentParser(prog='svm-asm',
                                description='Assembler for SVM')

    arg_parser.add_argument('-i',
                            dest='input_filename',
                            metavar='input',
                            help='SVM instruction set JSON',
                            default=None)
    arg_parser.add_argument('-o',
                            dest='output_filename',
                            metavar='output',
                            nargs=1,
                            help='assembled SVM binary filename',
                            default=None)
    arg_parser.add_argument('-f',
                            action='store_true',
                            dest='force_write',
                            help='force overwriting of C files',
                            default=False)

    args = arg_parser.parse_args()

    if args.input_filename is None:
        print('No input file specified')
        exit(2)

    output_filename = args.output_filename

    if args.output_filename is None:
        output_filename = args.input_filename

    instruction_set = InstructionSet(args.input_filename)
    instruction_set.load()

    code_style = CCodeStyle()

    template_writer = CInstructionTemplateWriter(
        output_filename,
        args.force_write,
        code_style
    )
    template_writer.write(instruction_set)

    exit(0)
