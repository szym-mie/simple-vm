#include "heap.h"

void heap_init(struct heap *heap, int32_t *heap_mem)
{
    heap->heap = heap_mem;
}

int heap_load(struct heap *heap, int32_t addr, int32_t *val)
{
    if (addr >= 0 && addr < heap->max_elem_count)
    {
        *val = *(heap->heap+addr);
        return HEAP_OK;
    }
    return HEAP_OOB;
}
int heap_store(struct heap *heap, int32_t addr, int32_t val)
{
    if (addr >= 0 && addr < heap->max_elem_count)
    {
        *(heap->heap+addr) = val;
        return HEAP_OK;
    }
    return HEAP_OOB;
}