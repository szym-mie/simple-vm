#ifndef _STACK_H_
#define _STACK_H_

#include "def.h"
#include "event.h"

#define STACK_OK 1
#define STACK_FULL 0
#define STACK_EMPTY 0

struct stack
{
	addr_t elem_count;
	addr_t max_elem_count;
	word_t *mem;
};

void stack_init(struct stack *stack, word_t *stack_mem);
int stack_push(struct stack *stack, word_t val);
int stack_pop(struct stack *stack, word_t *val);

#endif//_STACK_H_
