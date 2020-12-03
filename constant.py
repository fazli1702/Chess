import pygame

# window size
WIDTH, HEIGHT = 480, 480
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS or HEIGHT // ROWS # both are equal

pygame.font.init()
FONT_SIZE = 11
FONT = pygame.font.SysFont('hackregularnerdfontcomplete', FONT_SIZE)

# RGB colours
WHITE = (232, 235, 239)
LIGHT_BLUE = (125, 135, 150)
GREEN = (0, 255, 0)
DARK_GREEN = (123, 153, 105)
RED = (255, 0, 0)
LIGHT_BROWN = (241, 218, 179)
DARK_BROWN = (179, 135, 100)

# load images
W_PAWN = pygame.image.load('images/w_pawn.png')
W_KNIGHT = pygame.image.load('images/w_knight.png')
W_BISHOP = pygame.image.load('images/w_bishop.png')
W_ROOK = pygame.image.load('images/w_rook.png')
W_QUEEN = pygame.image.load('images/w_queen.png')
W_KING = pygame.image.load('images/w_king.png')

B_PAWN = pygame.image.load('images/b_pawn.png')
B_KNIGHT = pygame.image.load('images/b_knight.png')
B_BISHOP = pygame.image.load('images/b_bishop.png')
B_ROOK = pygame.image.load('images/b_rook.png')
B_QUEEN = pygame.image.load('images/b_queen.png')
B_KING = pygame.image.load('images/b_king.png')

g_circle = pygame.image.load('images/g_circle.png')
G_CIRCLE = pygame.transform.scale(g_circle, (60, 60))

g_box = pygame.image.load('images/g_box.png')
G_BOX = pygame.transform.scale(g_box, (60, 60))

capture_circle = pygame.image.load('images/capture.png')
CAPTURE_CIRCLE = pygame.transform.scale(capture_circle, (60, 60))

r_circle = pygame.image.load('images/r_circle.png')
R_CIRCLE = pygame.transform.scale(r_circle, (60, 60))


def get_opposite_colour(colour):
    if colour == 'W':
        return 'B'
    return 'W'

def get_pos_from_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return (col, row)

def convert_to_notation(pos):
    col, row = pos
    cols = {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g', 8:'h'}
    return f'{cols[col+1]}{8-row}'

def convert_to_pos(notation):
    col, row = notation[0], notation[1]
    cols = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    return (cols[col], abs(int(row)-8))
