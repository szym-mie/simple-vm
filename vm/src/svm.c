#include <stdio.h>

#include "program.h"
#include "set0.h"

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
	program_load(&prog, ist0_set, filename);
	printf("loaded.\n");
	printf("run program...\n");
	program_run(&prog, ist0_set, &stack);
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
