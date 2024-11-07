#include "ist0_set.h"
#include "instr.h"

INSTR_FN(nop) {}

INSTR_FN(i32)
{
	PRODUCE(*pv);
	NEXT_LOC();
}

INSTR_FN(add)
{
	int32_t a, b;
	CONSUME(&a);
	CONSUME(&b);
	PRODUCE(a + b);
	NEXT_LOC();
}

INSTR_FN(dec)
{
	int32_t a;
	CONSUME(&a);
	PRODUCE(a - 1);
	NEXT_LOC();
}

INSTR_FN(eq_)
{
	int32_t a, b;
	CONSUME(&a);
	CONSUME(&b);
	PRODUCE(a == b);
	NEXT_LOC();
}

INSTR_FN(ez_)
{
	int32_t a;
	CONSUME(&a);
	PRODUCE(a);
	PRODUCE(a == 0);
	NEXT_LOC();
}

INSTR_FN(jez)
{
	int32_t a;
	CONSUME(&a);
	if (a == 0) SET_LOC(*pv);
	else NEXT_LOC();
}

INSTR_FN(jnz)
{
	int32_t a;
	CONSUME(&a);
	if (a != 0) SET_LOC(*pv);
	else NEXT_LOC();
}

struct instr_def ist0_set[MAX_SET] =
{
	INSTR_ENTRY(0x00, nop, 0),
	INSTR_ENTRY(0x01, i32, 1),
	INSTR_ENTRY(0x02, add, 0),
	INSTR_ENTRY(0x03, dec, 0),
	INSTR_ENTRY(0x10, eq_, 0),
	INSTR_ENTRY(0x11, ez_, 0),
	INSTR_ENTRY(0x20, jez, 1),
	INSTR_ENTRY(0x21, jnz, 1),
};

