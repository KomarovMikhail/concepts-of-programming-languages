#include <stdio.h>
#include "exceptions.h"

void read_file()
{
    void * buf;
    SAFE_MALLOC(buf, 11 * sizeof(char))

    printf("Global stack pointer: %ld\n", global_ptr);

    int input;
    scanf("%d", &input);
    if (input == 0)
    {
        THROW(INVALID_ARGUMENT);
    }
    FILE * file = fopen("test", "-rw");
    if (file == NULL)
    {
        THROW(BAD_FILE);
    }
    fclose(file);
}

int main() {
    init_exceptions();
    printf("Global stack pointer: %ld\n", global_ptr);
    TRY
    {
        void * buf;
        SAFE_MALLOC(buf, 10 * sizeof(int))
        read_file();
    }
    CATCH(INVALID_ARGUMENT)
    {
        printf("Zero input\n");
    }
    CATCH(BAD_FILE)
    {
        printf("Caught BAD_FILE exception\n");
    }
    CATCH(OUT_OF_MEMORY)
    {
        printf("Caught OUT_OF_MEMORY exception\n");
    }
    END_TRY;
    printf("Global stack pointer: %ld\n", global_ptr);

    free_exceptions();
    return 0;
}