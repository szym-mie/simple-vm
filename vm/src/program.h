#ifndef _PROGRAM_H_
#define _PROGRAM_H_

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include "instr.h"

#define MAX_SET 256

struct program
{
	uint32_t start_loc;
	uint32_t instr_count;
	struct instr *instrs;
	int32_t *params;
};

// suggestion: link instruction defs to program with new struct

int program_load
(
		struct program *program, 
		struct instr_def instr_defs[MAX_SET], 
		const char *filename
);
int program_run
(
		struct program *program,
		struct instr_def instr_defs[MAX_SET], 
		struct stack *stack
);
int program_verify_sig(char *sig);

#endif//_PROGRAM_H_
