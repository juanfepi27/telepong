from pongGame.gameConstants import *
from pongGame.Striker import *
from pongGame.Ball import *
from pongProtocol import *
import pygame
import sys

def login(screen,font,clock):
	# Runner for login
	runningLogin = True

	# Text Login player 
	textPlayer = font.render("Login player", True, WHITE)
	textRectPlayer = textPlayer.get_rect()
	textRectPlayer.center = (WIDTH//2, 200)
	
	# Text Enter your nickname
	textNickname = font.render("Enter your nickname ", True, WHITE)
	textRectNickname = textNickname.get_rect()
	textRectNickname.center = (WIDTH//2, 270)

	# Input nickname
	inputNickname = pygame.Rect(WIDTH//2-140, 300, 140, 32)
	activeNickname = False
	valueNickname = ''

	# Colors for inputs
	colorActive = pygame.Color(GREEN)
	colorPassive = pygame.Color(WHITE)
	colorNickname = colorPassive

	# Play button
	playButton = pygame.Rect(400, 350, 100, 50)
	playButtonText = font.render("Play", True, BLACK)
	playButtonTextRect = playButtonText.get_rect()
	playButtonTextRect.center = (450, 375)

	# Filling the screen
	screen.fill(BLACK)
	screen.blit(textPlayer, textRectPlayer)
	screen.blit(textNickname, textRectNickname)
	pygame.draw.rect(screen, WHITE, playButton)
	screen.blit(playButtonText, playButtonTextRect)
	
	# Exit button
	exitBtn = pygame.Rect(850, 10, 25, 25)
	valueBtn = 'X'
	pygame.draw.rect(screen, WHITE, exitBtn)
	textExit = font.render(valueBtn, True, BLACK)
	screen.blit(textExit, (exitBtn.x+5, exitBtn.y+5))

	while runningLogin:

		for event in pygame.event.get():
			# If clicks on X
			if event.type == pygame.QUIT:
				sys.exit(0)

			# If clicks on any input
			if event.type == pygame.MOUSEBUTTONDOWN:
				if inputNickname.collidepoint(event.pos):
					activeNickname = True
				else:
					activeNickname = False

				if playButton.collidepoint(event.pos):
					if valueNickname != '':
						runningLogin = False

				if exitBtn.collidepoint(event.pos):
					sys.exit(0)

			# If types any letter
			if event.type == pygame.KEYDOWN:
				if activeNickname:
					if event.key == pygame.K_BACKSPACE:
						valueNickname = valueNickname[:-1]
					else:
						valueNickname += event.unicode

		# Show when the input is active
		if activeNickname:
			colorNickname = colorActive
		else:
			colorNickname = colorPassive

		# Rectangle for inputNickname field
		pygame.draw.rect(screen, colorNickname, inputNickname)
		textSurfaceNickname = font.render(valueNickname, True, BLACK)
		# Render at position stated in arguments
		screen.blit(textSurfaceNickname, (inputNickname.x+5, inputNickname.y+5))
		# Set width of textfield so that text cannot get outside of user's text input
		inputNickname.w = max(300, textSurfaceNickname.get_width()+10)

		pygame.display.flip()
		clock.tick(FPS)

	return valueNickname

def waitingRoom(screen,font,clock,running,client_socket):
	# Keep waiting while enter another player 
	while running!='START':
		# Set up screen
		screen.fill(BLACK)

		# Exit button
		exitBtn = pygame.Rect(850, 10, 25, 25)
		valueBtn = 'X'
		pygame.draw.rect(screen, WHITE, exitBtn)
		textExit = font.render(valueBtn, True, BLACK)
		screen.blit(textExit, (exitBtn.x+5, exitBtn.y+5))

		# Waiting text
		text = font.render("Waiting for another player to connect", True, WHITE)
		textRect = text.get_rect()
		textRect.center = (WIDTH//2, HEIGHT//2)
		screen.blit(text, textRect)
		pygame.display.update()
		clock.tick(FPS)

		# Handling if a player quits while s/he was waiting
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				message = "PLAYER QUIT"
				send_request(client_socket, message)
				sys.exit(0)
			if event.type == pygame.MOUSEBUTTONDOWN:
				if exitBtn.collidepoint(event.pos):
					message = "PLAYER QUIT"
					send_request(client_socket, message)
					sys.exit(0)

		# Handles the response for another player connected or if there are no rooms
		arr_return = receive_response(client_socket)
		if(arr_return):
			if(arr_return[0]==START):
				running = arr_return[0]
			elif(arr_return[0]==FULL):
				# Set up screen
				screen.fill(BLACK)

				# Text no rooms
				textWinner = font.render("No rooms available yet, check back soon", True, WHITE)
				textRectWinner = textWinner.get_rect()
				textRectWinner.center = (WIDTH//2, HEIGHT//2)
				screen.blit(textWinner, textRectWinner)
				pygame.display.update()

				# Wait 7 seconds to kick out the player
				pygame.time.wait(7000)
				sys.exit(0)

	return arr_return[1], arr_return[2]

def pong(screen,font,clock,nicknamePlayer1,nicknamePlayer2,client_socket):
	# Runner for the game
	running = True

	# Defining the objects
	geek1 = Striker(screen,font,0, 0, 10, 100, 10, GREEN)
	geek2 = Striker(screen,font,WIDTH-10, 0, 10, 100, 10, GREEN)
	ball = Ball(screen,WIDTH//2, HEIGHT//2, 10, 10, WHITE)

	listOfGeeks = [geek1, geek2]

	# Initial parameters of the players
	geek1Score, geek2Score = 0, 0
	geek1YFac, geek2YFac = 0, 0

	while running:
		# Set up screen
		screen.fill(BLACK)

		# Exit button
		exitBtn = pygame.Rect(WIDTH//2, 10, 25, 25)
		valueBtn = 'X'
		pygame.draw.rect(screen, WHITE, exitBtn)
		textExit = font.render(valueBtn, True, BLACK)
		screen.blit(textExit, (exitBtn.x+5, exitBtn.y+5))

		# Receiving events from the server
		arr_return = receive_response(client_socket)
		
		if(arr_return):
			# Pad events
			if(arr_return[0] == PAD):
				# Changing the Yfacs according to the key events sent by the server
				if(arr_return[1] == UP):
					if(arr_return[2] == LEFT):
						geek1YFac = -1
					else:
						geek2YFac = -1
				elif(arr_return[1] == DOWN):
					if(arr_return[2] == LEFT):
						geek1YFac = 1
					else: 
						geek2YFac = 1
				else:
					if(arr_return[2] == LEFT):
						geek1YFac = 0
					else: 
						geek2YFac = 0
			# Player events
			elif(arr_return[0] == PLAYER):
				# If the other player closes the game
				if(arr_return[1] == DISCONNECTED):
					# Send the confirmation
					message = "PLAYER BYE"
					send_request(client_socket, message)

					# Set up win screen
					screen.fill(BLACK)
					textWinner = font.render(f"You won! the other player left the game", True, WHITE)
					textRectWinner = textWinner.get_rect()
					textRectWinner.center = (WIDTH//2, HEIGHT//2)
					screen.blit(textWinner, textRectWinner)

					# Wait 7 seconds to kick out the player
					pygame.display.update()
					pygame.time.wait(7000)
					running = False

		# Event handling -> send request
		for event in pygame.event.get():
			# Leaves the game (disconnect)
			if event.type == pygame.QUIT:
				message = "PLAYER LEFT "
				send_request(client_socket, message)
				sys.exit(0)

			# Pressing keys
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					message = "PAD UP "
					send_request(client_socket, message)
				if event.key == pygame.K_DOWN:
					message = "PAD DOWN "
					send_request(client_socket, message)

			# Releasing keys
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					message = "PAD STILL "
					send_request(client_socket, message)

			# Press X button
			if event.type == pygame.MOUSEBUTTONDOWN:
				if exitBtn.collidepoint(event.pos):
					message = "PLAYER LEFT "
					send_request(client_socket, message)
					sys.exit(0)

		# Collision detection
		for geek in listOfGeeks:
			if pygame.Rect.colliderect(ball.getRect(), geek.getRect()):
				ball.hit()

		# Updating the objects
		geek1.update(geek1YFac)
		geek2.update(geek2YFac)
		
		point = ball.update()

		# -1 -> Geek_1 has scored
		# +1 -> Geek_2 has scored
		# 0 -> None of them scored
		if point == -1:
			message = "GAME POINT LEFT "
			send_request(client_socket, message)
			geek1Score += 1
		elif point == 1:
			message = "GAME POINT RIGHT "
			send_request(client_socket, message)
			geek2Score += 1

		# Someone has scored a point and the ball is out of bounds. So, we reset it's position
		if point:
			ball.reset()

		# Displaying the objects on the screen
		geek1.display()
		geek2.display()
		ball.display()

		# Displaying the scores of the players
		geek1.displayScore(f"{nicknamePlayer1} : ",geek1Score, 100, 20, WHITE)
		geek2.displayScore(f"{nicknamePlayer2} : ",geek2Score, WIDTH-100, 20, WHITE)

		pygame.display.update()
		clock.tick(FPS)

		if geek1Score == 10 or geek2Score == 10:
			# Stop the runner
			running = False

			# Set up screen
			screen.fill(BLACK)

			# Sends the request that the game has ended
			message = "GAME END"
			send_request(client_socket, message)

			# Winner text
			if(geek1Score == 5):
				textWinner = font.render(f"{nicknamePlayer1} won!", True, WHITE)
			else:
				textWinner = font.render(f"{nicknamePlayer2} won!", True, WHITE)
			textRectWinner = textWinner.get_rect()
			textRectWinner.center = (WIDTH//2, HEIGHT//2)
			screen.blit(textWinner, textRectWinner)

			# Disconnection advise
			textWinner2 = font.render("You are going to be disconnected in 7 seconds", True, WHITE)
			textRectWinner2 = textWinner2.get_rect()
			textRectWinner2.center = (WIDTH//2, HEIGHT//2+40)
			screen.blit(textWinner2, textRectWinner2)
			pygame.display.update()

			# Wait 7 seconds to kick out the player
			pygame.time.wait(7000)
			sys.exit(0)
