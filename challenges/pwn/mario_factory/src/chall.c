#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define NAME_LENGTH 32
#define flush fflush(stdout)


struct Mario
{
    int uid;
    char name[NAME_LENGTH];
} typedef Mario;

Mario* list_marios[5];
Mario* current_mario;
int nb_marios = 0;

void create_mario(){
    if(nb_marios >= 5){
        printf("You can not create more than 5 marios\n");
        flush;
        return;
    }

    char name[NAME_LENGTH];

    printf("Give him a name: ");
    flush;
    fgets(name, NAME_LENGTH, stdin);
    name[strcspn(name, "\n")] = 0;
    
    Mario* new_mario = malloc(sizeof(Mario));
    
    strcpy(new_mario->name, name);
    new_mario->uid = nb_marios;

    list_marios[nb_marios] = new_mario;
    current_mario = new_mario;
    nb_marios++;
}

void sign_in(){
    if(nb_marios == 0){
        printf("There is currently no mario created\n");
        flush;
        return;
    }

    char choice;
    int nl;

    printf("What id do you want: ");
    flush;

    choice = fgetc(stdin);
    nl = fgetc(stdin);

    if(nl != '\n') exit(0);
    
    
    current_mario = list_marios[choice - '0'];
}

void edit_mario(){
    char name[0x32];

    printf("What is your new name: ");
    flush;

    gets(name);
    
    for(int i = 0; i < 0x32; i++){
        current_mario->name[i] = name[i];
    }

}

void get_flag(){
    if(current_mario->uid == 1000){
        FILE *f = fopen("flag.txt", "r");
        if (f == NULL) {
            printf("Error while opening flag file\n");
            flush;
            exit(1);
        }
        char flag[100];
        if (fgets(flag, 100, f) != NULL) {
            printf("Your flag is : %s\n", flag);
            flush;
        }
        fclose(f);
    }
    else{
        printf("We give the flag only to the big mario\n");
        flush;
    }
}

void display_marios(){
    printf("UID : NAME\n\n");
    flush;
    for(int i = 0; i < nb_marios; i++){
        printf("%d : %s\n", list_marios[i]->uid, list_marios[i]->name);
        flush;
    }
}

int main(){    
    printf("TOTODOTODOTOTOOOOO! Here we goooo to create marioooooooos!!!\n");
    flush;

    while(1){
        printf("\nPlease make a choice:\n");
        flush;
        printf("1: Create a mario\n");
        flush;
        printf("2: Sign in to a mario\n");
        flush;
        printf("3: Edit current mario\n");
        flush;
        printf("4: Display marios\n");
        flush;
        printf("5: Get a flag\n");
        flush;
        printf("6: Exit\n");
        flush;
        if(current_mario != NULL){
            printf("You are currently %d's mario called: %s\n", current_mario->uid, current_mario->name);
            flush;
        }
        printf(">> ");
        flush;

        char choice;
        int nl;

        choice = fgetc(stdin);
        nl = fgetc(stdin);

        if(nl != '\n') exit(0);

        switch (choice)
        {
        case '1':
            create_mario();
            break;

        case '2':
            sign_in();
            break;

        case '3':
            edit_mario();
            break;
        
        case '4':
            display_marios();
            break;

        case '5':
            get_flag();
            break;
        
        case '6':
            printf("Bye bye, see you o/\n");
            flush;
            exit(0);
            break;
        
        default:
            break;
        }
    }

    return 0;
}
