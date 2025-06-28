#include "event.h"

void event_print(struct event *event)
{
    if (event->id < EV_UNKNOWN) event_set[event->id].fn(event);
    else event_set[EV_UNKNOWN].fn(event);
}

void event_reset(void)
{
    event.id = EV_OK;
}

void event_ok(void)
{
    event_reset();
}

void event_print_ok(struct event *event) 
{
    printf(
        "EV_OK: ok\n"
        "  no further info\n\n"
    );
}

void event_hint(char * msg)
{
    event_reset();
    event.id = EV_HINT;
    event.pval.msg = msg;
}

void event_print_hint(struct event *event) 
{
    printf(
        "EV_HINT: hint\n"
        "  %s\n\n", 
        event->pval.msg
    );
}

void event_deprecate(iid_t iid, char * msg)
{
    event_reset();
    event.id = EV_DEPRECATE;
    event.pval.iid = iid;
    event.xval.msg = msg;
}

void event_print_deprecate(struct event *event) 
{
    printf(
        "EV_DEPRECATE: deprecated feature\n"
        "  instr 0x%x: %s\n\n", 
        event->pval.iid, event->xval.msg
    );
}

void event_fatal(char * msg)
{
    event_reset();
    event.id = EV_FATAL;
    event.pval.msg = msg;
}

void event_print_fatal(struct event *event) 
{
    printf(
        "EV_FATAL: fatal\n"
        "  %s\n\n", 
        event->pval.msg
    );
}

void event_stack_empty(char * msg)
{
    event_reset();
    event.id = EV_STACK_EMPTY;
    event.pval.msg = msg;
}

void event_print_stack_empty(struct event *event) 
{
    printf(
        "EV_STACK_EMPTY: stack underflow\n"
        "  %s\n\n", 
        event->pval.msg
    );
}

void event_stack_full(char * msg)
{
    event_reset();
    event.id = EV_STACK_FULL;
    event.pval.msg = msg;
}

void event_print_stack_full(struct event *event) 
{
    printf(
        "EV_STACK_FULL: stack overflow\n"
        "  %s\n\n", 
        event->pval.msg
    );
}

void event_heap_ooa(char * msg, addr_t addr)
{
    event_reset();
    event.id = EV_HEAP_OOA;
    event.pval.msg = msg;
    event.xval.addr = addr;
}

void event_print_heap_ooa(struct event *event) 
{
    printf(
        "EV_HEAP_OOA: heap access out-of-alignment\n"
        "  %s\naddress: 0x%08x\n\n", 
        event->pval.msg, event->xval.addr
    );
}

void event_heap_oob(char * msg, addr_t addr)
{
    event_reset();
    event.id = EV_HEAP_OOB;
    event.pval.msg = msg;
    event.xval.addr = addr;
}

void event_print_heap_oob(struct event *event) 
{
    printf(
        "EV_HEAP_OOB: heap access out-of-bounds\n"
        "  %s\naddress: 0x%08x\n\n", 
        event->pval.msg, event->xval.addr
    );
}

void event_instr_undef(iid_t iid, loc_t loc)
{
    event_reset();
    event.id = EV_INSTR_UNDEF;
    event.pval.iid = iid;
    event.xval.loc = loc;
}

void event_print_instr_undef(struct event *event) 
{
    printf(
        "EV_INSTR_UNDEF: undefined instruction\n"
        "  instr: 0x%02x\naddress: 0x%08x\n\n", 
        event->pval.iid, event->xval.loc
    );
}

void event_jump_oob(char * msg, loc_t loc)
{
    event_reset();
    event.id = EV_JUMP_OOB;
    event.pval.msg = msg;
    event.xval.loc = loc;
}

void event_print_jump_oob(struct event *event) 
{
    printf(
        "EV_JUMP_OOB: jump to out-of-bounds location\n"
        "  %s\nlocation: 0x%08x\n\n", 
        event->pval.msg, event->xval.loc
    );
}

void event_print_unknown(struct event *event) 
{
    printf(
        "EV_UNKNOWN: unknown event\n"
    );
}

struct event event = { .id = EV_OK };
struct event_def event_set[EVENT_SET_LEN] = {
    { .fn = event_print_ok },
    { .fn = event_print_hint },
    { .fn = event_print_deprecate },
    { .fn = event_print_fatal },
    { .fn = event_print_stack_empty },
    { .fn = event_print_stack_full },
    { .fn = event_print_heap_ooa },
    { .fn = event_print_heap_oob },
    { .fn = event_print_instr_undef },
    { .fn = event_print_jump_oob },
    { .fn = event_print_unknown }
};


