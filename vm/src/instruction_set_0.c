#include "instruction_set_0.h"

void nop_00(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
}

void i32_01(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
    stack_push(st, *pv);
	*loc = *loc + 1;
}

void add_02(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
	int32_t a, b;
	stack_pop(st, &a);
	stack_pop(st, &b);
    stack_push(st, a + b);
	*loc = *loc + 1;
}

void dec_03(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
	int32_t a;
	stack_pop(st, &a);
	stack_push(st, a - 1);
	*loc = *loc + 1;
}

void eq__10(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
	int32_t a, b;
	stack_pop(st, &a);
	stack_pop(st, &b);
    stack_push(st, a == b);
	*loc = *loc + 1;
}

void ez__11(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
	int32_t a;
	stack_pop(st, &a);
	stack_push(st, a);
	stack_push(st, a == 0);
	*loc = *loc + 1;
}

void jez_20(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
	int32_t a;
	stack_pop(st, &a);
	*loc = a == 0 ? *pv : *loc + 1;
}

void jnz_21(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
	int32_t a;
	stack_pop(st, &a);
	*loc = a != 0 ? *pv : *loc + 1;
}

void ldi_40(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
    int32_t val;
    heap_load(hp, *pv, &val);
    stack_push(st, val);
    *loc = *loc + 1;
}

void lds_41(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
    int32_t addr, val;
    stack_pop(st, &addr);
    heap_load(hp, *pv, &val);
    stack_push(st, val);
    *loc = *loc + 1;
}

void sti_42(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
    int32_t val;
    stack_pop(st, &val);
    heap_store(hp, *(pv+1), val);
    *loc = *loc + 1;
}

void sts_43(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
    int32_t addr, val;
    stack_pop(st, &val);
    stack_pop(st, &addr);
    heap_store(hp, addr, val);
    *loc = *loc + 1;
}

void no_such(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
    printf("no such instr: at loc %08x\n", *loc);
}

struct instr_def instr_set[68] = {
    { .fn = &nop_00, .params_consumed = 0 },
    { .fn = &i32_01, .params_consumed = 0 },
    { .fn = &add_02, .params_consumed = 2 },
    { .fn = &dec_03, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &eq__10, .params_consumed = 2 },
    { .fn = &ez__11, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &jez_20, .params_consumed = 1 },
    { .fn = &jnz_21, .params_consumed = 1 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &no_such, .params_consumed = 0 },
    { .fn = &ldi_40, .params_consumed = 0 },
    { .fn = &lds_41, .params_consumed = 1 },
    { .fn = &sti_42, .params_consumed = 1 },
    { .fn = &sts_43, .params_consumed = 2 }
};