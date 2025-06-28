#include "program.h"

#define VERBOSE 1

int program_load
(
        struct program *program, 
        struct instr_def instr_defs[PROGRAM_MAX_SET], 
        const char *filename
) 
{
    FILE *f = fopen(filename, "rb");
    if (f == NULL) 
    {
        printf("cannot open file.\n");
        return 0;
    }
    if (!program_verify_sig(f)) 
    {
        printf("bad program signature.\n");
        return 0;
    }
    
    byte_t unused;
    loc_t instr_count;
    llen_t param_count;
    slen_t mattrs_count;
    // total instruction count
    fread(&instr_count, sizeof(loc_t), 1, f);
    // total parameters count
    fread(&param_count, sizeof(llen_t), 1, f);
    // ignore rest of the metadata (version + val size)
    fread(&unused, sizeof(byte_t), 1, f);
    fread(&unused, sizeof(byte_t), 1, f);
    fread(&mattrs_count, sizeof(slen_t), 1, f);

    struct instr *instrs = malloc(sizeof(struct instr) * instr_count);
    if (instrs == NULL) return 0;

    word_t *params = malloc(sizeof(word_t) * param_count);
    if (params == NULL)
    {
        free(instrs);
        return 0;
    }

    struct meta_attr *mattrs = malloc(sizeof(struct meta_attr) * mattrs_count);
    if (mattrs == NULL)
    {
        free(instrs);
        free(params);
        return 0;
    }

    for (slen_t mai = 0; mai < mattrs_count; mai++)
    {
        if (!meta_attr_parse(f, mattrs+mai)) return 0;
    }

    // padding
    fread(&unused, sizeof(byte_t), 1, f);

    iid_t id;
    
    for (llen_t ii = 0, pi = 0; ii < instr_count; ii++)
    {
        fread(&id, sizeof(iid_t), 1, f);
        if (VERBOSE) printf("read instr %u\n", id);
        uint8_t param_count = instr_defs[id].params_consumed;
        if (VERBOSE) printf("read %u params\n", param_count);

        struct instr *instr = instrs+ii;
        word_t *instr_params = params+pi;
        
        fread(instr_params, sizeof(word_t), param_count, f);
        pi += param_count;

        instr->id = id;
        instr->params = instr_params;
    }

    fclose(f);
    
    // TODO read start loc from binary file later
    program->start_loc = 0;
    program->meta_attr_count = mattrs_count;
    program->meta_attrs = mattrs;
    program->instr_count = instr_count;
    program->instrs = instrs;
    program->params = params;

    return 1;
}

int program_run
(
        struct program *program,
        struct instr_def instr_defs[PROGRAM_MAX_SET], 
        struct stack *stack,
        struct heap *heap
)
{
    loc_t loc = program->start_loc;
    struct instr *instr;

    while (loc < program->instr_count)
    {
        event_reset();
        instr = program->instrs + loc;
        instr_defs[instr->id].fn(&loc, stack, heap, instr->params);
        if (event.id == 0) continue;
        
        event_print(&event);
        if (EVENT_IS_FATAL(event)) break; 
    }

    return 1;
}

int program_verify_sig(FILE *f)
{
    // FIXME let's just say it passes for now
    char sig[4];
    fread(&sig, 1, 4, f);
    return 'S' == sig[0] && 'V' == sig[1] && 'M' == sig[2] && '0' == sig[3];
}
