#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>

#define flush fflush(stdout)

/*
    gcc -m32 -static -o chall chall.c -fno-stack-protector
*/

int get_sum(int num, ...){
    printf("The sum of ");
    flush;
    int res = 0;
    int arg;

    va_list valist;
    va_start(valist, num);

    for(int i = 0; i < num; i++){
        arg = va_arg(valist, int);
        printf("%x ", arg);
        flush;
        if(i < num - 1){
            printf("+ ");
            flush;
        }
        res += arg;
    }

    va_end(valist);
    printf("= %d\n", res);
    flush;
}


int main(){
    char buffer[32];
    char flag[32];

    FILE *fptr = fopen("flag.txt", "r");
    fgets(flag, sizeof(buffer), fptr);

    int size = 3;
    printf("Hello it's me MARIOOOO! What's your name ? ");
    flush;
    fgets(buffer, 34, stdin);
    buffer[-1] = '\0';

    if(size > 20){
        printf("I trusted you... You are trying to kill my code :pensive:\n");
        flush;
        exit(-1);
    }

    printf("Hello %sHere is a sum for you: \n", buffer);
    flush;
    get_sum(size, 1, 2, 3);

    fclose(fptr);
    return 0;
}
