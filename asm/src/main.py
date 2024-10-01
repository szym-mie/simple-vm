from argparse import ArgumentParser

from asm.src.parser import Parser
from binary import BinaryMetadata, BinaryWriter
from ist0_set import ist0_set
from dirv_set import dirv_set

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
    binary_metadata = BinaryMetadata('svm0', 1,
                                     val_width=args.val_byte_size,
                                     byte_order=args.byte_order)

    parser = Parser(ist0_set, dirv_set)

    if args.show_man:
        print(parser.get_full_manual())
        exit(1)

    if args.input_filename is None:
        print('No input file specified')
        exit(2)

    with open(args.output_filename, mode='wb') as out_fp:
        root_parser_context = parser.parse(args.input_filename)
        print(root_parser_context.get_summary())
        writer = BinaryWriter(out_fp, binary_metadata)
        writer.write_binary(root_parser_context.instructions_out)

    exit(0)
