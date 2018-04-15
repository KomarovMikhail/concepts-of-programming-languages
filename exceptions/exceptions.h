#ifndef EXCEPTIONS_EXCEPTIONS_H
#define EXCEPTIONS_EXCEPTIONS_H

#include <setjmp.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define STACK_SIZE 100

static jmp_buf global_env;
void* global_stack[STACK_SIZE];
size_t global_ptr = 0; // указатель на вершину стека

// добавляем указатель на аллоцированную память в стек
void add_alloc(void* ptr)
{
    if (global_ptr + 1 == STACK_SIZE)
    {
        printf("Memory exhausted\n");
        exit(1);
    }
    global_stack[global_ptr++] = ptr;
}

// очищаем стек до последнего TRY
void clean_alloc()
{
    while (global_stack[--global_ptr] != NULL)
    {
        free(global_stack[global_ptr]);
    }
}

#define TRY \
do {\
    add_alloc(NULL);\
    jmp_buf local_env;\
    memcpy(global_env, local_env, sizeof(jmp_buf));\
    switch( setjmp(global_env) )\
    {\
        case 0:

#define CATCH(exception_type) \
            break;\
        case exception_type:

#define END_TRY \
    }\
} while(0)

#define THROW(exception_type) \
clean_alloc();\
longjmp(global_env, exception_type)


#define SAFE_MALLOC(ptr, size) \
ptr = malloc( size ); \
add_alloc( ptr )

// exception types
#define BAD_FILE 1
#define OUT_OF_MEMORY 2
#define INVALID_ARGUMENT 3

#endif //EXCEPTIONS_EXCEPTIONS_H
