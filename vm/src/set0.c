#include "set0.h"
#include "instr.h"

INSTR_FN_DEF(nop) {}

INSTR_FN_DEF(i32)
{
	PRODUCE(*pv);
}

INSTR_FN_DEF(add)
{
	int32_t a, b;
	CONSUME(&a);
	CONSUME(&b);
	PRODUCE(a + b);
}

INSTR_FN_DEF(eq_)
{
	int32_t a, b;
	CONSUME(&a);
	CONSUME(&b);
	PRODUCE(a == b);
}


struct instr_def ist0_set[MAX_SET] =
{
	INSTR_DEF_ENTRY(0x00, nop, 0),
	INSTR_DEF_ENTRY(0x01, i32, 1),
	INSTR_DEF_ENTRY(0x02, add, 0),
	INSTR_DEF_ENTRY(0x10, eq_, 0)
};

