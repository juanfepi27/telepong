#include "myPongProtocol.h"

int main(int argc, char *argv[]){

    // check if the len of argv if equal to 2
    if (argc != 3) {
        printf("Use the format $./server <PORT> <Log File>\n");
        exit(1);
    }

    int lengFileName = strlen(argv[2]);

    if(lengFileName >= 4 && strcmp(argv[2] + lengFileName - 4, ".txt") != 0){
        printf("The log file must have the extension .txt\n");
        exit(1);
    }
    
    setUpServer(argv[1], argv[2]);
}