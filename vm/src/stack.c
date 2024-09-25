#include "stack.h"

void stack_init(struct stack *stack, int32_t *stack_mem)
{
	stack->elem_count = 0;
	stack->stack = stack_mem;
}

int stack_push(struct stack *stack, int32_t val)
{
	if (stack->elem_count < stack->max_elem_count)
	{
		*(stack->stack + stack->elem_count++) = val;
		return 1;
	}
	return 0;
}

int stack_pop(struct stack *stack, int32_t *val)
{
	if (stack->elem_count > 0)
	{
		*val = *(stack->stack + --stack->elem_count);
		return 1;
	}
	return 0;
}
