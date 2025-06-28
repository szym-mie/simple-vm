#ifndef _EVENT_H_
#define _EVENT_H_

#include <stdio.h>

#include "def.h"

#define EVENT_IS_FATAL(EV) ((EV).id >= EV_FATAL)

enum event_id
{
    // soft
    EV_OK=0, // everything ok
    EV_HINT, // hint at bad usage/pitfall
    EV_DEPRECATE, // smth is deprecated
    // fatal
    EV_FATAL, // any fatal event
    EV_STACK_EMPTY, // stack is empty, cannot pop
    EV_STACK_FULL, // stack is full, cannot push
    EV_HEAP_OOA, // heap access out-of-aligment
    EV_HEAP_OOB, // heap acesss out-of-bounds
    EV_INSTR_UNDEF, // undefined instruction
    EV_JUMP_OOB, // jump out of bounds
    // unknown event
    EV_UNKNOWN // fallback
};

#define EVENT_SET_LEN (EV_UNKNOWN + 1)

union event_val
{
    char *msg;
    iid_t iid;
    word_t word;
    byte_t byte;
    loc_t loc;
    addr_t addr;
};

struct event
{
    enum event_id id;
    union event_val pval;
    union event_val xval;
};

struct event_def
{
    void (*fn)(struct event *event);
};

void event_print(struct event *event);
void event_reset(void);

void event_ok(void);
void event_hint(char * msg);
void event_deprecate(iid_t iid, char * msg);
void event_fatal(char * msg);
void event_stack_empty(char * msg);
void event_stack_full(char * msg);
void event_heap_ooa(char * msg, addr_t addr);
void event_heap_oob(char * msg, addr_t addr);
void event_instr_undef(iid_t iid, loc_t loc);
void event_jump_oob(char * msg, loc_t loc);

extern struct event event;
extern struct event_def event_set[EVENT_SET_LEN];

#endif//_EVENT_H_