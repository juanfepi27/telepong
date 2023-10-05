import socket
import sys
from constants import *

def set_up_client(nicknamePlayer):
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.setblocking(False)
    if client_socket == None:
        print("Error: Socket could not be created.")
        sys.exit(1)
    else:
        print("Socket successfully created ")
    
    try:
        client_socket.connect((IP_SERVER,PORT))
    except BlockingIOError:
        pass
        
    local_tuple = client_socket.getsockname()
    print("Socket binded to: ", local_tuple)
    send_request(client_socket,"PLAYER NEW " + nicknamePlayer)
    return client_socket

def send_request(client_socket,message):
    print("To server: ", message, "\n")
    client_socket.send(bytes(message, ENCONDING_FORMAT))

def classify_request(request):

    arr_request=request.split(' ')

    if(arr_request[0] == GAME):

        if(arr_request[1] == POINT):
            req_game_point()
        else:
            unrecognized_data(request)

    elif(arr_request[0] == PLAYER):

        if(arr_request[1] == NEW):
            req_player_new()
        elif(arr_request[1] == LEFT):
            req_player_left()
        else:
            unrecognized_data(request)

    elif(arr_request[0] == PAD):

        if(arr_request[1] == UP):
            req_pad_up()
        elif(arr_request[1] == DOWN):
            req_pad_down()
        elif(arr_request[1] == STILL):
            req_pad_still()
        else:
            unrecognized_data(request)

    elif(arr_request[0] == BALL):

        if(arr_request[1] == DATA):
            req_ball_data()
        else:
            unrecognized_data(request)
    else:
        unrecognized_data(request)

def classify_response(response):

    arr_response=response.split(' ')

    if(arr_response[0] == GAME):
        if(arr_response[1] == START):
            return resp_game_start(arr_response)
        elif(arr_response[1] == END):
            resp_game_end()
        elif(arr_response[1] == SCORE):
            resp_game_score()
        else:
            unrecognized_data(response)

    elif(arr_response[0] == PLAYER):
        if(arr_response[1] == WAIT):
            return resp_player_wait()
        elif (arr_response[1] == DISCONNECTED):
            return resp_player_disconnected(arr_response)
        else:
            unrecognized_data(response)

    elif(arr_response[0] == PAD):
        if(arr_response[1] == MOVE):
            return resp_pad_move(arr_response)
            
        else:
            unrecognized_data(response)

    elif(arr_response[0] == BALL):
        if(arr_response[1] == CHANGE):
            return resp_ball_change(arr_response)
        else:
            unrecognized_data(response)
    else:
        unrecognized_data(response)

def receive_response(client_socket):
    try:
        data = client_socket.recv(RECV_BUFFER_SIZE)
        print('Received from server: ', data.decode())
        return classify_response(data.decode())
    except BlockingIOError:
        pass

##game
###REQUEST
def req_game_point():
    pass
###RESPONSE
def resp_game_start(arr_response):
    arr_return = [arr_response[1],arr_response[2],arr_response[3]]
    return arr_return

def resp_game_end():
    pass

def resp_game_score():
    pass

##player
###REQUEST
def req_player_new():
    pass
def req_player_left():
    pass
###RESPONSE
def resp_player_wait():
    return 'WAIT'

def resp_player_disconnected(arr_response):
    arr_return = [arr_response[0], arr_response[1]]
    return arr_return

##pad
###REQUEST
def req_pad_up():
    pass
def req_pad_down():
    pass
def req_pad_still():
    pass
###RESPONSE
def resp_pad_move(arr_response):
    arr_return = [arr_response[0], arr_response[2], arr_response[3]]
    return arr_return

##ball
###REQUEST
def req_ball_data():
    pass
###RESPONSE
def resp_ball_change(arr_response):
    return arr_response

#unrecognized
def unrecognized_data(command:str):
    response = UNRECOGNIZED+'\n'