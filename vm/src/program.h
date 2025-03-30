#ifndef _PROGRAM_H_
#define _PROGRAM_H_

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include "meta_attr.h"
#include "instr.h"

#define MAX_SET 256
typedef uint8_t iid_t;
typedef uint16_t slen_t;
typedef uint32_t llen_t;
typedef uint32_t loc_t;
typedef int32_t word_t;

struct program
{
	loc_t start_loc;
	slen_t meta_attr_count;
	struct meta_attr *meta_attrs;
	loc_t instr_count;
	struct instr *instrs;
	word_t *params;
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
		struct stack *stack,
		struct heap *heap
);
int program_verify_sig(char *sig);

#endif//_PROGRAM_H_
