from argparse import ArgumentParser

from instruction_set import InstructionSet
from c_file import CInstructionTemplateWriter, CCodeStyle

if __name__ == '__main__':
    arg_parser = ArgumentParser(prog='svm-asm',
                                description='Assembler for SVM')

    arg_parser.add_argument('-i',
                            dest='input_filename',
                            metavar='input',
                            help='path to SVM instruction set input JSON',
                            default=None)
    arg_parser.add_argument('-o',
                            dest='output_filename',
                            metavar='filename',
                            help='override filename of C template files',
                            default=None)
    arg_parser.add_argument('-p',
                            dest='output_basepath',
                            metavar='basepath',
                            help='path where C instruction set templates should be written to',
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

    output_basepath = args.output_basepath

    if args.output_basepath is None:
        output_basepath = '.'

    instruction_set = InstructionSet(args.input_filename)
    instruction_set.load()

    code_style = CCodeStyle()

    template_writer = CInstructionTemplateWriter(
        output_filename,
        output_basepath,
        args.force_write,
        code_style
    )
    template_writer.write(instruction_set)

    exit(0)
