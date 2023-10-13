from constants import *
import socket
import time
import sys

def set_up_client(nicknamePlayer):
    #create the socket
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #setting as non-blocking socket
    client_socket.setblocking(False)
    if client_socket == None:
        print("Error: Socket could not be created.")
        sys.exit(1)
    else:
        print("Socket successfully created ")

    #trying to connect the socket to the server 
    try:
        client_socket.connect((IP_SERVER,PORT))
    except BlockingIOError:
        pass

    #showing the connection
    local_tuple = client_socket.getsockname()
    print("Socket binded to: ", local_tuple)

    #sending the request of a new player
    send_request(client_socket,"PLAYER NEW " + nicknamePlayer)

    #return the socket
    return client_socket

def send_request(client_socket,message):
    #debugging the sent information
    print("To server: ", message, "\n")

    #addaption to send the request if the server doesn't receive it 
    while True:
        try:
            client_socket.send(bytes(message, ENCONDING_FORMAT))
            break
        except BlockingIOError:
            time.sleep(0.1)

def classify_response(response):
    #analize the response from the server
    arr_response=response.split(' ')

    #game responses
    if(arr_response[0] == GAME):
        if(arr_response[1] == START):
            return resp_game_start(arr_response)
        elif(arr_response[1] == FULL):
            return resp_game_full(arr_response)
        else:
            unrecognized_data(response)

    #player responses
    elif(arr_response[0] == PLAYER):
        if(arr_response[1] == WAIT):
            return resp_player_wait(arr_response)
        elif (arr_response[1] == DISCONNECTED):
            return resp_player_disconnected(arr_response)
        else:
            unrecognized_data(response)

    #pad responses
    elif(arr_response[0] == PAD):
        if(arr_response[1] == MOVE):
            return resp_pad_move(arr_response)
        else:
            unrecognized_data(response)

    else:
        unrecognized_data(response)

def receive_response(client_socket):
    #if there is no info, just pass
    try:
        #receive data from the buffer, 
        data = client_socket.recv(RECV_BUFFER_SIZE)

        #debug print
        print('Received from server: ', data.decode())

        #return the data
        return classify_response(data.decode())
    except BlockingIOError:
        pass

##game
def resp_game_start(arr_response):
    #return just the start directive and the parameters (both names)
    arr_return = [arr_response[1],arr_response[2],arr_response[3]]
    return arr_return

def resp_game_full(arr_response):
    #return the full directive
    arr_return = [arr_response[1]]
    return arr_return

##player
def resp_player_wait(arr_response):
    #return the wait directive
    arr_return = [arr_response[1]]
    return arr_return

def resp_player_disconnected(arr_response):
    #return the player disconnected directive
    arr_return = [arr_response[0], arr_response[1]]
    return arr_return

##pad
def resp_pad_move(arr_response):
    #return the directive pad <move> <side>
    arr_return = [arr_response[0], arr_response[2], arr_response[3]]
    return arr_return

#unrecognized
def unrecognized_data(response):
    print(UNRECOGNIZED+': '+response+'\n') 