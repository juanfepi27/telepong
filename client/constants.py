PORT = 50000
ENCONDING_FORMAT = "utf-8"
RECV_BUFFER_SIZE = 4096
IP_SERVER = '127.0.0.1'

# GAME
GAME = 'GAME' 
START = 'START' #When the two users are connected
END = 'END' #When the game is over because one of the two players has won
POINT = 'POINT' #When one of the two players scores a point
SCORE = 'SCORE' #When the game score changes because one of the two players scores a point

# PLAYER
PLAYER = 'PLAYER' 
NEW = 'NEW' #When a new player is connected
WAIT = 'WAIT' #When a player is waiting for another player to connect
LEFT = 'LEFT' #When a player leaves the game with the X button
DISCONNECTED = 'DISCONNECTED' #When a player leaves the game by closing the window

# PAD
PAD = 'PAD'
UP = 'UP' #When a player presses the up arrow
DOWN = 'DOWN' #When a player presses the down arrow
STILL = 'STILL' #When a player releases the up or down arrow
MOVE = 'MOVE' #server response to a PAD_UP, PAD_DOWN or PAD_STILL
RIGHT = 'RIGHT'
LEFT = 'LEFT'

# BALL
BALL = 'BALL'
DATA = 'DATA' #when the client sends the ball data to the server
CHANGE = 'CHANGE' #When the server sends the ball data to the client

# UNRECOGNIZED
UNRECOGNIZED = 'UNRECOGNIZED'