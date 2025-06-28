#ifndef _INSTR_H_
#define _INSTR_H_

#include "def.h"
#include "stack.h"
#include "heap.h"

#define INSTR_PARAMS  \
    loc_t *loc,       \
    struct stack *st, \
    struct heap *hp,  \
    const word_t *pv
#define INSTR_FN(QN) void QN(INSTR_PARAMS)
#define INSTR_ENTRY(ID, FN, PC) [ID] = { .fn = FN, .params_consumed = PC }

struct instr_def
{
	void (*fn)(INSTR_PARAMS);
	plen_t params_consumed;
};

struct instr
{
	iid_t id;
	word_t *params;
};

#define CONSUME(PTR) stack_pop(st, PTR)
#define PRODUCE(VAL) stack_push(st, VAL)
#define NEXT_LOC() (*loc)++
#define SET_LOC(LOC) *loc = LOC

#endif//_INSTR_H_

