from myPongProtocol import *
from constants import *
import pygame
import sys

class Striker:
		# Take the initial position, dimensions, speed and color of the object
	def __init__(self, posx, posy, width, height, speed, color):
		self.posx = posx
		self.posy = posy
		self.width = width
		self.height = height
		self.speed = speed
		self.color = color
		# Rect that is used to control the position and collision of the object
		self.geekRect = pygame.Rect(posx, posy, width, height)
		# Object that is blit on the screen
		self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

	# Used to display the object on the screen
	def display(self):
		self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

	def update(self, yFac):
		self.posy = self.posy + self.speed*yFac

		# Restricting the striker to be below the top surface of the screen
		if self.posy <= 0:
			self.posy = 0
		# Restricting the striker to be above the bottom surface of the screen
		elif self.posy + self.height >= HEIGHT:
			self.posy = HEIGHT-self.height

		# Updating the rect with the new values
		self.geekRect = (self.posx, self.posy, self.width, self.height)

	def displayScore(self, text, score, x, y, color):
		text = font20.render(text+str(score), True, color)
		textRect = text.get_rect()
		textRect.center = (x, y)

		screen.blit(text, textRect)

	def getRect(self):
		return self.geekRect

class Ball:
	def __init__(self, posx, posy, radius, speed, color):
		self.posx = posx
		self.posy = posy
		self.radius = radius
		self.speed = speed
		self.color = color
		self.xFac = 1
		self.yFac = -1
		self.ball = pygame.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)
		self.firstTime = 1

	def display(self):
		self.ball = pygame.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)

	def update(self):
		self.posx += self.speed*self.xFac
		self.posy += self.speed*self.yFac

		# If the ball hits the top or bottom surfaces, then the sign of yFac is changed and it results in a reflection
		if self.posy <= 0 or self.posy >= HEIGHT:
			self.yFac *= -1

		#if the ball makes point
		if self.posx <= 0 and self.firstTime:
			self.firstTime = 0
			return 1
		elif self.posx >= WIDTH and self.firstTime:
			self.firstTime = 0
			return -1
		else:
			return 0

	def reset(self):
		self.posx = WIDTH//2
		self.posy = HEIGHT//2
		self.xFac *= -1
		self.firstTime = 1

	# Used to reflect the ball along the X-axis
	def hit(self):
		self.xFac *= -1

	def getRect(self):
		return self.ball

def login():
	# runner for login
	runningLogin = True

	# Text Login player 
	textPlayer = font20.render("Login player", True, WHITE)
	textRectPlayer = textPlayer.get_rect()
	textRectPlayer.center = (WIDTH//2, 100)
	
	# Text Enter your nickname
	textNickname = font20.render("Enter your nickname ", True, WHITE)
	textRectNickname = textNickname.get_rect()
	textRectNickname.center = (405, 180)

	# input nickname
	inputNickname = pygame.Rect(300, 200, 140, 32)
	activeNickname = False
	valueNickname = ''

	# Text Enter your email
	textEmail = font20.render("Enter your email ", True, WHITE)
	textRectEmail = textEmail.get_rect()
	textRectEmail.center = (385, 270)

	# input email
	inputEmail = pygame.Rect(300, 290, 140, 32)
	activeEmail = False
	valueEmail = ''

	# colors for inputs
	colorActive = pygame.Color(GREEN)
	colorPassive = pygame.Color(WHITE)
	colorNickname = colorPassive
	colorEmail = colorPassive

	# Play button
	playButton = pygame.Rect(400, 350, 100, 50)
	playButtonText = font20.render("Play", True, BLACK)
	playButtonTextRect = playButtonText.get_rect()
	playButtonTextRect.center = (450, 375)

	screen.fill(BLACK)
	screen.blit(textPlayer, textRectPlayer)
	screen.blit(textNickname, textRectNickname)
	screen.blit(textEmail, textRectEmail)
	pygame.draw.rect(screen, WHITE, playButton)
	screen.blit(playButtonText, playButtonTextRect)

	exitBtn = pygame.Rect(850, 10, 25, 25)
	valueBtn = 'X'
	pygame.draw.rect(screen, WHITE, exitBtn)
	textExit = font20.render(valueBtn, True, BLACK)
	screen.blit(textExit, (exitBtn.x+5, exitBtn.y+5))

	while runningLogin:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
			# If click on any input
			if event.type == pygame.MOUSEBUTTONDOWN:
				if inputNickname.collidepoint(event.pos):
					activeNickname = True
					activeEmail = False
				else:
					activeNickname = False
		
				if inputEmail.collidepoint(event.pos):
					activeEmail = True
					activeNickname = False
				else:
					activeEmail = False

				if playButton.collidepoint(event.pos):
					if valueNickname != '' and valueEmail != '':
						runningLogin = False
				
				if exitBtn.collidepoint(event.pos):
					sys.exit(0)
				
			# If type any letter
			if event.type == pygame.KEYDOWN:
				if activeNickname:
					if event.key == pygame.K_BACKSPACE:
						valueNickname = valueNickname[:-1]
					else:
						valueNickname += event.unicode
				if activeEmail:
					if event.key == pygame.K_BACKSPACE:
						valueEmail = valueEmail[:-1]
					else:
						valueEmail += event.unicode
	
		if activeNickname:
			colorNickname = colorActive
		else:
			colorNickname = colorPassive

		if activeEmail:
			colorEmail = colorActive
		else:
			colorEmail = colorPassive

		# Rectangle for inputNickname field
		pygame.draw.rect(screen, colorNickname, inputNickname)
		textSurfaceNickname = font20.render(valueNickname, True, BLACK)
		# render at position stated in arguments
		screen.blit(textSurfaceNickname, (inputNickname.x+5, inputNickname.y+5))
		# set width of textfield so that text cannot get outside of user's text input
		inputNickname.w = max(300, textSurfaceNickname.get_width()+10)

		# Rectangle for inputEmail field
		pygame.draw.rect(screen, colorEmail, inputEmail)
		textSurfaceEmail = font20.render(valueEmail, True, BLACK)
		# render at position stated in arguments
		screen.blit(textSurfaceEmail, (inputEmail.x+5, inputEmail.y+5))
		# set width of textfield so that text cannot get outside of user's text input
		inputEmail.w = max(300, textSurfaceEmail.get_width()+10)

		pygame.display.flip()
		clock.tick(FPS)

	return valueNickname

def waitingRoom(running,client_socket):
	while running!='START':
		screen.fill(BLACK)
		exitBtn = pygame.Rect(850, 10, 25, 25)
		valueBtn = 'X'
		pygame.draw.rect(screen, WHITE, exitBtn)
		textExit = font20.render(valueBtn, True, BLACK)
		screen.blit(textExit, (exitBtn.x+5, exitBtn.y+5))

		text = font20.render("Waiting for another player to connect", True, WHITE)
		textRect = text.get_rect()
		textRect.center = (WIDTH//2, HEIGHT//2)
		screen.blit(text, textRect)
		pygame.display.update()
		clock.tick(FPS)

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
		
		arr_return = receive_response(client_socket)
		if(arr_return):
			if(arr_return[0]==START):
				running = arr_return[0]
			elif(arr_return[0]==FULL):
				screen.fill(BLACK)
				textWinner = font20.render("No rooms available yet, check back soon", True, WHITE)
				textRectWinner = textWinner.get_rect()
				textRectWinner.center = (WIDTH//2, HEIGHT//2)
				screen.blit(textWinner, textRectWinner)
				pygame.display.update()
				pygame.time.wait(7000)
				sys.exit(0)

	return arr_return[1], arr_return[2]

def pong(nicknamePlayer1,nicknamePlayer2,client_socket):
	running = True

	# Defining the objects
	geek1 = Striker(20, 0, 10, 100, 10, GREEN)
	geek2 = Striker(WIDTH-30, 0, 10, 100, 10, GREEN)
	ball = Ball(WIDTH//2, HEIGHT//2, 7, 10, WHITE)

	listOfGeeks = [geek1, geek2]

	# Initial parameters of the players
	geek1Score, geek2Score = 0, 0
	geek1YFac, geek2YFac = 0, 0

	while running:
		screen.fill(BLACK)
		exitBtn = pygame.Rect(WIDTH//2, 10, 25, 25)
		valueBtn = 'X'
		pygame.draw.rect(screen, WHITE, exitBtn)
		textExit = font20.render(valueBtn, True, BLACK)
		screen.blit(textExit, (exitBtn.x+5, exitBtn.y+5))
		arr_return = receive_response(client_socket)
		
		if(arr_return):
			if(arr_return[0] == PAD):
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
			elif(arr_return[0] == PLAYER):
				if(arr_return[1] == DISCONNECTED):
					message = "PLAYER BYE"
					send_request(client_socket, message)
					screen.fill(BLACK)
					textWinner = font20.render(f"You won! the other player left the game", True, WHITE)
					textRectWinner = textWinner.get_rect()
					textRectWinner.center = (WIDTH//2, HEIGHT//2)
					screen.blit(textWinner, textRectWinner)
					pygame.display.update()
					pygame.time.wait(7000)
					running = False

		# Event handling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				message = "PLAYER LEFT "
				send_request(client_socket, message)
				sys.exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					message = "PAD UP"
					send_request(client_socket, message)
				if event.key == pygame.K_DOWN:
					message = "PAD DOWN"
					send_request(client_socket, message)
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					message = "PAD STILL"
					send_request(client_socket, message)
			
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
			message = "GAME POINT LEFT"
			send_request(client_socket, message)
			geek1Score += 1
		elif point == 1:
			message = "GAME POINT RIGHT"
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

		if geek1Score == 5 or geek2Score == 5:
			running = False
			screen.fill(BLACK)
			if(geek1Score == 5):
				message = "GAME END"
				send_request(client_socket, message)
				textWinner = font20.render(f"{nicknamePlayer1} won!", True, WHITE)
			else:
				message = "GAME END"
				send_request(client_socket, message)
				textWinner = font20.render(f"{nicknamePlayer2} won!", True, WHITE)
			textRectWinner = textWinner.get_rect()
			textRectWinner.center = (WIDTH//2, HEIGHT//2)
			screen.blit(textWinner, textRectWinner)
			textWinner2 = font20.render("You are going to be disconnected in 7 seconds", True, WHITE)
			textRectWinner2 = textWinner2.get_rect()
			textRectWinner2.center = (WIDTH//2, HEIGHT//2+40)
			screen.blit(textWinner2, textRectWinner2)
			pygame.display.update()
			pygame.time.wait(7000)
			sys.exit(0)

if __name__ == '__main__':
    pygame.init()
    font20 = pygame.font.Font('freesansbold.ttf', 20)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    WIDTH, HEIGHT = 900, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    FPS = 30
    nicknameCurrentPlayer = login()
    client_socket = set_up_client(nicknameCurrentPlayer)
    action_response = receive_response(client_socket)
    player_names = waitingRoom(action_response,client_socket)
    pong(player_names[0],player_names[1], client_socket)