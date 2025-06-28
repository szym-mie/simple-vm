#include <stdio.h>

#include "meta_attr.h"
#include "program.h"
#include "instruction_set_0.h"

static char *input = "aaa.svm.out";
static int help = 0;
static int verbose = 0;

enum parse_state
{
	PS_ACCEPT, // accept new option
	PS_HELP, // -h
	PS_INPUT, // -i
	PS_INPUT_FILENAME, // -i filename
	PS_VERBOSE, // -v
	PS_EXTRA, // -x
	PS_EXTRA_FLAG // -x flag
};

int
parse_args(int argc, char **argv)
{
#define IS_SHORT_OPT(ARG, OPT) ( \
	*(ARG+0) == '-' &&           \
	*(ARG+1) == OPT &&           \
	*(ARG+2) == '\0')
#define HANDLE_OPT(PS) { state = PS; break; }
	argv++;
	enum parse_state state = PS_ACCEPT;
	for (int argi = 0; argi < argc; argi++)
	{
		char *arg = *argv++;
		switch (state)
		{
			case PS_ACCEPT:
				if (IS_SHORT_OPT(arg, 'h')) HANDLE_OPT(PS_HELP)
				if (IS_SHORT_OPT(arg, 'i')) HANDLE_OPT(PS_INPUT)
				if (IS_SHORT_OPT(arg, 'v')) HANDLE_OPT(PS_VERBOSE)
				if (IS_SHORT_OPT(arg, 'x')) HANDLE_OPT(PS_EXTRA)
				printf("unknown option: %s\n", arg);
				return 0;
			case PS_HELP:
				help = 1;
				state = PS_ACCEPT;
				break;
			case PS_INPUT:
				state = PS_INPUT_FILENAME;
				break;
			case PS_INPUT_FILENAME:
				input = arg;
				state = PS_ACCEPT;
				break;
			case PS_VERBOSE:
				verbose = 1;
				state = PS_ACCEPT;
				break;
			case PS_EXTRA:
				state = PS_EXTRA_FLAG;
				break;
			case PS_EXTRA_FLAG:
				// TODO: add extra flag
				state = PS_ACCEPT;
				break;
		}
	}
	return 1;
#undef IS_SHORT_OPT
#undef HANDLE_OPT
}

void
display_help(void) 
{
	printf(
		"usage: svm-vm [-h] [-i input] [-v] [-x flag]...\n\n" \
		"Virtual machine for SVM\n\n"                         \
		"options:\n"                                          \
		"  -h        show this help message and exit\n"       \
		"  -i input  SVM bytecode filename\n"                 \
		"  -v        verbose output\n"                        \
		"  -x flag   extra option\n"
	);
}

int
main(int argc, char **argv)
{
	// TODO parse arguments
	if (!parse_args(argc, argv)) 
	{
		printf("cannot read options\n");
		return 2;
	}
	if (help) {
		display_help();
		return 0;
	}
	struct program prog;

	struct stack stack;
	int32_t stack_arr[1024];

	stack.mem = stack_arr;
	stack.elem_count = 0;
	stack.max_elem_count = 1024;

	struct heap heap;
	int32_t heap_arr[4096];

	heap.mem.m4 = heap_arr;
	heap.addr_end = 4096;

	printf("load %s...\n", input);
	if (!program_load(&prog, instr_set, input))
	{
		printf("cannot load program.\n");
		return 3;
	}
	printf("loaded.\n");
	printf("meta attributes (%d):\n", prog.meta_attr_count);

	for (slen_t i = 0; i < prog.meta_attr_count; i++)
	{
		struct meta_attr *mattr = prog.meta_attrs+i;
		printf("  %s = \"%s\"\n", mattr->key, mattr->val);
	}

	printf("run program...\n");
	if (!program_run(&prog, instr_set, &stack, &heap))
	{
		printf("program run failed");
		return 4;
	}
	printf("end stack:\n\n");
	
	for (;;)
	{
		int32_t v;
		if (!stack_pop(&stack, &v)) break;
		printf("  | 0x%08x |\n", v);
	}

	printf("  +------------+\n");
	printf("exit.\n");

	return 0;
}
