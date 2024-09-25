#include "program.h"

int program_load
(
		struct program *program, 
		struct instr_def instr_defs[MAX_SET], 
		const char *filename
) 
{
	FILE *f = fopen(filename, "rb");
	char *sig;

	fread(&sig, 1, 4, f);
	if (!program_verify_sig(sig)) return 0;
	
	uint32_t instr_count;
	uint32_t param_count;
	fread(&instr_count, sizeof(uint32_t), 1, f);
	fread(&param_count, sizeof(uint32_t), 1, f);
	
	uint8_t unused;

	// ignore rest of the metadata (version + val size + padding)
	fread(&unused, sizeof(uint8_t), 1, f);
	fread(&unused, sizeof(uint8_t), 1, f);
	fread(&unused, sizeof(uint8_t), 1, f);
	fread(&unused, sizeof(uint8_t), 1, f);

	struct instr *instrs = malloc(sizeof(struct instr) * instr_count);
	if (instrs == NULL) return 0;

	int32_t *params = malloc(sizeof(int32_t) * param_count);
	if (params == NULL)
	{
		free(instrs);
		return 0;
	}

	uint8_t id;
	uint32_t tpi = 0;

	for (uint32_t i = 0; i < instr_count; i++)
	{
		fread(&id, sizeof(uint8_t), 1, f);
		uint8_t param_count = instr_defs[id].params_consumed;
		
		struct instr *instr = instrs + i;
		int32_t *instr_params = params + tpi;
		
		fread(instr_params, sizeof(int32_t), param_count, f);
		tpi += param_count;

		instr->id = id;
		instr->params = instr_params;
	}
	
	// TODO read start loc from binary file later
	program->start_loc = 0;
	program->instr_count = instr_count;
	program->instrs = instrs;
	program->params = params;

	return 1;
}

int program_run
(
		struct program *program,
		struct instr_def instr_defs[MAX_SET], 
		struct stack *stack
)
{
	uint32_t loc = program->start_loc;
	struct instr *instr;

	for (; loc < program->instr_count; loc++)
	{
		instr = program->instrs + loc;
		// TODO currently does not support location changes
		// TODO return from instruction fn to serve exceptions
		instr_defs[instr->id].fn(stack, instr->params);
	}

	return 1;
}

int program_verify_sig(char *sig)
{
	// FIXME let's just say it passes for now
	return 1;
}
