PORT = 50000
ENCONDING_FORMAT = "utf-8"
RECV_BUFFER_SIZE = 4096
IP_SERVER = '54.87.213.122'

# SIDES
RIGHT = 'RIGHT'
LEFT = 'LEFT'

# GAME
GAME = 'GAME' 
START = 'START' #When the two users are connected
END = 'END' #When the game is over because one of the two players has won
POINT = 'POINT' #When one of the two players scores a point
FULL = 'FULL' #When game rooms are full

# PLAYER
PLAYER = 'PLAYER' 
NEW = 'NEW' #When a new player is connected
WAIT = 'WAIT' #When a player is waiting for another player to connect
QUIT = 'QUIT' #When a player leaves the game with the X button while waiting another player
LEFT = 'LEFT' #When a player leaves the game with the X button while playing
DISCONNECTED = 'DISCONNECTED' #response When a player leaves the game by closing the window
BYE = 'BYE' #When a player confirms that will end the game by others disconnection

# PAD
PAD = 'PAD'
UP = 'UP' #When a player presses the up arrow
DOWN = 'DOWN' #When a player presses the down arrow
STILL = 'STILL' #When a player releases the up or down arrow
MOVE = 'MOVE' #server response to a PAD_UP, PAD_DOWN or PAD_STILL

# UNRECOGNIZED
UNRECOGNIZED = 'UNRECOGNIZED'