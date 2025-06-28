#ifndef _PROGRAM_H_
#define _PROGRAM_H_

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include "meta_attr.h"
#include "instr.h"
#include "event.h"

#define PROGRAM_MAX_SET 256

struct program
{
	loc_t start_loc;
	slen_t meta_attr_count;
	struct meta_attr *meta_attrs;
	llen_t instr_count;
	struct instr *instrs;
	word_t *params;
};

int program_load
(
		struct program *program, 
		struct instr_def instr_defs[PROGRAM_MAX_SET], 
		const char *filename
);
int program_run
(
		struct program *program,
		struct instr_def instr_defs[PROGRAM_MAX_SET], 
		struct stack *stack,
		struct heap *heap
);
int program_verify_sig(FILE *f);

#endif//_PROGRAM_H_
