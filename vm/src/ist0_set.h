#ifndef _SET0_H_
#define _SET0_H_

#include <stdint.h>

#include "instr.h"
#include "program.h"

INSTR_FN_DEF(nop);
INSTR_FN_DEF(i32);
INSTR_FN_DEF(add);
INSTR_FN_DEF(eq_);

extern struct instr_def ist0_set[MAX_SET];

#endif//_SET0_H_

