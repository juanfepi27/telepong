# Telepong Project
#### Juan Felipe Pinzón, Miguel Ángel Calvache and Maria Paula Ayala

## 1. Introduction
In this repository you'll find the documentation of our project, an implementation of the classic Pong game in a server-client architecture. In this guide we will take you through the process we took to create this project, from the design to the implementation of it. 

## 2. Project overview
Our implementation of the Pong game is not just a recreation of the traditional game; it's an exploration of the fascinating realm of networking and multiplayer gaming. By implementing a server-client architecture and harnessing the power of socket programming, we've taken Pong to the next level.

- This project is structured around a central server and multiple clients. The server functions as the game coordinator, handling game state, synchronization, and communication between clients. The clients, in the other hand, handle user inputs and display the game interface. This design ensures a seamless and responsive gaming experience, while also enabling multiplayer gameplay across different devices.

- Menawhile, socket programming is at the heart of this project. It allows for efficient and low-latency communication between the server and clients, making gameplay feel instantaneous and dynamic. Through the use of sockets, we've enabled the real-time exchange of game data, creating an engaging and interactive experience.

Now, let's dive into the details of each part of this project. 

## 3. Pong protocol
For starters, in this project, we created our own protocol for the communication between the server and the client. You'll find this protocol in Python and in C giving that the code of the client is made in Python and the server is in C. 

To explain how our protocol works first take a look at the activity diagram below: 

![Pong Protocol](https://github.com/juanfepi27/telepong/assets/85038378/c90e0429-1364-4058-8b7c-b968a9f3283e)
Or you can also go to this [link](https://drive.google.com/file/d/1Af47fn7xyPEkDO0muV7jz2pVc5oP14fP/view?usp=sharing) and see it with more details.

As you can see the process goes in this order:

1. The server is set up, which means the socket is created and is waiting for clients to connect to it.

2. The client in the other hand is also set up and connected to the server. Then it sends a message to the server saying PLAYER NEW <username>

3. The server receives this message and checks if there is another player already connected, if there is only one player connected it sends PLAYER WAIT to the client and when they receive it, it takes the client to a black screen with the message "Waiting for other players". In case there was already another player connected the server sends the message GAME START <username1> <username2> and it takes both players to the interface of the game. Finally, in case the maximum amount of players were already connected the server send GAME FULL, which means that the player needs to wait for a game to end for it to connect.

4. When the game starts the server is constantly hearing both clients to check if they send any event and if so it sends the respective response. Meanwhile the client is also constantly sending messages and hearing for the responses of the server. Down below we are going to specify each message that the client can send and the responses of the server:

    - PAD UP: When the client presses the up arrow key it sends this message to the server, the server analyzes which of the clients send it and classifies it as LEFT or RIGHT, it then sends the message PAD MOVE to both clients and changes the position of the respective pad.

    - PAD DOWN: When the client presses the down arrow key it sends this message to the server, the server analyzes which of the clients send it and classifies it as LEFT or RIGHT, it then sends the message PAD MOVE to both clients and changes the position of the respective pad.

    - PAD STILL: When the client doesn't press any key it sends this message to the server, the server analyzes which of the clients send it and classifies it as LEFT or RIGHT, it then sends the message PAD MOVE to both clients and changes the position of the respective pad.

    - PLAYER LEFT: When the client closes the interface in the middle of the game it sends this message to the server and the server sends PLAYER DISCONNECTED, which takes the player that still remains in the game to a black screen with the message "You won! the other player left the game".

    - PLAYER BYE:  A message of confirmation that the client received the message of PLAYER DISCONNECTED and that it will end the game for the other player.

    - PLAYER QUIT: The client close the game while still in the waiting room, the server just receives that information and updates that there are no clients waiting.

    - GAME POINT: When the client scores a point it sends this message to the server, the server then analyzes which of the clients send it and classifies it as LEFT or RIGHT. This is send from both clients to check that both clients are synchronized. 

    - GAME END: This message is sent when one of the players scores 5 points and it just ends the game for both players with the message of who won.

5. When the messages received or send are linked to the game ending (GAME END, PLAYER QUIT or PLAYER BYE) the server kills the communication with that client and the interface of the game is closed for the client. 

## 4. Running the project
*Before reading the instructions you should know that our game only runs in computers that have Linux.*

Our server is up in AWS, working in the port 50000 and with a public IP that is changing each time we start the instance, so what you'll need to do to play our game is to download the client folder and in the file constants.py change the IP to the one we tell you to. After you change that, just run in your terminal the file tcpClient.py and the interface of the game should appear.

The first thing you'll need to do is create a username and press the play button, then, as explained before, if there are not other players already connected you will see a black screen with the message "Waiting for other players", in case there was already someone connected you will be taken to the game immediately. The game ends when one of the players gets to 5 points or if someone leaves the game. 

Our game supports until 10 players at the same time, and it connects people in order of arrival, you don't choose who you want to play with. 

## 5. Conclusions
- For this project we had the option of choosing between TCP or UDP protocol, in our case we chose TCP. We made this decision because in the game of Pong is extremely important the precise synchronization and consistent updates, it relies on real time communication and managing lost data effectively and TCP offers us this since it is connection-oriented.

    TCP has a dedicated and a persistent connection between the client and server is established. In contrast, UDP is connectionless, therefore it may lead to packet loss and out-of-order delivery of information, which is not optimal for the game since one player can see different things in their screen. However we are aware that UDP is faster than TCP, but for us is more important that several players can play simultaneously with the certainty that the information is the same for everyone than a few miliseconds of delay. 

    Lastly, as we are aware that there will be delays in the information that's why we limit the amount of users to 10 at the same time, so we don't have the risk of increasing the delay because of the amount of connections. 

- In the process of making this project we faced several challenges, one of them was making our own text-based protocol. Nonetheless, we consider this was a great approach since we could make the protocol highly compatible to our game and in this way we only creatd what we needed, rather than using one protocol already created in where we may have not used all of its methods or actions.

    Also, a great advantage of creating our own protocol was that we could dive into how the information flows in the internet and in this type of games and we can use this knowledge in future projects. 

- Finally, we found very interesting how we could connect a server and a client in two different programming languages. It expanded our horizons as developers and got us out of our comfort zone by getting to know languages we hadn't used and to understand better how the socket programming works in different environments. 

## 6. References
- https://www.geeksforgeeks.org/tcp-server-client-implementation-in-c/
- https://beej.us/guide/bgnet/
- https://beej.us/guide/bgc/
- https://youtu.be/U28svzb1WUs?si=6NuH1-Koet5_2uQc
- https://www.geeksforgeeks.org/create-a-pong-game-in-python-pygame/
