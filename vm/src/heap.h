#ifndef _HEAP_H_
#define _HEAP_H_

#include "def.h"
#include "event.h"

#define HEAP_OK 0
#define HEAP_OOB 1
#define HEAP_OOA 2

union heap_mem
{
    word_t *m4;
    byte_t *m1;
};

struct heap
{
	addr_t addr_end;
	union heap_mem mem;
};

void heap_init(struct heap *heap, byte_t *heap_mem);
int heap_load1(struct heap *heap, addr_t addr, byte_t *val);
int heap_store1(struct heap *heap, addr_t addr, byte_t val);
int heap_load4(struct heap *heap, addr_t addr, word_t *val);
int heap_store4(struct heap *heap, addr_t addr, word_t val);

#endif//_HEAP_H_