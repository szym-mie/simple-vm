#include "heap.h"

#define HEAP_AT1(H, A) ((H).mem.m1+(A>>0))
#define HEAP_AT4(H, A) ((H).mem.m4+(A>>2))

#define HEAP_TST_AL4(A) ((A&0x3)==0)

void heap_init(struct heap *heap, byte_t *heap_mem)
{
    heap->mem.m1 = heap_mem;
}

int heap_load1(struct heap *heap, addr_t addr, byte_t *val)
{
    if (addr >= heap->addr_end)
    {
        event_heap_oob("heap_load1", addr);
        return HEAP_OOB;
    }
    *val = *HEAP_AT1(*heap, addr);
    return HEAP_OK;
}

int heap_store1(struct heap *heap, addr_t addr, byte_t val)
{
    if (addr >= heap->addr_end)
    {
        event_heap_oob("heap_store1", addr);
        return HEAP_OOB;
    }
    *HEAP_AT1(*heap, addr) = val;
    return HEAP_OK;
}

int heap_load4(struct heap *heap, addr_t addr, word_t *val)
{
    if (!HEAP_TST_AL4(addr))
    {
        event_heap_ooa("heap_load4", addr);
        return HEAP_OOA;
    }
    if (addr >= heap->addr_end)
    {
        event_heap_oob("heap_load4", addr);
        return HEAP_OOB;
    }
    *val = *HEAP_AT4(*heap, addr);
    return HEAP_OK;
}

int heap_store4(struct heap *heap, addr_t addr, word_t val)
{
    if (!HEAP_TST_AL4(addr))
    {
        event_heap_ooa("heap_store4", addr);
        return HEAP_OOA;
    }
    if (addr >= heap->addr_end)
    {
        event_heap_oob("heap_store4", addr);
        return HEAP_OOB;
    }
    *HEAP_AT4(*heap, addr) = val;
    return HEAP_OK;
}