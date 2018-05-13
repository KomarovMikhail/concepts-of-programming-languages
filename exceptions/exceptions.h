#ifndef EXCEPTIONS_EXCEPTIONS_H
#define EXCEPTIONS_EXCEPTIONS_H

#include <setjmp.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

void** global_stack;
jmp_buf* env_stack;
size_t env_ptr;
size_t global_ptr; // указатель на вершину стека
size_t stack_size;
size_t nested_size;

// добавляем указатель на аллоцированную память в стек
void add_alloc(void* ptr);

// очищаем стек до последнего TRY
void clean_alloc();

void init_exceptions();
void free_exceptions();

#define TRY \
{\
    add_alloc(NULL);\
    jmp_buf local_env;\
    if (env_ptr + 1 == nested_size)\
    {\
        nested_size += 100;\
        env_stack = (jmp_buf*)realloc(env_stack, nested_size * sizeof(jmp_buf));\
    }\
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
}\
else\
{\
    THROW(OUT_OF_MEMORY);\
}

// exception types
#define BAD_FILE 1
#define OUT_OF_MEMORY 2
#define INVALID_ARGUMENT 3
#define RUNTIME_ERROR 4

#endif //EXCEPTIONS_EXCEPTIONS_H
