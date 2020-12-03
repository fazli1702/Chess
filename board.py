import pygame
from constant import *
from piece import *
from copy import deepcopy


class Board:
    def __init__(self):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.turn = 'W'  # colour
        self.create_board()

    def get_piece(self, pos):
        col, row = pos
        return self.board[row][col]

    def get_board(self):
        return self.board

    def get_king(self, colour):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece((col, row))
                if isinstance(piece, King):
                    if piece.colour == colour:
                        king = piece
                        king.set_pos((col, row))
        return king

    def get_all_moves(self, colour):
        '''return all standard move that can be made by all pieces of specified colour'''
        all_moves = []
        for row in self.board:
            for piece in row:
                if piece != 0:
                    if piece.colour == colour:
                        all_moves.extend(piece.get_moves(self.board))
        return all_moves


    def move(self, piece, new_pos):
        '''move piece - old pos -> new pos, set old pos to empty (0)'''
        curr_col, curr_row = piece.get_pos()
        new_col, new_row = new_pos

        self.board[curr_row][curr_col], self.board[new_row][new_col] = 0, self.board[curr_row][curr_col]
        piece.move(new_pos)


    def is_check(self, colour):
        '''see if king of specified colour in check'''
        king = self.get_king(colour)        
        all_moves = self.get_all_moves(get_opposite_colour(colour))
        if king.get_pos() in all_moves:
            return True
        return False


    def castle(self, side, colour, new_k_pos):
        '''move king and rook to correct squares when castling'''
        king = self.get_king(colour)
        new_k_col, new_k_row = new_k_pos

        if side == 'K':
            r_col = COLS - 1
            new_r_col = new_k_col - 1

        else:
            r_col = 0
            new_r_col = new_k_col + 1

        rook = self.get_piece((r_col, king.row))
        new_r_pos = (new_r_col, king.row)

        print(f'{king.colour}K CASTLE {side} SIDE')
        self.move(king, new_k_pos)
        self.move(rook, new_r_pos)


    def en_passant(self, pawn, new_pos):
        '''move pawn and remove pawn when capture en passant'''
        print('EN PASSANT')
        old_col, old_row = pawn.get_pos()
        new_col, new_row = new_pos
        capture_col, capture_row = new_col, old_row
        self.move(pawn, new_pos)
        self.board[capture_row][capture_col] = 0














    def copy_board(self):
        new_board = []
        for row in self.board:
            new_row = []
            for piece in row:
                if piece == 0:
                    new_row.append(0)
                else:
                    new_piece = deepcopy(piece)
                    new_row.append(new_piece)
            new_board.append(new_row)
        return new_board

    def highlight_square(self, piece, win):
        win.blit(G_BOX, piece.get_coordinate())

    def print_row(self, lst):
        row = '|'
        for ele in lst:
            if ele == 0:
                ele = ''
            row += '{:^4}|'.format(str(ele))
        return row


    def print_board(self):
        '''print board on terminal'''
        l = 43
        print('*' * l)

        for i, row in enumerate(self.board):
            row = str(8-i) + ' ' + self.print_row(row)
            print(row)
            print('-' * l)

        footer = self.print_row(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
        foot = '  ' + footer
        print(foot)
        print('*' * l)


    def create_board(self):
        '''create starting position of all pieces'''

        # pawns - row 1(B), 6(W)
        for col in range(COLS):
            b_p = Pawn(col, 1, 'B')
            w_p = Pawn(col, 6, 'W')

            self.board[1][col] = b_p
            self.board[6][col] = w_p

        # kings - col 4 / e file
        b_k = King(4, 0, 'B')
        w_k = King(4, 7, 'W')
        self.board[0][4] = b_k
        self.board[7][4] = w_k

        # queens - col 3 / d file
        b_q = Queen(3, 0, 'B')
        w_q = Queen(3, 7, 'W')
        self.board[0][3] = b_q
        self.board[7][3] = w_q

        # rooks - col 0, 7 / a, h file
        for col in [0, 7]:
            b_r = Rook(col, 0, 'B')
            w_r = Rook(col, 7, 'W')
            self.board[0][col] = b_r
            self.board[7][col] = w_r

        # knights - col 1, 6 / b, g file
        for col in [1, 6]:
            b_n = Knight(col, 0, 'B')
            w_n = Knight(col, 7, 'W')
            self.board[0][col] = b_n
            self.board[7][col] = w_n

        # bishop - col 2, 5 / c, f file
        for col in [2, 5]:
            b_b = Bishop(col, 0, 'B')
            w_b = Bishop(col, 7, 'W')
            self.board[0][col] = b_b
            self.board[7][col] = w_b

    def draw_check(self, colour, win):
        king = self.get_king(colour)
        king.draw_check(win)


    def draw_squares(self, win):
        '''draw checkerboard pattern'''
        win.fill(LIGHT_BROWN)
        for row in range(ROWS):
            for col in range((row+1) % 2, COLS, 2):
                pygame.draw.rect(win, DARK_BROWN, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    
    def draw_rank(self, win):
        '''draw rank/row number at left side of board'''
        x, y = 2, 2
        for i in range(8, 0, -1):
            colour = LIGHT_BROWN if i % 2 != 0 else DARK_BROWN
            text = FONT.render(str(i), True, colour)
            win.blit(text, (x, y))
            y += SQUARE_SIZE

    def draw_file(self, win):
        '''draw file/col number at bottom of board'''
        file = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        x, y = SQUARE_SIZE - FONT_SIZE + 3, HEIGHT - FONT_SIZE - 3
        for i, ele in enumerate(file):
            colour = LIGHT_BROWN if i % 2 == 0 else DARK_BROWN
            text = FONT.render(ele, True, colour)
            win.blit(text, (x, y))
            x += SQUARE_SIZE
            


    def draw_board(self, win):
        '''draw board and draw pieces onto board'''
        self.draw_squares(win)
        self.draw_rank(win)
        self.draw_file(win)

    def draw_pieces(self, win):
        for row in self.board:
            for piece in row:
                if piece == 0:
                    continue
                else:
                    piece.show(win)