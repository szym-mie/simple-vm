#ifndef _HEAP_H_
#define _HEAP_H_

#include <stdint.h>

#define HEAP_OK
#define HEAP_OOB

struct heap
{
	uint32_t max_elem_count;
	int32_t *heap;
};

void heap_init(struct heap *heap, int32_t *heap_mem);
int heap_load(struct heap *heap, int32_t addr, int32_t *val);
int heap_store(struct heap *heap, int32_t addr, int32_t val);

#endif//_HEAP_H_