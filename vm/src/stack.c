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
		return STACK_OK;
	}
	return STACK_FULL;
}

int stack_pop(struct stack *stack, int32_t *val)
{
	if (stack->elem_count > 0)
	{
		*val = *(stack->stack + --stack->elem_count);
		return STACK_OK;
	}
	return STACK_EMPTY;
}
