#include "instruction_set_0.h"

void nop_00(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
}

void put_01(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
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

void ldi4_40(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
    int32_t val;
    heap_load4(hp, *pv, &val);
    stack_push(st, val);
    *loc = *loc + 1;
}

void lds4_41(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
    int32_t addr, val;
    stack_pop(st, &addr);
    heap_load4(hp, addr, &val);
    stack_push(st, val);
    *loc = *loc + 1;
}

void sti4_42(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
    int32_t val;
    stack_pop(st, &val);
    heap_store4(hp, *pv, val);
    *loc = *loc + 1;
}

void sts4_43(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
    int32_t addr, val;
    stack_pop(st, &val);
    stack_pop(st, &addr);
    heap_store4(hp, addr, val);
    *loc = *loc + 1;
}

void ldi1_44(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
    int32_t val = 0;
    heap_load1(hp, *pv, (int8_t *) &val);
    stack_push(st, val);
    *loc = *loc + 1;
}

void lds1_45(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
    int32_t addr, val = 0;
    stack_pop(st, &addr);
    heap_load1(hp, addr, (int8_t *) &val);
    stack_push(st, val);
    *loc = *loc + 1;
}

void sti1_46(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
    int32_t val;
    stack_pop(st, &val);
    heap_store1(hp, *pv, (int8_t) val);
    *loc = *loc + 1;
}

void sts1_47(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
    int32_t addr, val;
    stack_pop(st, &val);
    stack_pop(st, &addr);
    heap_store1(hp, addr, (int8_t) val);
    *loc = *loc + 1;
}

void no_such(loc_t *loc, struct stack *st, struct heap *hp, const word_t *pv)
{
    printf("no such instr: at loc %08x\n", *loc);
    event_instr_undef(0x00, *loc); //TODO
}

struct instr_def instr_set[72] = {
    { .fn = &nop_00, .params_consumed = 0 },
    { .fn = &put_01, .params_consumed = 1 },
    { .fn = &add_02, .params_consumed = 0 },
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
    { .fn = &eq__10, .params_consumed = 0 },
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
    { .fn = &ldi4_40, .params_consumed = 1 },
    { .fn = &lds4_41, .params_consumed = 0 },
    { .fn = &sti4_42, .params_consumed = 1 },
    { .fn = &sts4_43, .params_consumed = 0 },
    { .fn = &ldi1_44, .params_consumed = 1 },
    { .fn = &lds1_45, .params_consumed = 0 },
    { .fn = &sti1_46, .params_consumed = 1 },
    { .fn = &sts1_47, .params_consumed = 0 }
};