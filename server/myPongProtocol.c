#include "myPongProtocol.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h> // read(), write(), close()
#include <pthread.h>
#include <fcntl.h>
#include <errno.h>

struct room{
    bool open;
    int clientsConnected;
    char* nicknamePlayer1;
    char* nicknamePlayer2;
    int connfd1;
    int connfd2;
    int scorePlayer1;
    int scorePlayer2;
    pthread_mutex_t mutex;
};

struct threadArgs{
    int connfd;
    char *logFile;
};

struct room rooms[MAX_ROOMS];

int setUpServer(char* port, char* logFile){
    int sockfd, connfd, len;
    struct sockaddr_in servaddr, cli;
    struct threadArgs args;
    char* messageLog;

    // socket create and verification
    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    if (sockfd == -1) {
        messageLog = "Socket creation failed...";
        writeLog(logFile, messageLog);
        printf("socket creation failed...\n");
        exit(0);
    }
    else
        messageLog = "Socket successfully created with AF_INET and SOCK_STREAM";
        writeLog(logFile, messageLog);
        printf("Socket successfully created..\n");
    bzero(&servaddr, sizeof(servaddr));

    // assign IP, PORT
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(PORT);

    // Binding newly created socket to given IP and verification
    if ((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0) {
        messageLog = "Socket bind failed";
        writeLog(logFile, messageLog);
        printf("socket bind failed...\n");
        exit(0);
    }
    else
        messageLog = "Socket successfully binded";
        writeLog(logFile, messageLog);
        printf("Socket successfully binded..\n");

    int flags = fcntl(sockfd, F_GETFL, 0);

    if (flags == -1) {
        messageLog = "Error while getting the server socket flags";
        writeLog(logFile, messageLog);
        perror("Error while getting the server socket flags");
        exit(1);
    }

    if (fcntl(sockfd, F_SETFL, O_NONBLOCK) == -1) {
        messageLog = "Error while setting the server socket to non-blocking";
        writeLog(logFile, messageLog);
        perror("Error while setting the server socket to non-blocking");
        exit(1);
    }
    
    // Now server is ready to listen and verification
    if ((listen(sockfd, 10)) != 0) {
        messageLog = "Error while listen, verify connections";
        writeLog(logFile, messageLog);
        printf("Listen failed...\n");
        exit(0);
    }
    else{
        messageLog = "Server successfully listening";
        writeLog(logFile, messageLog);
        printf("Server listening..\n");
    }

    //initialize rooms
    for (int i=0; i < MAX_ROOMS; i++){
        rooms[i].open = 1;
        rooms[i].clientsConnected = 0;
        rooms[i].nicknamePlayer1 = "";
        rooms[i].nicknamePlayer2 = "";
        rooms[i].scorePlayer1 = 0;
        rooms[i].scorePlayer2 = 0;
        rooms[i].connfd1 = -1;
        rooms[i].connfd2 = -1;
        pthread_mutex_init(&rooms[i].mutex, NULL);
    }

    len = sizeof(cli);

    while(1){
        connfd = accept(sockfd, (SA*)&cli, &len);
        if (connfd < 0) {
            if (errno == EWOULDBLOCK || errno == EAGAIN) {
                // No incoming connections, continue waiting.
                usleep(100000);  // Sleep for a short time to avoid busy-waiting
                continue;
            } else {
                messageLog = "Server accept failed";
                writeLog(logFile, messageLog);
                printf("server accept failed...\n");
                exit(0);
            }
        }
        else
            messageLog = "Server accept a client";
            writeLog(logFile, messageLog);
            printf("server accept the client...\n");

            int client_flags = fcntl(connfd, F_GETFL, 0);
            if (client_flags == -1) {
                messageLog = "Error while getting the client socket flags";
                writeLog(logFile, messageLog);
                perror("Error while getting the client socket flags");
                exit(1);
            }

            if (fcntl(connfd, F_SETFL, client_flags | O_NONBLOCK) == -1) {
                messageLog = "Error while setting the client socket to non-blocking";
                writeLog(logFile, messageLog);
                perror("Error while setting the client socket to non-blocking");
                exit(1);
            }

            pthread_t client_thread;
            int* connfd_ptr = malloc(sizeof(int));
            *connfd_ptr = connfd;
            args.connfd = connfd;
            args.logFile = logFile;
            pthread_create(&client_thread, NULL, handleClient, &args);
    }
    return connfd;
}

void* handleClient(void* arg){
    int connfd = ((struct threadArgs*)arg)->connfd;
    char* logFile = ((struct threadArgs*)arg)->logFile;
    bool isConnected = true;
    int numberOfPlayer;
    int flagRoom = -1;
    char* messageLog;

    //check for available rooms
    //one player waiting for couple
    for(int i=0; i < MAX_ROOMS; i++){
        if(flagRoom != -1){
            break;
        }
        if(rooms[i].open && rooms[i].clientsConnected == 1){
            flagRoom = i;
        }
    }
    //alone rooms
    for(int i=0; i < MAX_ROOMS; i++){
        if(flagRoom != -1){
            break;
        }
        if(rooms[i].open && rooms[i].clientsConnected == 0){
            flagRoom = i;
        }
    }

    //lets start the game or leave the game if it is full
    if(flagRoom >= 0){
        pthread_mutex_lock(&rooms[flagRoom].mutex);
        rooms[flagRoom].clientsConnected++; // 1 or 2
        numberOfPlayer = rooms[flagRoom].clientsConnected; // 1 or 2
        if(rooms[flagRoom].clientsConnected == 2){
            rooms[flagRoom].open = false;
        }
        messageLog = "We found an available room";
        writeLogRoom(flagRoom,numberOfPlayer,logFile,messageLog);
        pthread_mutex_unlock(&rooms[flagRoom].mutex);

        // El cliente ya debió haber mandado el request PLAYER NEW
        receiveRequest(connfd,flagRoom,numberOfPlayer,logFile);

        // Esperar a que el otro jugador se conecte
        while(true){
            receiveRequest(connfd,flagRoom,numberOfPlayer,logFile);
            if(rooms[flagRoom].clientsConnected == 2 && strcmp(rooms[flagRoom].nicknamePlayer1,"")!=0 && strcmp(rooms[flagRoom].nicknamePlayer2,"")!=0){
                char* message = "GAME START";
                char* nickname1 = rooms[flagRoom].nicknamePlayer1;
                char* nickname2 = rooms[flagRoom].nicknamePlayer2;

                messageLog = "Starts a game";
                writeLogRoom(flagRoom,numberOfPlayer,logFile,messageLog);

                int totalLength = snprintf(NULL, 0, "%s %s %s", message, nickname1, nickname2);
                char* response = (char*)malloc(totalLength + 1);  // +1 para el carácter nulo
                snprintf(response, totalLength + 1, "%s %s %s", message, nickname1, nickname2);
                sendResponse(flagRoom, numberOfPlayer, connfd, response, logFile);

                break;
            }
        }

        while(isConnected){
            receiveRequest(connfd,flagRoom,numberOfPlayer,logFile);
        }
    }else{
        messageLog = "There are not available rooms yet";
        writeLog(logFile, messageLog);
        char* message = "GAME FULL";
        sendResponse(flagRoom,-1,connfd,message,logFile);
        pthread_exit(NULL);
    }
}

void receiveRequest(int connfd, int numberOfRoom, int numberOfPlayer, char* logFile){
    char buff[RECV_BUFFER_SIZE];
    memset(buff, 0, sizeof(buff));

    char* messageLog;

    ssize_t bytes_received = recv(connfd, buff, sizeof(buff), 0);

    if (bytes_received == -1) {
        if (errno == EWOULDBLOCK || errno == EAGAIN) {
            usleep(10000);
        } else {
            messageLog = "Error while receiving data from the client";
            writeLogRoom(numberOfRoom,numberOfPlayer,logFile,messageLog);
            perror("Error while receiving data from the client");
            exit(1);
        }
    } else if (bytes_received == 0) {
        // El cliente ha cerrado la conexión
        messageLog = "Client closes connection";
        writeLogRoom(numberOfRoom,numberOfPlayer,logFile,messageLog);
        close(connfd);
    } else {
        // Procesar los datos recibidos
        printf("From client: %s\n", buff);
        classifyRequest(connfd,buff,numberOfRoom,numberOfPlayer,logFile);
    }
}

void sendResponse(int numberOfRoom, int numberOfPlayer, int connfd, char *response, char *logFile){
    int totalLength = snprintf(NULL, 0, "Server sends: %s", response);
    char *messageLog = (char*)malloc(totalLength + 1);  // +1 para el carácter nulo
    snprintf(messageLog, totalLength + 1, "Server sends: %s", response);

    writeLogRoom(numberOfRoom,numberOfPlayer,logFile,messageLog);
    send(connfd, response, strlen(response),0);
    printf("To client: %s\n", response);
}

void classifyRequest(int connfd, char *request, int numberOfRoom, int numberOfPlayer, char* logFile){

    char *tokens[3];
    char *token;
    char *messageLog;
    int i = 0;

    token = strtok(request, " ");

    while(token != NULL){
        tokens[i] = token;
        token = strtok(NULL, " ");
        i++;
    }

    if(strcmp(tokens[0], GAME) == 0){
        if(strcmp(tokens[1],POINT)==0){
            reqGamePoint(numberOfRoom, numberOfPlayer, tokens[2], logFile);
        }
        else if (strcmp(tokens[1],END)==0){
            messageLog = "Server receives that the game ended";
            writeLogRoom(numberOfRoom,numberOfPlayer,logFile,messageLog);
            reqGameEnd(connfd,numberOfRoom, numberOfPlayer);
        }
        else{
            //UNRECOGNIZED
            messageLog = "Error: <GAME>, second parameter unrecognized";
            writeLogRoom(numberOfRoom,numberOfPlayer,logFile,messageLog);
            printf("Error: <GAME>, second parameter unrecognized");
        }
    }
    else if(strcmp(tokens[0],PLAYER)==0){
        if(strcmp(tokens[1],NEW)==0){
            messageLog = "Server receives a new player";
            writeLogRoom(numberOfRoom,numberOfPlayer,logFile,messageLog);
            reqPlayerNew(connfd,tokens[2],numberOfRoom,numberOfPlayer, logFile);
        }
        else if(strcmp(tokens[1],LEFT)==0){
            messageLog = "Server receives that a player left the game during the match";
            writeLogRoom(numberOfRoom,numberOfPlayer,logFile,messageLog);
            reqPlayerLeft(connfd, numberOfRoom, numberOfPlayer, logFile);
        }
        else if(strcmp(tokens[1],BYE)==0){
            messageLog = "Server receives the confirmation that leaves the room after winning by others left";
            writeLogRoom(numberOfRoom,numberOfPlayer,logFile,messageLog);
            reqPlayerBye(connfd, numberOfRoom, numberOfPlayer);
        }
        else if(strcmp(tokens[1],QUIT)==0){
            messageLog = "Server receives that a player left the game at the waiting room";
            writeLogRoom(numberOfRoom,numberOfPlayer,logFile,messageLog);
            reqPlayerQuit(connfd, numberOfRoom, numberOfPlayer);
        }
        else{
            messageLog = "Error: <PLAYER>, second parameter unrecognized";
            writeLogRoom(numberOfRoom,numberOfPlayer,logFile,messageLog);
            printf("Error: <PLAYER>, second parameter unrecognized");
        }
    }
    else if(strcmp(tokens[0],PAD)==0){
        if(strcmp(tokens[1],UP)==0){
            messageLog = "Server receives that the pad is going upwards";
            writeLogRoom(numberOfRoom,numberOfPlayer,logFile,messageLog);
            reqPadUp(numberOfRoom, numberOfPlayer, logFile);
        }
        else if(strcmp(tokens[1],DOWN)==0){
            messageLog = "Server receives that the pad is going downwards";
            writeLogRoom(numberOfRoom,numberOfPlayer,logFile,messageLog);
            reqPadDown(numberOfRoom, numberOfPlayer, logFile);
        }
        else if(strcmp(tokens[1],STILL)==0){
            messageLog = "Server receives that the pad is still";
            writeLogRoom(numberOfRoom,numberOfPlayer,logFile,messageLog);
            reqPadStill(numberOfRoom, numberOfPlayer, logFile);
        }
        else{
            messageLog = "Error: <PAD>, second parameter unrecognized";
            writeLogRoom(numberOfRoom,numberOfPlayer,logFile,messageLog);
            printf("Error: <PAD>, second parameter unrecognized");
        }
    }
    else{
        messageLog = "Error: first parameter unrecognized while receiving a request";
        writeLogRoom(numberOfRoom,numberOfPlayer,logFile,messageLog);
        printf("Error: first parameter unrecognized");
    }
}

void reqPlayerLeft(int connfd, int numberOfRoom, int numberOfPlayer, char *logFile){
    char* response = "PLAYER DISCONNECTED";
    pthread_mutex_lock(&rooms[numberOfRoom].mutex);
    if (connfd == rooms[numberOfRoom].connfd1){
        sendResponse(numberOfRoom, 2, rooms[numberOfRoom].connfd2, response, logFile);
    }
    else if (connfd == rooms[numberOfRoom].connfd2){
        sendResponse(numberOfRoom, 1, rooms[numberOfRoom].connfd1, response, logFile);
    }
    rooms[numberOfRoom].clientsConnected = 0;
    rooms[numberOfRoom].nicknamePlayer1 = "";
    rooms[numberOfRoom].nicknamePlayer2 = "";
    rooms[numberOfRoom].connfd1 = -1;
    rooms[numberOfRoom].connfd2 = -1;
    rooms[numberOfRoom].scorePlayer1 = 0;
    rooms[numberOfRoom].scorePlayer2 = 0;
    rooms[numberOfRoom].open = true;
    pthread_mutex_unlock(&rooms[numberOfRoom].mutex);
    shutdown(connfd, SHUT_RDWR);
    pthread_exit(NULL);
}

void reqPlayerBye(int connfd, int numberOfRoom, int numberOfPlayer){
    pthread_exit(NULL);
}

void reqPlayerQuit(int connfd, int numberOfRoom, int numberOfPlayer){
    pthread_mutex_lock(&rooms[numberOfRoom].mutex);
    rooms[numberOfRoom].clientsConnected--;
    rooms[numberOfRoom].nicknamePlayer1 = NULL;
    rooms[numberOfRoom].connfd1 = -1;
    pthread_mutex_unlock(&rooms[numberOfRoom].mutex);

    pthread_exit(NULL);
}

void reqGameEnd(int connfd, int numberOfRoom, int numberOfPlayer){
    pthread_mutex_lock(&rooms[numberOfRoom].mutex);
    rooms[numberOfRoom].clientsConnected = 0;
    rooms[numberOfRoom].nicknamePlayer1 = "";
    rooms[numberOfRoom].nicknamePlayer2 = "";
    rooms[numberOfRoom].connfd1 = -1;
    rooms[numberOfRoom].connfd2 = -1;
    rooms[numberOfRoom].scorePlayer1 = 0;
    rooms[numberOfRoom].scorePlayer2 = 0;
    rooms[numberOfRoom].open = true;
    pthread_mutex_unlock(&rooms[numberOfRoom].mutex);
    
    pthread_exit(NULL);
}

void reqGamePoint(int numberOfRoom, int numberOfPlayer, char* side, char* logFile){
    pthread_mutex_lock(&rooms[numberOfRoom].mutex);
    if (numberOfPlayer==1){
        rooms[numberOfRoom].scorePlayer1 += 1;
    }
    else {
        rooms[numberOfRoom].scorePlayer2 += 1;
    }
    pthread_mutex_unlock(&rooms[numberOfRoom].mutex);

    int totalLength = snprintf(NULL, 0, "Server receives that %s scores a point", side);
    char *messageLog = (char*)malloc(totalLength + 1);  // +1 para el carácter nulo
    snprintf(messageLog, totalLength + 1, "Server receives that %s scores a point", side);

    writeLogRoom(numberOfRoom,numberOfPlayer,logFile,messageLog);
}

void writeLogRoom(int numberOfRoom, int numberOfPlayer, char* logFile, char* message){
    int totalLength = snprintf(NULL, 0, "- source[room: %d|player: %d] - %s", numberOfRoom, numberOfPlayer, message);
    char *messageLog = (char*)malloc(totalLength + 1);  // +1 para el carácter nulo
    snprintf(messageLog, totalLength + 1, "- source[room: %d|player: %d] - %s", numberOfRoom, numberOfPlayer, message);

    writeLog(logFile, messageLog);
}

void writeLog(char* logFile, char* message){
    FILE *f = fopen(logFile, "a");
    if (f == NULL){
        printf("Error opening file!\n");
        exit(1);
    }
    // Obtener la hora actual en segundos desde la época
    time_t actualTime;
    struct tm *infoTime;
    
    time(&actualTime);
    infoTime = localtime(&actualTime);

    // Formatear y mostrar la fecha y hora actual
    fprintf(f,"[%02d/%02d/%04d %02d:%02d:%02d] %s\n",
           infoTime->tm_mday, infoTime->tm_mon + 1, infoTime->tm_year + 1900,
           infoTime->tm_hour, infoTime->tm_min, infoTime->tm_sec,message);
    fclose(f);
}

void reqPlayerNew(int connfd, char* nickname, int numberOfRoom, int numberOfPlayer, char *logFile){
    
    if(numberOfPlayer == 1){
        rooms[numberOfRoom].nicknamePlayer1 = strdup(nickname);
        rooms[numberOfRoom].connfd1 = connfd;
        char* response = "PLAYER WAIT";
        sendResponse(numberOfRoom, numberOfPlayer, connfd, response, logFile);
    }
    else if(numberOfPlayer == 2){
        rooms[numberOfRoom].nicknamePlayer2=strdup(nickname);
        rooms[numberOfRoom].connfd2 = connfd;
    }
}

void reqPadUp(int numberOfRoom, int numberOfPlayer, char *logFile){
    char* response;
    if(numberOfPlayer == 1){
        response = "PAD MOVE UP LEFT";
    }
    else if(numberOfPlayer == 2){
        response = "PAD MOVE UP RIGHT";
    }

    sendResponse(numberOfRoom, 1, rooms[numberOfRoom].connfd1, response, logFile);
    sendResponse(numberOfRoom, 2, rooms[numberOfRoom].connfd2, response, logFile);
}

void reqPadDown(int numberOfRoom, int numberOfPlayer, char *logFile){
    char* response;
    if(numberOfPlayer == 1){
        response = "PAD MOVE DOWN LEFT";
    }
    else if(numberOfPlayer == 2){
        response = "PAD MOVE DOWN RIGHT";
    }

    sendResponse(numberOfRoom, 1, rooms[numberOfRoom].connfd1, response, logFile);
    sendResponse(numberOfRoom, 2, rooms[numberOfRoom].connfd2, response, logFile);
}

void reqPadStill(int numberOfRoom, int numberOfPlayer, char *logFile){
    char* response;
    if(numberOfPlayer == 1){
        response = "PAD MOVE STILL LEFT";
    }
    else if(numberOfPlayer == 2){
        response = "PAD MOVE STILL RIGHT";
    }

    sendResponse(numberOfRoom, 1, rooms[numberOfRoom].connfd1, response, logFile);
    sendResponse(numberOfRoom, 2, rooms[numberOfRoom].connfd2, response, logFile);
}

void closeConnection(int sockfd){
    close(sockfd);
}