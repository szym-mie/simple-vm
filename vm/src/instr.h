#ifndef _INSTR_H_
#define _INSTR_H_

#include <stdint.h>

#include "stack.h"

#define INSTR_PARAMS struct stack *s, const int32_t *pv
#define INSTR_FN_DEF(QN) void QN(INSTR_PARAMS)
#define INSTR_DEF_ENTRY(ID, FN, PC) [ID] = { .fn = FN, .params_consumed = PC }

struct instr_def
{
	void (*fn)(INSTR_PARAMS);
	uint8_t params_consumed;
};

struct instr
{
	uint8_t id;
	int32_t *params;
};

#define CONSUME(PTR) stack_pop(s, PTR);
#define PRODUCE(VAL) stack_push(s, VAL);

#endif//_INSTR_H_

