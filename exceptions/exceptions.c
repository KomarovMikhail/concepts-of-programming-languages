#include "exceptions.h"

void add_alloc(void* ptr)
{
    if (global_ptr + 1 == STACK_SIZE)
    {
//        printf("Memory exhausted\n");
//        exit(1);
        THROW(OUT_OF_MEMORY);
    }
    global_stack[global_ptr++] = ptr;
}

void clean_alloc()
{
    while (global_stack[--global_ptr] != NULL)
    {
        free(global_stack[global_ptr]);
    }
}
