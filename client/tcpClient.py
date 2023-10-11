from pongGame.gameConstants import *
from pongGame.Game import *
from pongProtocol import *
from constants import *
import pygame

if __name__ == '__main__':
	#set up game
    pygame.init()
    font = pygame.font.Font('freesansbold.ttf', 20)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()

	#login
    nicknameCurrentPlayer = login(screen,font,clock)

	#connect with the server
    client_socket = set_up_client(nicknameCurrentPlayer)
    action_response = receive_response(client_socket)

	#keep waiting for anothe player 
    player_names = waitingRoom(screen,font,clock,action_response,client_socket)
    
	#play 
    pong(screen,font,clock,player_names[0],player_names[1], client_socket)