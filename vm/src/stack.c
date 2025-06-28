#include "stack.h"

void stack_init(struct stack *stack, word_t *stack_mem)
{
    stack->elem_count = 0;
    stack->mem = stack_mem;
}

int stack_push(struct stack *stack, word_t val)
{
    if (stack->elem_count >= stack->max_elem_count)
    {
        event_stack_full("stack_push");
        return STACK_FULL;
    }
    *(stack->mem+stack->elem_count++) = val;
    return STACK_OK;
}

int stack_pop(struct stack *stack, word_t *val)
{
    if (stack->elem_count == 0)
    {
        event_stack_empty("stack_pop");
        return STACK_EMPTY;
    }
    *val = *(stack->mem+--stack->elem_count);
    return STACK_OK;
}
