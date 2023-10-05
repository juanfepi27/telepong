#ifndef _MY_PONG_PROTOCOL
#define _MY_PONG_PROTOCOL

#define PORT 50000
#define ENCONDING_FORMAT "utf-8"
#define RECV_BUFFER_SIZE 4096
#define IP_SERVER '127.0.0.1'
#define SA struct sockaddr
#define MAX_ROOMS 5

// GAME
const char* GAME = "GAME"; 
const char* START = "START"; //When the two users are connected
const char* END = "END"; //When the game is over because one of the two players has won
const char* POINT = "POINT"; //When one of the two players scores a point
const char* SCORE = "SCORE"; //When the game score changes because one of the two players scores a point

// PLAYER
const char* PLAYER = "PLAYER"; 
const char* NEW = "NEW"; //When a new player is connected
const char* WAIT = "WAIT"; //When a player is waiting for another player to connect
const char* LEFT = "LEFT"; //When a player leaves the game with the X button
const char* DISCONNECTED = "DISCONNECTED"; //When a player leaves the game
const char* BYE = "BYE"; //When a player leaves and the second player confirms the dicconnection
const char* QUIT = "QUIT"; //When the client leaves the waiting room

// PAD
const char* PAD = "PAD";
const char* UP = "UP"; //When a player presses the up arrow
const char* DOWN = "DOWN"; //When a player presses the down arrow
const char* STILL = "STILL"; //When a player releases the up or down arrow
const char* MOVE = "MOVE"; //server response to a PAD_UP, PAD_DOWN or PAD_STILL

// BALL
const char* BALL = "BALL";
const char* DATA = "DATA"; //when the client sends the ball data to the server
const char* CHANGE = "CHANGE"; //When the server sends the ball data to the client

// UNRECOGNIZED
#define UNRECOGNIZED = "UNRECOGNIZED"

void writeLog(char* logFile, char* message);
void writeLogRoom(int numberOfRoom, int numberOfPLayer, char* logFile, char* message);
int setUpServer(char* port, char* logFile);
void* handleClient(void* arg);
void receiveRequest(int connfd, int numberOfRoom, int numberOfPlayer, char* logFile);
void sendResponse(int numberOfRoom, int numberOfPlayer, int connfd, char *response, char* logFile);
void classifyRequest(int connfd, char *request, int numberOfRoom, int numberOfPlayer, char* logFile);
void reqPlayerLeft( int connfd, int numberOfRoom, int numberOfPlayer, char* logFile);
void reqPlayerBye(int connfd, int numberOfRoom, int numberOfPlayer);
void reqPlayerQuit(int connfd, int numberOfRoom, int numberOfPlayer);
void reqGameEnd(int connfd, int numberOfRoom, int numberOfPlayer);
void reqGamePoint(int numberOfRoom, int numberOfPLayer, char* side, char* logFile);
void reqPlayerNew(int connfd, char *nickname, int numberOfRoom, int numberOfPlayer, char* logFile);
void reqPadUp(int numberOfRoom, int numberOfPlayer, char* logFile);
void reqPadDown(int numberOfRoom, int numberOfPlayer, char* logFile);
void reqPadStill(int numberOfRoom, int numberOfPlayer, char* logFile);
void closeConnection(int sockfd);

# include "myPongProtocol.c"
# endif