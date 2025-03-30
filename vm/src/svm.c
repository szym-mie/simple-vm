#include <stdio.h>

#include "meta_attr.h"
#include "program.h"
#include "instruction_set_0.h"

int
main(int argc, char *argv[])
{
	// TODO parse arguments
	const char *filename = argv[1];
	struct program prog;
	struct stack stack;
	int32_t stack_arr[1024];

	stack.stack = stack_arr;
	stack.elem_count = 0;
	stack.max_elem_count = 1024;

	printf("load %s...\n", filename);
	program_load(&prog, instr_set, filename);
	printf("loaded.\n");
	printf("meta attributes (%d):\n", prog.meta_attr_count);

	for (slen_t i = 0; i < prog.meta_attr_count; i++)
	{
		struct meta_attr *mattr = prog.meta_attrs+i;
		printf("  %s = \"%s\"\n", mattr->key, mattr->val);
	}

	printf("run program...\n");
	program_run(&prog, instr_set, &stack);
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
