#ifndef EXCEPTIONS_EXCEPTIONS_H
#define EXCEPTIONS_EXCEPTIONS_H

#include <setjmp.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define STACK_SIZE 100
#define MAX_NESTED 100000

void* global_stack[STACK_SIZE];
jmp_buf env_stack[MAX_NESTED];
size_t env_ptr = 0;
size_t global_ptr = 0; // указатель на вершину стека

// добавляем указатель на аллоцированную память в стек
void add_alloc(void* ptr);

// очищаем стек до последнего TRY
void clean_alloc();

#define TRY \
{\
    add_alloc(NULL);\
    jmp_buf local_env;\
    memcpy(env_stack[env_ptr++], local_env, sizeof(jmp_buf));\
    switch( setjmp(env_stack[env_ptr-1]) )\
    {\
        case 0:

#define CATCH(exception_type) \
            break;\
        case exception_type:

#define END_TRY \
    }\
}

#define THROW(exception_type) \
clean_alloc();\
longjmp(env_stack[--env_ptr], exception_type)


#define SAFE_MALLOC(ptr, size) \
ptr = malloc( size ); \
if (ptr != NULL)\
{\
    add_alloc( ptr );\
}

// exception types
#define BAD_FILE 1
#define OUT_OF_MEMORY 2
#define INVALID_ARGUMENT 3
#define RUNTIME_ERROR 4

#endif //EXCEPTIONS_EXCEPTIONS_H
