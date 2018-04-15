#include <stdio.h>
#include "exceptions.h"

void read_file()
{
    void * buf;
    SAFE_MALLOC(buf, 11 * sizeof(char))
    if (buf == NULL)
    {
        printf("Cannot allocate memory\n");
    }

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
    printf("Global stack pointer: %ld\n", global_ptr);
    TRY
    {
        void * buf;
        SAFE_MALLOC(buf, 10 * sizeof(int))
        if (buf == NULL)
        {
            printf("Cannot allocate memory\n");
        }

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
    END_TRY;
    printf("Global stack pointer: %ld\n", global_ptr);

    return 0;
}