#ifndef _STACK_H_
#define _STACK_H_

#include <stdint.h>

struct stack
{
	uint32_t elem_count;
	uint32_t max_elem_count;
	int32_t *stack;
};

void stack_init(struct stack *stack, int32_t *stack_mem);
int stack_push(struct stack *stack, int32_t val);
int stack_pop(struct stack *stack, int32_t *val);

#endif//_STACK_H_
