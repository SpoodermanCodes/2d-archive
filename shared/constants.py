BLOCK = 20
HEADER = 60
FPS = 10

# Colors (R, G, B, A) normalized 0-1
BLACK =      (0, 0, 0, 1)
WHITE =      (1, 1, 1, 1)
DARK_GRAY =  (0.1, 0.1, 0.1, 1)
GRAY =       (0.4, 0.4, 0.4, 1)
GREEN =      (0, 1, 0, 1)
DARK_GREEN = (0, 0.6, 0, 1)
RED =        (1, 0, 0, 1)
DARK_RED =   (0.6, 0, 0, 1)
BLUE =       (0.2, 0.4, 1, 1)
CYAN =       (0, 0.9, 0.9, 1)
YELLOW =     (1, 1, 0, 1)
ORANGE =     (1, 0.5, 0, 1)
PURPLE =     (0.6, 0, 0.8, 1)
MAGENTA =    (1, 0, 1, 1)
PINK =       (1, 0.4, 0.7, 1)

# Tetromino colors
TETROMINO_COLORS = {
    'I': CYAN,
    'O': YELLOW,
    'T': PURPLE,
    'S': GREEN,
    'Z': RED,
    'J': BLUE,
    'L': ORANGE,
}

TETROMINO_SHAPES = {
    'I': [[1,1,1,1]],
    'O': [[1,1],[1,1]],
    'T': [[0,1,0],[1,1,1]],
    'S': [[0,1,1],[1,1,0]],
    'Z': [[1,1,0],[0,1,1]],
    'J': [[1,0,0],[1,1,1]],
    'L': [[0,0,1],[1,1,1]],
}
