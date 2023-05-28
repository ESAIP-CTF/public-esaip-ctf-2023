#include <stdio.h>

struct position
{
    int x;
    int y;
};


int main(int charc, char* argv)
{
    char maze[3][17] = {" X   XXXXX   XXX\0",
                        " X X     X X  XX\0",
                        "   XXXXX   XX   \0"};

    struct position pos;
    pos.x = 0;
    pos.y = 0;

    char user_input[26] = {0};
    char* ret = fgets(user_input, 26, stdin);

    if(ret != NULL)
    {
        for(int i = 0; i < 25; i++)
        {
            char chr = user_input[i];

            if(chr == 'U')
            {
                if(pos.y == 0) { return 0; }
                if(maze[pos.y - 1][pos.x] == 'X') { return 0; }
                maze[pos.y][pos.x] = 'X';
                pos.y-= 1;
            }
            if(chr == 'D')
            {
                if(pos.y == 2) { return 0; }
                if(maze[pos.y + 1][pos.x] == 'X') { return 0; }
                maze[pos.y][pos.x] = 'X';
                pos.y+= 1;
            }
            if(chr == 'L')
            {
                if(pos.x == 0) { return 0; }
                if(maze[pos.y][pos.x - 1] == 'X') { return 0; }
                maze[pos.y][pos.x] = 'X';
                pos.x-= 1;
            }
            if(chr == 'R')
            {
                if(pos.x == 16) { return 0; }
                if(maze[pos.y][pos.x + 1] == 'X') { return 0; }
                maze[pos.y][pos.x] = 'X';
                pos.x+= 1;
            }

            if(pos.x == 15 && pos.y == 2) {
                printf("ECTF{%s}\n", user_input);
            }
        }
    }

    return 0;
}

// DDRRUURRDRRRRDRRUURRDRDRR
