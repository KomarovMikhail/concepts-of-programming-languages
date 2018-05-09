#include "exceptions.h"

void add_alloc(void* ptr)
{
    if (global_ptr + 1 == stack_size)
    {
        stack_size += 100;
        global_stack = realloc(global_stack, stack_size * sizeof(void*));
        if (global_stack == NULL)
        {
            THROW(OUT_OF_MEMORY);
        }
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

void init_exceptions()
{
    env_ptr = 0;
    global_ptr = 0;
    stack_size = 100;
    nested_size = 100;
    global_stack = malloc(stack_size * sizeof(void*));
    env_stack = (jmp_buf*)malloc(nested_size * sizeof(jmp_buf));
}

void free_exceptions()
{
    free(global_stack);
    free(env_stack);
}
